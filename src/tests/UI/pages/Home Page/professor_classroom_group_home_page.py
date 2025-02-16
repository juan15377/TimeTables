from src.UI.pages.home_page.components import ProfessorHomePage, ClassroomHomePage, GroupHomePage
from src.tests.database_example import database_example
import flet as ft

def main(page : ft.Page):
    page.theme_mode = "dark"

    # Example usage:
    database = database_example
    page.add(ProfessorHomePage())
    

ft.app(main)