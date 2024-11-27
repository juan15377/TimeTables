import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors

import sys 
sys.path.append("src/Logic/")
sys.path.append("tests/Logic/")
sys.path.append("src/GUI/Editor Materia ")
sys.path.append("src/GUI/Pagina profesor")

from Editor_materia import *

from Professor_page import *





def load_professor_page(profesor):
    
    pass

def load_classroom_page(classroom):
    pass 


def load_subjects_page(subject):
    pass


#/main/juan_de_jesus/calculo/





ROUTE_PROFESSOR = '/PROFESSOR'
ROUTE_CLASSROOM = '/CLASSROOM'
ROUTE_SUBJECTS = '/GROUP'
#                                                .subject
#                                          |----SUBJECT_DETAILS
#                     |-----|---PROFESSORS--
#                    |         .professor  |---PROFESSOR_DETAILS
#     |---PROFESSOR----
#     |                             |---CLASSROOM_DETAILS
#/ ---|---CLASSROOM------CLASSROOMS--
#     |                   .classroom |-------SUBJECT_DETAILS
#     |---GROUP---                             .subject
#                |          |-------GROUP_DETAILS
#                |---GROUPS--
#                  .group   |--- SUBJECT_DETAILS
#                                 .subject

# va ser unos de los puntos de los cuales la aplicacion va arrancar
# esta clase sera la encargada de recibir una ruta o un profesor, aula o grupo, materia 
# de esta forma generara y cambiara la pagina 
class Enruter_page():
    
    
    def __init__(self, page) -> None:
        page.title = "TimeTables"
        self.page
        
    def change_page(self, page_content, route):
        self.page.views.clear()
        
        self.page.views.append(View(route, 
                                   page_content))
            
        self.page.update()


    def navigate_to_professors(self):
        
        
        pass 
    
    def navigate_to_new_professor(self):
        pass
    
    def navigate_to_lassrooms(self, classroom):
        pass
    
    def navigate_to_groups(self, group):
        pass  
    
    def navigate_to_subject(self, subject):# in the subject 
        pass
    
        

        
    


def main(page: Page):
    page.title = 'Ejemplo de Rutas'

    def route_change(route):
        page.views.clear()

        # Default view (home page)
        if page.route == '/':
            page.views.append(
                View(
                    '/',
                    [
                        AppBar(title=Text('App Flet'), bgcolor=colors.SURFACE_VARIANT),
                        ElevatedButton('Visitar la tienda', on_click=lambda _: page.go('/tienda')),
                        ElevatedButton('Visitar las materias', on_click=lambda _: page.go('/materias'))
                    ]
                )
            )

        # Tienda view
        elif page.route == '/tienda':
            page.views.append(
                View(
                    '/tienda',
                    [
                        AppBar(title=Text('Tienda'), bgcolor=colors.SURFACE_VARIANT),
                        ElevatedButton('Inicio', on_click=lambda _: page.go('/')),
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    "Range slider with divisions and labels",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Container(height=30)
                            ],
                        )
                    ]
                )
            )

        # Materias view
        elif page.route == '/materias':
            page.views.append(
                View(
                    '/materias',
                    [
                        AppBar(title=Text('Materias'), bgcolor=colors.SURFACE_VARIANT),
                        ElevatedButton('Inicio', on_click=lambda _: page.go('/')),
                        ElevatedButton('detalles', on_click=lambda _: page.go('/materias/detalles')),
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    "Puta_cola",  # This text can be changed
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Container(height=30)
                            ],
                        )
                    ]
                )
            )
            
        elif page.route == '/materias/detalles':
            page.views.append(
                View(
                    '/',
                    [
                        AppBar(title=Text('Juan_de_jesus/calculo'), bgcolor=colors.SURFACE_VARIANT),
                        ElevatedButton('materias', on_click=lambda _: page.go('/materias')),
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    "Puta_cola",  # This text can be changed
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Container(height=30)
                            ],
                        )
                    ]
                )
            )
        
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)

