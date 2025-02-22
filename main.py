import dash_mantine_components as dmc
from dash import (
    Dash,
    _dash_renderer,
    Input,
    Output,
    # State,
    # callback,
    html,
    clientside_callback,
)
from dash_iconify import DashIconify

_dash_renderer._set_react_version("18.2.0")

app = Dash(external_stylesheets=dmc.styles.ALL)
app._favicon = "icon.svg"


def get_icon(icon):
    return DashIconify(icon=icon, height=16)


theme_toggle = dmc.Switch(
    offLabel=DashIconify(
        icon="radix-icons:sun",
        width=20,
    ),
    onLabel=DashIconify(
        icon="radix-icons:moon",
        width=20,
    ),
    id="color-scheme-switch",
    persistence=True,
    color="grey",
    size="md",
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
                        ),
                        dmc.NavLink(
                            label="Portfolios",
                            leftSection=get_icon(icon="octicon:repo-24"),
                            rightSection=get_icon(icon="tabler-chevron-right"),
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
                                dmc.Title("Charizard (Pokémon)", order=3),
                            ]
                        ),
                        *[
                            dmc.NavLink(
                                label=f"Link_{i+1}",
                                leftSection=get_icon(icon="tabler:activity"),
                                rightSection=get_icon(
                                    icon="tabler-chevron-right"
                                ),
                                variant="light",
                                active=True,
                            )
                            for i in range(100)
                        ],
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
    (switchOn) => {
       document.documentElement.setAttribute('data-mantine-color-scheme',
       switchOn ? 'dark' : 'light');
       return window.dash_clientside.no_update
    }
    """,
    Output("color-scheme-switch", "id"),
    Input("color-scheme-switch", "checked"),
)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
