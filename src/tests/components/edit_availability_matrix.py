from src.tests.database_example import database_example 

from src.UI.components.edit_availability_matrix import EditAvailabilityMatrix

import flet as ft 
def main(page : ft.Page):
    professor = database_example.professors.get()[0]
    sb = EditAvailabilityMatrix()
    page.add(sb)
    
    
ft.app(main)