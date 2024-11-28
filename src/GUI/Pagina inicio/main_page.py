import flet as ft

from professor_page_group_pages import ProfesorMainPage, ClassroomMainPage, GroupMainPage


import sys 
sys.path.append("src/GUI/Enrouter/")

import sys 
sys.path.append("src/GUI/Enrutador/")
sys.path.append("src/GUI/Pagina profesor/")
from prueba import EnrouterPage
from TMaterias import Bd

import flet as ft

from Professor_page import ProfessorsPage, ClassroomsPage, GroupsPage



# cada vez que se reinicia la base de datos, o se carga se deben, crear 6 paginas nuevas con 
# sus ciertas referencias
class Pages():
    
    def __init__(self,
                        professors_page,
                        classrooms_page,
                        groups_page):

    
        self.professors_page = professors_page
        self.classrooms_page = classrooms_page
        self.groups_page = groups_page
        
# falta un boton para regresar a la pagina principal

class MainPage():
    
    
    def __init__(self, bd, page) -> None:

        # Contenido inicial de cada sección
        
        def change_to_mainpage():
            enrouter_page.main_page = main_page
            enrouter_page.change_page('/')
            professor_page.update()
            #classroom_page.update()
            #group_page.update()
        
        professors_page = ProfessorsPage(bd, change_to_mainpage)
        classrooms_page = ClassroomsPage(bd, change_to_mainpage)
        groups_page = GroupsPage(bd, change_to_mainpage)  
        

        pages = Pages(
            professors_page,
            classrooms_page,
            groups_page
        )
        
        enrouter_page = EnrouterPage(page, pages)
        self.page = page
        self.bd = bd
        
        
        function_reference_change_to_page = enrouter_page.change_page
        professor_page = ProfesorMainPage(bd, function_reference_change_to_page)
        classroom_page = ClassroomMainPage(bd, function_reference_change_to_page)
        group_page = GroupMainPage(bd, function_reference_change_to_page)
        
        
        
        content = ft.Container(
            content= ft.Column([professor_page], alignment=ft.MainAxisAlignment.START, expand=True,
                        height=800,
                        width=600
                        ), 
            expand=True)


        # Callback para manejar los cambios de la NavigationRail
        def on_change(e):
            
            selected_index = e.control.selected_index
            
            # Cambiar el contenido basado en la selección
            if selected_index == 0:  # Profesor
                content.content = ft.Column([professor_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            height=800,
                                            width=600)
                professor_page.update()

            elif selected_index == 1:  # Aula
                content.content = ft.Column([classroom_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            height=800,
                                            width=600)
                classroom_page.update()

            elif selected_index == 2:  # Grupo
                content.content = ft.Column([group_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            height=800,
                                            width=60)
                group_page.update()

            content.update()        
            # Actualizar la página
            
            
        def cargar_base_datos(e):
            bd.load_db("/home/juan/Escritorio/DB.pickle")
            self.restart()
            professor_page.update()
            classroom_page.update()
            group_page.update()
            

        # Barra de navegación
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            leading=ft.Column(
                    controls = [ft.FloatingActionButton(icon=ft.icons.CREATE, 
                                            text="Print",
                                            on_click = lambda e: bd.generate_pdf("/home/juan/Escritorio", "puto")),
                                ft.FloatingActionButton(icon=ft.icons.SAVE, 
                                            text="Guargar",
                                            on_click = lambda e: bd.save_db("/home/juan/Escritorio", "DB")),
                                ft.FloatingActionButton(icon=ft.icons.CHARGING_STATION, 
                                            text="Cargar",
                                            on_click = lambda e: cargar_base_datos(e))
                    ]
                    ),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.FAVORITE_BORDER,
                    selected_icon=ft.icons.FAVORITE,
                    label="Profesor",
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                    selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                    label="Aula",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                    label_content=ft.Text("Grupo"),
                ),
            ],
            on_change=on_change,  # Llamar al callback
        )

        # Layout principal
        
        main_page = ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    content,  # Contenedor dinámico
                ],
                expand=True,
            )
        page.add(
            main_page
        )
        
    def restart(self):
        bd = self.bd
        page = self.page
         # Contenido inicial de cada sección
        self.bd = bd
        
        professors_page = ProfessorsPage(bd)
        classrooms_page = ClassroomsPage(bd)
        groups_page = GroupsPage(bd)  
        

        pages = Pages(
            professors_page,
            classrooms_page,
            groups_page
        )
        
        
        enrouter_page = EnrouterPage(page, pages)
        self.page = page
        self.bd = bd
        
        function_reference_change_to_page = enrouter_page.change_page
        professor_page = ProfesorMainPage(bd, function_reference_change_to_page)
        classroom_page = ClassroomMainPage(bd, function_reference_change_to_page)
        group_page = GroupMainPage(bd, function_reference_change_to_page)

        
        content = ft.Container(
            content= ft.Column([professor_page], alignment=ft.MainAxisAlignment.START, expand=True,
                        height=800,
                        width=600
                        ), 
            expand=True)


        # Callback para manejar los cambios de la NavigationRail
        def on_change(e):
            
            selected_index = e.control.selected_index
            
            # Cambiar el contenido basado en la selección
            if selected_index == 0:  # Profesor
                content.content = ft.Column([professor_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            height=800,
                                            width=600)
                professor_page.update()

            elif selected_index == 1:  # Aula
                content.content = ft.Column([classroom_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            height=800,
                                            width=600)
                classroom_page.update()

            elif selected_index == 2:  # Grupo
                content.content = ft.Column([group_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            height=800,
                                            width=60)
                group_page.update()

            content.update()        
            # Actualizar la página
            
        def cargar_base_datos(e):
            bd.load_db("/home/juan/Escritorio/DB.pickle")
            self.restart()
            professor_page.update()
            classroom_page.update()
            group_page.update()
            

        # Barra de navegación
        rail = ft.NavigationRail(
            selected_index=0,
            min_width=100,
            min_extended_width=400,
            label_type=ft.NavigationRailLabelType.ALL,
            leading=ft.Column(
                    controls = [ft.FloatingActionButton(icon=ft.icons.CREATE, 
                                            text="Add",
                                            on_click = lambda e: bd.generate_pdf("/home/juan/Escritorio", "puto")),
                                ft.FloatingActionButton(icon=ft.icons.SAVE, 
                                            text="Guargar",
                                            on_click = lambda e: self.bd.save_db("/home/juan/Escritorio", "DB")),
                                ft.FloatingActionButton(icon=ft.icons.CHARGING_STATION, 
                                            text="Cargar",
                                            on_click = lambda e: cargar_base_datos(e)),
                    ]
                    ),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.FAVORITE_BORDER,
                    selected_icon=ft.icons.FAVORITE,
                    label="Profesor",
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                    selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                    label="Aula",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                    label_content=ft.Text("Grupo"),
                ),
            ],
            on_change=on_change,  # Llamar al callback
        )
        
        page.controls.clear()
        
        page.add(
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    content,  # Contenedor dinámico,
                ],
                expand=True,
            )
        )
        page.update()


        
    



def main(page: ft.Page):
    
    MainPage(Bd, page)


ft.app(main)


# ? arreglar el problema de deslizamiento hacia abajo
# ! arreglar el caso de un tablero cuando no se tiene matterias
# ! arreglar el problema cuando no hay profesores, aulao grupos

