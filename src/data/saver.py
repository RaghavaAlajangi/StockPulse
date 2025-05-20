import sqlite3
from pathlib import Path

from dotenv import load_dotenv

from .screener_headers import percentage_headers, ratio_headers, table_headers

load_dotenv()

DB_PATH = Path(__file__).resolve().parents[2] / "database" / "stocks.db"


class StockDatabase:
    def __init__(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create necessary tables to store stock data."""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS stock_names (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT UNIQUE,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS key_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            metric_name TEXT,
            value REAL,
            UNIQUE(stock_id, metric_name),
            FOREIGN KEY(stock_id) REFERENCES stocks(id)
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS peer_comparision (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            peer_name TEXT,
            param TEXT,
            value REAL,
            UNIQUE(stock_id, peer_name, param),
            FOREIGN KEY(stock_id) REFERENCES stocks(id)
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS quarterly_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            category TEXT,
            year TEXT,
            value REAL,
            UNIQUE(stock_id, category, year),
            FOREIGN KEY(stock_id) REFERENCES stocks(id)
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS profit_loss (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            category TEXT,
            year TEXT,
            value REAL,
            UNIQUE(stock_id, category, year),
            FOREIGN KEY(stock_id) REFERENCES stocks(id)
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS stock_percentages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            metric TEXT,
            year TEXT,
            value REAL,
            UNIQUE(stock_id, metric, year),
            FOREIGN KEY(stock_id) REFERENCES stocks(id)
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS balance_sheet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            category TEXT,
            year TEXT,
            value REAL,
            UNIQUE(stock_id, category, year),
            FOREIGN KEY(stock_id) REFERENCES stocks(id)
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cash_flow (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            category TEXT,
            year TEXT,
            value REAL,
            UNIQUE(stock_id, category, year),
            FOREIGN KEY(stock_id) REFERENCES stocks(id)
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ratios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            category TEXT,
            year TEXT,
            value REAL,
            UNIQUE(stock_id, category, year),
            FOREIGN KEY(stock_id) REFERENCES stocks(id)
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS shareholding_pattern (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_id INTEGER,
            category TEXT,
            year TEXT,
            value REAL,
            UNIQUE(stock_id, category, year),
            FOREIGN KEY(stock_id) REFERENCES stocks(id)
            )
            """
        )

        self.conn.commit()

    def save_db(self, stock_ticker, stock_data):
        stock_ticker_id = self.insert_stock(stock_ticker)
        self.insert_key_metrics(
            stock_ticker_id,
            {key: stock_data.get(key, None) for key in ratio_headers},
        )
        self.insert_financial_tables(stock_ticker_id, stock_data["tables"])
        self.insert_stock_percentages(
            stock_ticker_id,
            {key: stock_data.get(key, {}) for key in percentage_headers},
        )

    def insert_stock(self, ticker):
        """Insert stock if not exists and return stock ID."""
        self.cursor.execute(
            """
            INSERT INTO stock_names (ticker, last_updated)
            VALUES (?, CURRENT_TIMESTAMP)
            ON CONFLICT(ticker)
            DO UPDATE SET last_updated = CURRENT_TIMESTAMP
            """,
            (ticker,),
        )
        self.conn.commit()
        self.cursor.execute(
            "SELECT id FROM stock_names WHERE ticker = ?", (ticker,)
        )
        return self.cursor.fetchone()[0]

    def record_exists(self, table, conditions):
        """Check if a record exists in a table."""
        query = f"SELECT 1 FROM {table} WHERE " + " AND ".join(
            f"{col} = ?" for col in conditions.keys()
        )
        self.cursor.execute(query, tuple(conditions.values()))
        return self.cursor.fetchone() is not None

    def insert_key_metrics(self, stock_id, metrics):
        """Insert a metric values only if they don't already exist."""
        for key, value in metrics.items():
            self.cursor.execute(
                """
                INSERT INTO key_metrics (
                stock_id,
                metric_name,
                value)
                VALUES (?, ?, ?)
                ON CONFLICT(stock_id, metric_name)
                DO UPDATE SET value = excluded.value
                """,
                (stock_id, key, value),
            )
        self.conn.commit()

    def insert_financial_tables(self, stock_id, tabel_data):
        """Insert financial table data only if they don't already exist."""
        for table_name, table_row_list in tabel_data.items():
            db_head_name = table_headers[table_name]
            if db_head_name != "peer_comparision":
                for trow_dict in table_row_list:
                    for key, values in trow_dict.items():
                        for year, value in values.items():
                            self.cursor.execute(
                                f"""
                                INSERT INTO {db_head_name} (
                                stock_id,
                                category,
                                year,
                                value)
                                VALUES (?, ?, ?, ?)
                                ON CONFLICT(stock_id, category, year)
                                DO UPDATE SET value = excluded.value
                                """,
                                (stock_id, key, year, value),
                            )
            else:
                for trow_dict in table_row_list:
                    peer_name, param = None, None
                    for slno, peer_dict in trow_dict.items():
                        for i, (key, value) in enumerate(peer_dict.items()):
                            if i == 0:
                                peer_name = value
                                continue
                            else:
                                param = key
                            self.cursor.execute(
                                """
                                INSERT INTO peer_comparision (
                                stock_id,
                                peer_name,
                                param,
                                value)
                                VALUES (?, ?, ?, ?)
                                ON CONFLICT(stock_id, peer_name, param)
                                DO UPDATE SET value = excluded.value
                                """,
                                (stock_id, peer_name, param, value),
                            )
        self.conn.commit()

    def insert_stock_percentages(self, stock_id, percentages):
        """Insert percentage values only if they don't already exist."""
        for key, values in percentages.items():
            for year, value in values.items():
                self.cursor.execute(
                    """
                    INSERT INTO stock_percentages (
                    stock_id, metric, year, value)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(stock_id, metric, year)
                    DO UPDATE SET value = excluded.value
                    """,
                    (stock_id, key, year, value),
                )
        self.conn.commit()
