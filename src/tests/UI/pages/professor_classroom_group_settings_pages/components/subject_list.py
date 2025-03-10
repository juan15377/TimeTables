from src.UI.pages.professor_classroom_group_settings_pages.components.subject_list import SubjectList 
import flet as ft 
from src.tests.database_example import database_example
def main(page : ft.Page):
    call_subjects = database_example.professors.get()[0].get_subjects
    
    page.add(SubjectList(page, call_subjects))
    
ft.app(main)