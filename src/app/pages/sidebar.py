import dash_mantine_components as dmc
from dash import html

from .elements import get_icon


def sidebar():
    return dmc.AppShellNavbar(
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
                        label="Database",
                        leftSection=get_icon(icon="octicon:database-16"),
                        children=[
                            html.Div(
                                style={
                                    "display": "flex",
                                    "align-items": "flex-end",
                                    "gap": "5px",  # Space between items
                                },
                                children=[
                                    dmc.TagsInput(
                                        label="Scrape Stock",
                                        placeholder="NSE or BSE Stock ID",
                                        required=True,
                                        id="scrape_text",
                                        clearable=True,
                                        style={
                                            "flexGrow": 1,
                                            "width": "200px",
                                        },  # Allow text input to grow
                                    ),
                                    dmc.Button(
                                        "Scrape",
                                        id="scrape_click",
                                        variant="outline",
                                        disabled=False,
                                        rightSection=get_icon(
                                            "mdi:download-circle"
                                        ),
                                    ),
                                    html.Div(id="notifications_container"),
                                ],
                            ),
                        ],
                    ),
                    dmc.NavLink(
                        label="Screener",
                        leftSection=get_icon(icon="mingcute:filter-line"),
                    ),
                ],
            )
        ],
        p="md",
        style={
            # When you change the width, also change the width in dmc.AppShell
            "width": "400px",
            "padding": "20px",
            "height": "100vh",
            "display": "inline-block",
            "verticalAlign": "top",
        },
    )
