import dash_mantine_components as dmc
from dash_iconify import DashIconify

from .elements import toggle_theme


def header():
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
