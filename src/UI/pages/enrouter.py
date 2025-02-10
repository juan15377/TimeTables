import sys
import flet as ft
from flet import View

from src.models.database import *
from .resource_pcg import EditorPCG
from .list_professors_classrooms_groups import ProfessorsPage, ClassroomsPage, GroupsPage
from .subject import SubjectEditor


def load_subjects_page(bd, page_to_route, page):
    subject_editor = SubjectEditor(bd, reference_page_router = page_to_route, page = page)
    return subject_editor
    pass


#/main/juan_de_jesus/calculo/

# En el enrouter deben cargarse las 3 paginas principales
# de una vez se incorporara la funcionalidad de poder editar una materia 




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
# se necesita cambiar la estrcutura de enrutamiento por que ya llevo mas de 20 horas buscando un error, lo que indica que 
# al codigo le falta estrcuturacion, la referencia de la base de datos actualizada la tendra el enrouterpage

# existira una main_page, que esta tambien esta ligada a una base de datos, 

# Enrouter_page("/") -> Main_page
# Enrouter_page("/CLASSROOMS") -> Classrooms_page
# Enrouter_page("/PROFESSORS") -> Professors_page
# Enrouter_page("/GROUPS") -> Groups_page
# Enrouter_page("/CLASSROOMS/SUBJECT_DETAILS") -> Subject_edit with reference to back in /CLASSROOMS 

# se debe tener una base de las paginas, si pasa un simple contenedor como pagina, esta debe pasar ese,




class Pages():
    
    def __init__(self,
                        professors_page,
                        classrooms_page,
                        groups_page, 
                        main_page):

    
        self.professors_page = professors_page
        self.classrooms_page = classrooms_page
        self.groups_page = groups_page
        self.main_page = main_page

class EnrouterPCG():
    
    def __init__(self, db, enrouter_page):
        
        self.db = db 
        self.enrouter_page = enrouter_page
        pass 

    def change_page(self, pcg):
        content_page = None 
        
        if type(pcg) == Professor:
            content_page = EditorPCG(pcg, self.db, self.enrouter_page)            
        elif type(pcg) == Classroom:
            content_page = EditorPCG(pcg, self.db, self.enrouter_page)
        else:
            content_page = EditorPCG(pcg, self.db, self.enrouter_page)
        self.enrouter_page.load_page_content(content_page)
        pass 

class SubjectPagesManager():
    
    def __init__(db, page_manager):
        pass  
    
    def load_editor(subject):
        pass  
    
    def load_new():
        
        pass 









class PageManager():
    
    def __init__(self, bd, pages, page_container : ft.Container) -> None:
        self.pages = pages
        self.db = bd
        self.page_container = page_container
        self.pcg = EnrouterPCG(self.db, self)
        self.subject = SubjectPagesManager(db, self)
        
    def change_page(self, route, subject=False, pcg=False):
        # Diccionario de rutas y sus correspondientes páginas
        routes = {
            '/PROFESSORS': self.pages.professors_page,
            '/CLASSROOMS': self.pages.classrooms_page,
            '/GROUPS': self.pages.groups_page,
            '/': self.pages.main_page
        }

        # Verificar si la ruta está en el diccionario
        if route in routes:
            page_content = routes[route]
            page_content.update(update=False)
        
        # Rutas con detalles de la materia
        elif route in ['/PCG/SUBJECT_DETAILS', '/PROFESSORS/SUBJECT_DETAILS', '/CLASSROOMS/SUBJECT_DETAILS', '/GROUPS/SUBJECT_DETAILS']:
            page_back_callback = lambda: self.change_page(route.split('/')[1])  # Genera la ruta de retorno
            page_content = load_subjects_page(self.db, page_back_callback, self.page)
        
        # Cargar la página de contenido
        self.load_page_content(page_content)
        

    def update_db(self, bd):
        self.db = bd
        print(len(self.db.professors.get()))
        professors_page = ProfessorsPage(self.db, 
                                         self)
        
        classrooms_page = ClassroomsPage(self.db, 
                                         self)
        
        groups_page = GroupsPage(self.db, 
                                 self)
        
        self.pages = Pages(professors_page, classrooms_page, groups_page)
        pass


    def load_page_content(self, page_content):
        
        self.page.controls[0]=page_content
            
        self.page.update()
        
    
    def navigate_to_new_subject(self, page_to_route, page):
        page_content = load_subjects_page(self.bd, page_to_route, page)
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