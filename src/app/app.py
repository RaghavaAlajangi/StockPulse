import dash_mantine_components as dmc
from dash import (
    Dash,
    _dash_renderer,
    Input,
    Output,
    # State,
    callback,
    html,
    clientside_callback,
    MATCH,
)
from dash_iconify import DashIconify

from mock_data import generate_mock_stock_data
import random

data = generate_mock_stock_data()

_dash_renderer._set_react_version("18.2.0")

app = Dash(external_stylesheets=dmc.styles.ALL)
app._favicon = "icon.svg"


def dummy_tabs():
    tlist = [
        "quarterly_results",
        "annual_results",
        "balance_sheet",
        "share_holding_pattern",
    ]
    return dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.TabsTab(
                        f"{d}",
                        value=f"{d}",
                    )
                    for d in tlist
                ]
            ),
            *[
                dmc.TabsPanel(
                    children=[
                        dmc.Table(
                            data={
                                "caption": f"{s} tab content",
                                "head": [
                                    "Element position",
                                    "Atomic mass",
                                    "Symbol",
                                    "Element name",
                                ],
                                "body": [
                                    [
                                        6,
                                        12.011,
                                        "C",
                                        "Carbon",
                                    ],
                                    [
                                        7,
                                        14.007,
                                        "N",
                                        "Nitrogen",
                                    ],
                                    [
                                        39,
                                        88.906,
                                        "Y",
                                        "Yttrium",
                                    ],
                                    [
                                        56,
                                        137.33,
                                        "Ba",
                                        "Barium",
                                    ],
                                    [
                                        58,
                                        140.12,
                                        "Ce",
                                        "Cerium",
                                    ],
                                ],
                            }
                        ),
                    ],
                    value=f"{s}",
                )
                for s in tlist
            ],
        ],
        color="red",
        orientation="horizontal",
        variant="default",
        value=tlist[0],
    )


def get_icon(icon):
    return DashIconify(icon=icon, height=16)


theme_toggle = dmc.SegmentedControl(
    id="switch_theme",
    persistence=True,
    data=[
        {
            "label": dmc.Center(
                DashIconify(
                    icon="radix-icons:sun",
                    width=15,
                )
            ),
            "value": "light",
        },
        {
            "label": dmc.Center(
                DashIconify(
                    icon="radix-icons:moon",
                    width=15,
                )
            ),
            "value": "dark",
        },
    ],
    transitionDuration=0,
    value="dark",
    radius="md",
    size="xs",
)


def make_control(text, action_id):
    rlist = ["price", "ROE", "ROCE", "PEG"]
    return dmc.Flex(
        [
            dmc.AccordionControl(
                children=[
                    dmc.Text(text, fw=700),
                    dmc.Text("company code", size="xs"),
                    html.Br(),
                    dmc.Group(
                        [
                            *[
                                dmc.Stack(
                                    [
                                        dmc.Text(ro, size="xs"),
                                        dmc.Text(data[text][ro.lower()]),
                                    ],
                                    align="center",
                                    gap="xs",
                                )
                                for ro in rlist
                            ],
                            *[
                                dmc.Stack(
                                    [
                                        dmc.Text(f"kpi-{i}", size="xs"),
                                        DashIconify(
                                            icon="ri:heart-add-fill",
                                            width=20,
                                            color=random.choice(
                                                ["green", "red"]
                                            ),
                                        ),
                                    ],
                                    align="center",
                                    gap="xs",
                                )
                                for i in range(4)
                            ],
                        ]
                    ),
                ]
            ),
            dmc.ActionIcon(
                children=DashIconify(icon="tabler:heart"),
                color="red",
                variant="transparent",
                n_clicks=0,
                id={"index": action_id},
            ),
        ],
        justify="space-between",
    )


layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
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
                            theme_toggle,
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
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=[
                html.Div(
                    children=[
                        dmc.NavLink(
                            label="Home",
                            leftSection=get_icon(icon="bi:house-door-fill"),
                        ),
                        dmc.NavLink(
                            label="Wishlists",
                            leftSection=get_icon(
                                icon="mingcute:heartbeat-2-line"
                            ),
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
                                    leftSection=get_icon(
                                        icon="octicon:repo-24"
                                    ),
                                ),
                                dmc.NavLink(
                                    label="Portfolio 2",
                                    leftSection=get_icon(
                                        icon="octicon:repo-24"
                                    ),
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
                "width": "300px",
                # "background": "#16121c",
                # "color": "white",
                "padding": "20px",
                "height": "100vh",
                "display": "inline-block",
                "verticalAlign": "top",
            },
        ),
        dmc.AppShellMain(
            children=[
                dmc.ScrollArea(
                    # h=250,
                    # w=350,
                    children=[
                        html.Div(
                            [
                                dmc.Title("Stocks List", order=2),
                            ]
                        ),
                        dmc.Accordion(
                            id="accordion-compose-controls",
                            chevronPosition="left",
                            children=[
                                dmc.AccordionItem(
                                    [
                                        make_control(f"{i}", f"action-{i}"),
                                        dmc.AccordionPanel(
                                            dmc.ScrollArea(
                                                h=400,
                                                children=[dummy_tabs()],
                                            ),
                                        ),
                                    ],
                                    value=f"item-{i}",
                                )
                                for i in data.keys()
                            ],
                            variant="separated",
                        ),
                    ],
                ),
            ],
            style={
                # "background": "#211b1b",
                # "padding": "20px",
                "display": "inline-block",
                "height": "100vh",
                "verticalAlign": "top",
            },
        ),
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


def run_app(local=True, host="0.0.0.0", port=8050):
    if local:
        app.run_server(debug=True)
    else:
        app.run_server(host=host, port=port, debug=False)
