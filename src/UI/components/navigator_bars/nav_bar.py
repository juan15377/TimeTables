import flet as ft
from ...State import global_state


class NavBar(ft.AppBar):
    
    def __init__(self, page : ft.Page):
        
        def get_previous_page():
            return global_state.get_state_by_key("manager_routes").get_state().get_prevoius()
            
        super().__init__(
            leading=ft.IconButton(ft.icons.ARROW_BACK_IOS_NEW, on_click= lambda e: page.go(get_previous_page()
                                                                                        )),
            leading_width=40,
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
                ft.IconButton(ft.icons.FILTER_3, on_click = lambda e: page.go("/PROFESSORS")),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Item 1",
                                         icon = ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click = lambda e: page.go("/PROFESSORS"))),
                        ft.PopupMenuItem(),  # divider
                        ft.PopupMenuItem(
                            text="Checked item", checked=False
                        ),
                    ]
                ),
            ],
        )
