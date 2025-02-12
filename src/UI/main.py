import flet as ft  
from .routes import router
from .State import global_state 
from src.UI.components.navigator_bars import NavBar

def main(page: ft.Page):

    page.theme_mode = "dark"
    page.appbar = NavBar(page)
    page.on_route_change = lambda route : router.route_change(route, page)
    router.page = page
    page.add(
        router.body
    )
    page.go('/')

