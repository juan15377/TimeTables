import flet as ft
from flet import View

import sys 

sys.path.append("src/GUI/SubjectEditor/")

from subject_editor import SubjectEditor

def load_subjects_page(bd, page_to_route):
    subject_editor = SubjectEditor(bd, reference_page_router = page_to_route)
    return subject_editor
    pass


#/main/juan_de_jesus/calculo/

# En el enrouter deben cargarse las 3 paginas principales





ROUTE_PROFESSOR = '/PROFESSORS'
ROUTE_CLASSROOM = '/CLASSROOMs'
ROUTE_SUBJECTS = '/GROUPS'
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
class EnrouterPage():
    
    
    def __init__(self, page, pages, bd) -> None:
        page.title = "TimeTables"
        self.main_page = None
        self.pages = pages
        self.page =  page
        self.bd = bd
        
        
    def change_page(self,route):
        
        if route == '/PROFESSORS':
            page_content = self.pages.professors_page
            self.pages.professors_page.update(update = False)
        elif route == '/CLASSROOMS':
            page_content = self.pages.classrooms_page
            self.pages.classrooms_page.update(update = False)
        elif route == '/GROUPS':
            page_content = self.pages.groups_page
            self.pages.groups_page.update(update = False)
        elif route == '/':
            page_content = self.main_page
        self.load_page_content(page_content)  
  



    def load_page_content(self, page_content):
        
        self.page.views.clear()
        
        
        self.page.views.append(View('hola',
                                   controls = [page_content]))
            
        self.page.update()
        
    
    def navigate_to_new_subject(self, page_to_route):
        page_content = load_subjects_page(self.bd, page_to_route)
        self.load_page_content(page_content)
        
        pass 
    
    def navigate_to_new_professor(self):
        pass
    
    def navigate_to_lassrooms(self, classroom):
        pass
    
    def navigate_to_groups(self, group):
        pass  
    
    def navigate_to_subject(self, subject):# in the subject 
        pass
    
#
#
#def main(page: Page):
#    page.title = 'Ejemplo de Rutas'
#
#    def route_change(route):
#        page.views.clear()
#
#        # Default view (home page)
#        if page.route == '/':
#            page.views.append(
#                View(
#                    '/',
#                    [
#                        AppBar(title=Text('App Flet'), bgcolor=colors.SURFACE_VARIANT),
#                        ElevatedButton('Visitar la tienda', on_click=lambda _: page.go('/tienda')),
#                        ElevatedButton('Visitar las materias', on_click=lambda _: page.go('/materias'))
#                    ]
#                )
#            )
#
#        # Tienda view
#        elif page.route == '/tienda':
#            page.views.append(
#                View(
#                    '/tienda',
#                    [
#                        AppBar(title=Text('Tienda'), bgcolor=colors.SURFACE_VARIANT),
#                        ElevatedButton('Inicio', on_click=lambda _: page.go('/')),
#                        ft.Column(
#                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                            controls=[
#                                ft.Text(
#                                    "Range slider with divisions and labels",
#                                    size=20,
#                                    weight=ft.FontWeight.BOLD,
#                                ),
#                                ft.Container(height=30)
#                            ],
#                        )
#                    ]
#                )
#            )
#
#        # Materias view
#        elif page.route == '/materias':
#            page.views.append(
#                View(
#                    '/materias',
#                    [
#                        AppBar(title=Text('Materias'), bgcolor=colors.SURFACE_VARIANT),
#                        ElevatedButton('Inicio', on_click=lambda _: page.go('/')),
#                        ElevatedButton('detalles', on_click=lambda _: page.go('/materias/detalles')),
#                        ft.Column(
#                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                            controls=[
#                                ft.Text(
#                                    "Puta_cola",  # This text can be changed
#                                    size=20,
#                                    weight=ft.FontWeight.BOLD,
#                                ),
#                                ft.Container(height=30)
#                            ],
#                        )
#                    ]
#                )
#            )
#            
#        elif page.route == '/materias/detalles':
#            page.views.append(
#                View(
#                    '/',
#                    [
#                        AppBar(title=Text('Juan_de_jesus/calculo'), bgcolor=colors.SURFACE_VARIANT),
#                        ElevatedButton('materias', on_click=lambda _: page.go('/materias')),
#                        ft.Column(
#                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                            controls=[
#                                ft.Text(
#                                    "Puta_cola",  # This text can be changed
#                                    size=20,
#                                    weight=ft.FontWeight.BOLD,
#                                ),
#                                ft.Container(height=30)
#                            ],
#                        )
#                    ]
#                )
#            )
#        
#        page.update()
#
#    def view_pop(view):
#        page.views.pop()
#        top_view = page.views[-1]
#        page.go(top_view.route)
#    
#    page.on_route_change = route_change
#    page.on_view_pop = view_pop
#    page.go(page.route)
#
#
#ft.app(target=main)
#
#