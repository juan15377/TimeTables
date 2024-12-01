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

from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)


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
        
        self.page = page
        self.bd = bd
        self.restart()
        #return None 

        
    def restart(self):
        
        page = self.page
        bd = self.bd
     
        def change_to_mainpage():
            enrouter_page.main_page = main_page
            enrouter_page.change_page('/')
            professor_page.update()
            classroom_page.update()
            group_page.update()
            
            
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
        
        enrouter_page = EnrouterPage(self.page, pages, bd)
        self.page = page
        self.bd = bd
        
        
        function_reference_change_to_page = enrouter_page.change_page
        professor_page = ProfesorMainPage(self.bd, function_reference_change_to_page)
        classroom_page = ClassroomMainPage(self.bd, function_reference_change_to_page)
        group_page = GroupMainPage(self.bd, function_reference_change_to_page)
        
        
        
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
            
            
        # Pick files dialog
        def load_db(e: FilePickerResultEvent):
            selected_files.value = (
                ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
            )
            print("BHJHGFDCFVGBHNJKMLGFDFGVHBJNKMLJGFCDXSDCFGVHBJNKM")
            self.bd.load_db(e.files[0].path)
            professor_page.update()
            classroom_page.update()
            group_page.update()
            self.restart()
            #selected_files.update()
            print("Cargar base de datos")

        pick_files_load_bd = FilePicker(on_result=load_db)
        selected_files = Text()

        # Save file dialog
        def save_db(e: FilePickerResultEvent):
            save_file_path.value = e.path if e.path else "Cancelled!"
            self.bd.save_db(e.path)
            print("Guardar Base de Datos")
            #save_file_path.update()

        pick_file_save_db = FilePicker(on_result=save_db)
        save_file_path = Text()

        # Open directory dialog
        def printer_db(e: FilePickerResultEvent):
            directory_path.value = e.path if e.path else "Cancelled!"
            if e.path:
                self.bd.generate_pdf(e.path)
            print("imprimir Base de datos")
            #directory_path.update()

        pick_file_printer = FilePicker(on_result=printer_db)
        directory_path = Text()

        # hide all dialogs in overlay
        self.page.overlay.extend([pick_files_load_bd, pick_file_save_db, pick_file_printer])

        # Barra de navegación
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            leading=ft.Column(
                    controls = [ft.FloatingActionButton(icon=ft.icons.DATA_OBJECT, 
                                            text="Print",
                                            on_click = lambda e: pick_file_printer.save_file(
                        )),
                                ft.FloatingActionButton(icon=ft.icons.SAVE, 
                                            text="Guargar",
                                            on_click = lambda e:  pick_file_save_db.save_file()),
                                ft.FloatingActionButton(icon=ft.icons.CHARGING_STATION, 
                                            text="Cargar",
                                            on_click = lambda e: pick_files_load_bd.pick_files(
                        ),)
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
        page.add(
            main_page
        )
        


        
# al momento de eliminar una materia todos los bloques que se colocaron dentro de el deben actualizarse



def main(page: ft.Page):
    
    Bd = BD()
    
    MainPage(Bd, page)




# ? arreglar el problema de deslizamiento hacia abajo
# ! arreglar el caso de un tablero cuando no se tiene matterias
# ! arreglar el problema cuando no hay profesores, aulao grupos

