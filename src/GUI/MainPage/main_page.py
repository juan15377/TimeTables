import flet as ft
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)


from src.Logic.Bd import BD
from src.GUI.EnrouterPage import EnrouterPage
from src.Logic.Professor_Classroom_Group import *
from src.GUI.MainPage.professor_page_group_pages import *
from src.GUI.Professors_classrooms_groups_pages.prof_class_gro_pages import *

from flet import FilePicker, FilePickerResultEvent



def preload_database(page):
    pass

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
            classroom_page.update()
            group_page.update()
            self.page.update()
            
            
        def reference_to_add_subject_professors():
            enrouter_page.navigate_to_new_subject(lambda : enrouter_page.change_page("/PROFESSORS"))
            
        def reference_to_add_subject_classrooms():
            enrouter_page.navigate_to_new_subject(lambda :enrouter_page.change_page('/CLASSROOMS'))
            
        def reference_to_add_subject_groups():
            enrouter_page.navigate_to_new_subject(lambda : enrouter_page.change_page('/GROUPS'))
        
        professors_page = ProfessorsPage(bd, change_to_mainpage, reference_to_add_subject_professors)
        classrooms_page = ClassroomsPage(bd, change_to_mainpage, reference_to_add_subject_classrooms)
        groups_page = GroupsPage(bd, change_to_mainpage, reference_to_add_subject_groups)  
        

        pages = Pages(
            professors_page,
            classrooms_page,
            groups_page
        )
        
        enrouter_page = EnrouterPage(page, pages, bd)
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
            
            
        def cargar_base_datos():
            self.bd.load_db(page)
            self.restart()
            professor_page.update()
            classroom_page.update()
            group_page.update()
            #self.page.update()
            
        def guardar_base_de_datos():
            self.bd.save_db(self.page)
            
        def imprimir_horario():
            self.bd.generate_pdf(self.page)
            
            

        # Barra de navegación
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            leading=ft.Column(
                    controls = [ft.FloatingActionButton(icon=ft.icons.DATA_OBJECT, 
                                            text="Print",
                                            on_click = lambda e: imprimir_horario()),
                                ft.FloatingActionButton(icon=ft.icons.SAVE, 
                                            text="Guargar",
                                            on_click = lambda e: guardar_base_de_datos()),
                                ft.FloatingActionButton(icon=ft.icons.CHARGING_STATION, 
                                            text="Cargar",
                                            on_click = lambda e: cargar_base_datos())
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
        
        
        
        def change_to_mainpage():
            enrouter_page.main_page = main_page
            enrouter_page.change_page('/')
            professor_page.update()
            classroom_page.update()
            group_page.update()
            self.page.update()
            
            
            
        def reference_to_add_subject_professors():
            enrouter_page.navigate_to_new_subject(lambda : enrouter_page.change_page("/PROFESSORS"))
            
        def reference_to_add_subject_classrooms():
            enrouter_page.navigate_to_new_subject(lambda :enrouter_page.change_page('/CLASSROOMS'))
            
        def reference_to_add_subject_groups():
            enrouter_page.navigate_to_new_subject(lambda : enrouter_page.change_page('/GROUPS'))
        
        professors_page = ProfessorsPage(bd, change_to_mainpage, reference_to_add_subject_professors)
        classrooms_page = ClassroomsPage(bd, change_to_mainpage, reference_to_add_subject_classrooms)
        groups_page = GroupsPage(bd, change_to_mainpage, reference_to_add_subject_groups)  
        

        pages = Pages(
            professors_page,
            classrooms_page,
            groups_page
        )
        
        enrouter_page = EnrouterPage(page, pages, bd)
        
        
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
            
            
        def cargar_base_datos():
            file_path =  get_file_path(self.page)
            self.bd.load_db(file_path)
            self.restart()
            professor_page.update()
            classroom_page.update()
            group_page.update()
            self.page.update()
            
        def guardar_base_de_datos():
            save_path = create_file_path(self.page)
            self.bd.save_db(save_path)
            
        def imprimir_horario():
            save_path = create_file_path(self.page)
            self.bd.generate_pdf(save_path)
            
            

        # Barra de navegación
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            leading=ft.Column(
                    controls = [ft.FloatingActionButton(icon=ft.icons.DATA_OBJECT, 
                                            text="Print",
                                            on_click = lambda e: imprimir_horario()),
                                ft.FloatingActionButton(icon=ft.icons.SAVE, 
                                            text="Guargar",
                                            on_click = lambda e: guardar_base_de_datos()),
                                ft.FloatingActionButton(icon=ft.icons.CHARGING_STATION, 
                                            text="Cargar",
                                            on_click = lambda e: cargar_base_datos())
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
        page.controls.clear()
        page.views.clear()
        
        page.add(main_page)
        page.update()


        
# al momento de eliminar una materia todos los bloques que se colocaron dentro de el deben actualizarse



def main(page: ft.Page):
    
    Bd = BD()
    
    MainPage(Bd, page)


ft.app(main)


# ? arreglar el problema de deslizamiento hacia abajo
# ! arreglar el caso de un tablero cuando no se tiene matterias
# ! arreglar el problema cuando no hay profesores, aulao grupos

