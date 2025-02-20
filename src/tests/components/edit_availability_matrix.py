from src.tests.database_example import database_example 

from src.UI.components.subjects_schedule_grid import SubjectScheduleGrid

import flet as ft 
def main(page : ft.Page):
    professor = database_example.professors.get()[0]
    sb = SubjectScheduleGrid(professor)
    page.add(sb)
    
    
ft.app(main)