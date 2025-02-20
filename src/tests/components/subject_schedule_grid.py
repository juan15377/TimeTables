from src.tests.database_example import database_example, professor, materia_0

from src.UI.components.subjects_schedule_grid import SubjectScheduleGrid

print("FYTGUH", len(professor.subjects))
import flet as ft 
def main(page : ft.Page):
    print(professor.name)
    sb = SubjectScheduleGrid(page, professor)
    page.add(sb)
    
    
ft.app(main)