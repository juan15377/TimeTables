import flet as ft
from ...State import global_state

def NavBar(page):

    NavBar = ft.AppBar(
            leading=ft.IconButton(ft.icons.HOME, on_click=lambda _: page.go(global_state.get_state_by_key("previous_page"))),
            leading_width=40,
            title=ft.Text("Flet Router"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.HOME, on_click=lambda _: page.go('/'))
            ]
        )

    return NavBar