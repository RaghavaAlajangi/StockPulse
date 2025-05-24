import dash_mantine_components as dmc


def main_layout():
    return dmc.AppShellMain(
        children=[
            dmc.ScrollArea(
                # h=250,
                # w=350,
                children=[
                    dmc.Title("Stocks Grid", order=2),
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
    )
