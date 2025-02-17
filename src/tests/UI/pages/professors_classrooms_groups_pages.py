from src.UI.pages.professors_classrooms_groups_pages import ProfessorsPage, ClassroomsPage, GroupsPage
import flet as ft 
from src.tests.database_example import database_example

def main(page : ft.Page):
    page.theme_mode = "dark"

    # Example usage:
    database = database_example
    professors_page = ProfessorsPage(page, "")
    #classrooms_page = ClassroomsPage(database_example, page)
    #groups_page = GroupsPage(database_example, page)

    page.add(professors_page)
    #page.add(classrooms_page)
    #page.add(groups_page)


ft.app(main)
