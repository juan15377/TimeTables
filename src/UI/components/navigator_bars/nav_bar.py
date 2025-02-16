import flet as ft
from ...State import global_state


class NavBar(ft.AppBar):
    
    def __init__(self, page : ft.Page):
        super().__init__(
            leading=ft.IconButton(ft.icons.ARROW_BACK_IOS_NEW, on_click= lambda e: page.go(global_state.get_state_by_key("previous_page").get_state())),
            leading_width=40,
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
                ft.IconButton(ft.icons.FILTER_3),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Item 1"),
                        ft.PopupMenuItem(),  # divider
                        ft.PopupMenuItem(
                            text="Checked item", checked=False
                        ),
                    ]
                ),
            ],
        )
