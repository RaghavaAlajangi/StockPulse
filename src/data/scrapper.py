import os
import time
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .saver import StockDatabase
from .screener_headers import percentage_headers, ratio_headers, table_headers

load_dotenv()


class ScreenerWeb:
    def __init__(self):
        self.login_url = "https://www.screener.in/login/"
        self.stock_data = {
            "tables": {},
        }
        self.db = StockDatabase()

    def scrap_stock(self, screener_ticker):
        """Scrap stock data and store it in the database."""
        driver = self._screener_login()

        ticker_list = (
            [screener_ticker]
            if not isinstance(screener_ticker, list)
            else screener_ticker
        )

        for st in ticker_list:
            web_url = f"https://www.screener.in/company/{st}/"
            driver.get(web_url)
            time.sleep(4)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            self.stock_data = {"tables": {}}

            # Parallelize data extraction where possible
            with ThreadPoolExecutor() as executor:
                executor.submit(self._extract_key_metrics, soup)
                executor.submit(self._extract_tables, soup)
                executor.submit(self._extract_percentage_tables, soup)

            # Store Data in DB
            self.db.save_db(st, self.stock_data)
        driver.close()

    def _screener_login(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # New headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware
        chrome_options.add_argument("--window-size=1920,1080")  # Set window
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.login_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        driver.find_element(By.NAME, "username").send_keys(os.getenv("USER"))
        driver.find_element(By.NAME, "password").send_keys(os.getenv("PASS"))
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)
        return driver

    def _extract_key_metrics(self, soup):
        """Extract key financial key metrics."""
        for ratio_key in ratio_headers:
            name_span = soup.find(
                "span",
                class_="name",
                string=lambda text: text and ratio_key in text,
            )
            if name_span:
                value_span = name_span.find_next_sibling(
                    "span", class_="nowrap value"
                )
                if value_span:
                    num_span = value_span.find("span", class_="number")
                    ratio_val = num_span.text.strip() if num_span else None
                    self.stock_data[ratio_key] = ratio_val

    def _extract_tables(self, soup):
        """Extract financial tables."""
        for table_key in table_headers.keys():
            heading = soup.find("h2", string=table_key)
            if heading:
                raw_table = heading.find_next("table")
                if raw_table:
                    headers = [
                        th.text.strip() for th in raw_table.find_all("th")
                    ]
                    rows = raw_table.find_all("tr")[1:]

                    rows_list = []
                    for tr in rows:
                        cells = tr.find_all("td")
                        sub_head = cells[0].text.strip()
                        row_data = {
                            sub_head: {
                                h: c.text.strip()
                                for h, c in zip(headers[1:], cells[1:])
                            }
                        }
                        rows_list.append(row_data)
                    self.stock_data["tables"][table_key] = rows_list
                else:
                    self.stock_data["tables"][table_key] = None

    def _extract_percentage_tables(self, soup):
        """Extract percentage tables."""
        for per_key in percentage_headers:
            for table in soup.find_all("table", class_="ranges-table"):
                if table.find("th") and per_key in table.find("th").text:
                    rows = table.find_all("tr")[1:]
                    per_table = {
                        row.find_all("td")[0]
                        .text.strip(): row.find_all("td")[1]
                        .text.strip()
                        for row in rows
                    }
                    self.stock_data[per_key] = per_table
                    break
