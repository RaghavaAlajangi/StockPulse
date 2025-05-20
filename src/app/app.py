import dash_mantine_components as dmc
from dash import MATCH, Dash, Input, Output, _dash_renderer, callback
from dash import callback_context as ctx
from dash import clientside_callback, html, no_update
from dash_iconify import DashIconify

from ..data import ScreenerWeb
from .elements import get_icon, toggle_theme

_dash_renderer._set_react_version("18.2.0")

app = Dash(external_stylesheets=dmc.styles.ALL)
app._favicon = "icon.svg"


def app_header():
    return dmc.AppShellHeader(
        dmc.Group(
            [
                dmc.Group(
                    [
                        dmc.Image(src="assets/icon.svg", h=35),
                        dmc.Title("StockPulse", c="white"),
                    ],
                    h="100%",
                    px="md",
                ),
                dmc.Group(
                    [
                        toggle_theme(),
                        dmc.Avatar(
                            DashIconify(
                                icon="mingcute:user-4-fill",
                                color="white",
                                width=33,
                                height=33,
                            ),
                            variant="transparent",
                            radius="md",
                            size="md",
                        ),
                        dmc.Avatar(
                            DashIconify(
                                icon="octicon:mark-github-24",
                                color="white",
                                width=30,
                                height=30,
                            ),
                            variant="transparent",
                            radius="md",
                            size="md",
                        ),
                    ],
                    h="100%",
                    px="md",
                ),
            ],
            justify="space-between",
            style={"flex": 1},
            h="100%",
            px="md",
        ),
        style={
            "background": "linear-gradient(to right, #130d82, #3316d9,"
            "#320da1, #430666)",
            "color": "white",
            "padding": "10px",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "space-between",
        },
    )


def app_sidebar():
    return dmc.AppShellNavbar(
        id="navbar",
        children=[
            html.Div(
                children=[
                    html.Div(
                        style={
                            "display": "flex",
                            "align-items": "flex-end",
                            "gap": "5px",  # Space between items
                        },
                        children=[
                            dmc.TagsInput(
                                label="Enter Stock Name",
                                placeholder="Valid stocks all you like!",
                                required=True,
                                id="scrape_text",
                                clearable=True,
                                style={
                                    "flexGrow": 1
                                },  # Allow text input to grow
                            ),
                            dmc.Button(
                                "Fetch",
                                id="scrape_click",
                                variant="outline",
                                leftSection=get_icon(
                                    "fluent:database-plug-connected-20-filled"
                                ),
                            ),
                            html.Div(id="notifications_container"),
                        ],
                    ),
                    dmc.NavLink(
                        label="Home",
                        leftSection=get_icon(icon="bi:house-door-fill"),
                    ),
                    dmc.NavLink(
                        label="Wishlists",
                        leftSection=get_icon(icon="mingcute:heartbeat-2-line"),
                        rightSection=get_icon(icon="tabler-chevron-right"),
                        children=[
                            dmc.NavLink(
                                label="Wishlist 1",
                                leftSection=get_icon(
                                    icon="mingcute:heartbeat-2-line"
                                ),
                            ),
                            dmc.NavLink(
                                label="Wishlist 2",
                                leftSection=get_icon(
                                    icon="mingcute:heartbeat-2-line"
                                ),
                            ),
                            dmc.NavLink(
                                label="Wishlist 3",
                                leftSection=get_icon(
                                    icon="mingcute:heartbeat-2-line"
                                ),
                            ),
                        ],
                    ),
                    dmc.NavLink(
                        label="Portfolios",
                        leftSection=get_icon(icon="octicon:repo-24"),
                        rightSection=get_icon(icon="tabler-chevron-right"),
                        children=[
                            dmc.NavLink(
                                label="Portfolio 1",
                                leftSection=get_icon(icon="octicon:repo-24"),
                            ),
                            dmc.NavLink(
                                label="Portfolio 2",
                                leftSection=get_icon(icon="octicon:repo-24"),
                            ),
                        ],
                    ),
                    dmc.NavLink(
                        label="Screener",
                        leftSection=get_icon(icon="mingcute:filter-line"),
                    ),
                    dmc.NavLink(
                        label="Database",
                        leftSection=get_icon(icon="octicon:database-16"),
                    ),
                    dmc.NavLink(
                        label="Disabled",
                        leftSection=get_icon(icon="tabler:circle-off"),
                        disabled=True,
                    ),
                ],
            )
        ],
        p="md",
        style={
            "width": "450px",
            # "background": "#16121c",
            # "color": "white",
            "padding": "20px",
            "height": "100vh",
            "display": "inline-block",
            "verticalAlign": "top",
        },
    )


def app_main():
    return dmc.AppShellMain(
        children=[
            # dmc.ScrollArea(
            #     # h=250,
            #     # w=350,
            #     children=[
            #         html.Div(
            #             [
            #                 dmc.Title("Stocks List", order=2),
            #             ]
            #         ),
            #         dmc.Accordion(
            #             id="accordion-compose-controls",
            #             chevronPosition="left",
            #             children=[
            #                 dmc.AccordionItem(
            #                     [
            #                         make_control(f"{i}", f"action-{i}"),
            #                         dmc.AccordionPanel(
            #                             dmc.ScrollArea(
            #                                 h=400,
            #                                 children=[dummy_tabs()],
            #                             ),
            #                         ),
            #                     ],
            #                     value=f"item-{i}",
            #                 )
            #                 for i in data.keys()
            #             ],
            #             variant="separated",
            #         ),
            #     ],
            # ),
        ],
        style={
            # "background": "#211b1b",
            # "padding": "20px",
            "display": "inline-block",
            "height": "100vh",
            "verticalAlign": "top",
        },
    )


layout = dmc.AppShell(
    [
        app_header(),
        app_sidebar(),
        app_main(),
    ],
    header={"height": 80},
    padding="md",
    navbar={
        "width": 300,
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
    Output("notifications_container", "children"),
    Output("scrape_click", "loading"),
    Input("scrape_text", "value"),
    Input("scrape_click", "n_clicks"),
    prevent_initial_call=True,
)
def scrape_stcok_data(stock_list, sclick):
    button_id = ctx.triggered_id
    web = ScreenerWeb()
    if button_id and stock_list:
        if "scrape_click" in button_id:
            web.scrap_stock(stock_list)
            return (
                dmc.Notification(
                    title="Data Scraped!",
                    id="scrape_notify",
                    action="show",
                    message="Stocks data have been stored in DB!",
                    icon=DashIconify(icon="ic:round-celebration"),
                    position="bottom-right",
                ),
                False,
            )

    return no_update, no_update


def run_app(local=True, host="0.0.0.0", port=100):
    if local:
        app.run(debug=True)
    else:
        app.run(host=host, port=port, debug=False)
