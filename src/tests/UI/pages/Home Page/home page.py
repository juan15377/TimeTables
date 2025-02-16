from src.UI.pages.home_page import HomePage
from src.tests.database_example import database_example
import flet as ft
from src.UI.components.navigator_bars import NavBar
import flet as ft 

def main(page : ft.Page):
    page.theme_mode = "dark"
    
    page.appbar = NavBar(page)
    page.add(HomePage(page, ""))
    



ft.app(main)

