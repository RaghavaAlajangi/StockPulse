import dash_mantine_components as dmc
from dash import MATCH, Dash, Input, Output, State, _dash_renderer, callback
from dash import callback_context as ctx
from dash import clientside_callback, no_update

from ..data import ScreenerWeb
from .pages import header, main_layout, sidebar

_dash_renderer._set_react_version("18.2.0")

app = Dash(external_stylesheets=dmc.styles.ALL)
app._favicon = "icon.svg"


layout = dmc.AppShell(
    [
        header(),
        sidebar(),
        main_layout(),
    ],
    header={"height": 80},
    padding="md",
    navbar={
        # Sidebar menu width
        "width": 400,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    id="appshell",
)

app.layout = dmc.MantineProvider(layout)


clientside_callback(
    """
    (colorScheme) => {
       document.documentElement.setAttribute('data-mantine-color-scheme',
       colorScheme);
       return window.dash_clientside.no_update
    }
    """,
    Output("switch_theme", "id"),
    Input("switch_theme", "value"),
)


@callback(
    Output({"index": MATCH}, "variant"), Input({"index": MATCH}, "n_clicks")
)
def update_heart(n):
    if n % 2 == 0:
        return "default"
    return "filled"


clientside_callback(
    """
    function updateLoadingState(n_clicks) {
        return true
    }
    """,
    Output("scrape_click", "loading", allow_duplicate=True),
    Input("scrape_click", "n_clicks"),
    prevent_initial_call=True,
)


@callback(
    Output("scrape_click", "disabled"),
    Input("scrape_text", "value"),
    State("scrape_click", "disabled"),
)
def toggle_scrape_button(stock_list, click_enabled):
    if stock_list and len(stock_list) > 0:
        return not click_enabled
    return no_update, no_update


@callback(
    Output("scrape_text", "value"),
    Output("scrape_click", "loading"),
    Input("scrape_text", "value"),
    Input("scrape_click", "n_clicks"),
    prevent_initial_call=True,
)
def scrape_stock_data(stock_list, sclick):
    button_id = ctx.triggered_id
    web = ScreenerWeb()
    if button_id and stock_list:
        if "scrape_click" in button_id:
            web.scrap_stock(stock_list)
            return (
                None,
                False,
            )

    return no_update, no_update


def run_app(local=True, host="0.0.0.0", port=100):
    if local:
        app.run(debug=True)
    else:
        app.run(host=host, port=port, debug=False)
