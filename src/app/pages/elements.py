import dash_mantine_components as dmc
from dash_iconify import DashIconify


def toggle_theme():
    return dmc.SegmentedControl(
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


def get_icon(icon):
    return DashIconify(icon=icon, height=16)


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
