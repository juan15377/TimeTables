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
# MainPage es donde se puede se presentan las paginas principales
class MainPage(ft.Row):
    
    
    def __init__(self, bd, page) -> None:
        
        self.page = page
        self.restart(bd)
        #return None 

        
    def restart(self, bd):
        self.bd = bd
        page = self.page

 
        enrouter_page = EnrouterPage(self, self.bd, self.page)
        
        
        
        
        
        professor_page = ProfesorMainPage(self.bd, lambda route : enrouter_page.change_page(route))
        classroom_page = ClassroomMainPage(self.bd, lambda route : enrouter_page.change_page(route))
        group_page = GroupMainPage(self.bd, lambda route : enrouter_page.change_page(route))
        
        self.professor_page = professor_page
        self.classroom_page = classroom_page
        self.group_page = group_page
        
        
        content = ft.Container(
            content= ft.Column([professor_page], alignment=ft.MainAxisAlignment.START, expand=True,
                        ), 
            expand=True)
        
        #professor_page.update()


        # Callback para manejar los cambios de la NavigationRail
        def on_change(e):
            
            selected_index = e.control.selected_index
            
            # Cambiar el contenido basado en la selección
            if selected_index == 0:  # Profesor
                content.content = ft.Column([professor_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            height=800,
                                            width=600,
                                            )
                professor_page.update(update= False)

            elif selected_index == 1:  # Aula
                content.content = ft.Column([classroom_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            height=800,
                                            width=600)
                classroom_page.update(update = False)

            elif selected_index == 2:  # Grupo
                content.content = ft.Column([group_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            height=800,
                                            width=60)
                group_page.update(update = False)

            content.update()        
            # Actualizar la página
            
            
        # Pick files dialog
        def load_db(e: FilePickerResultEvent):
            selected_files.value = (
                ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
            )
            self.bd.load_db(e.files[0].path)
            professor_page.update(update = False)
            classroom_page.update(update = False)
            group_page.update(update = False)
            enrouter_page.update_db(self.bd)
            self.restart(self.bd)
            content.update()
            
            

        pick_files_load_bd = FilePicker(on_result=load_db)
        selected_files = Text()

        # Save file dialog
        def save_db(e: FilePickerResultEvent):
            save_file_path.value = e.path if e.path else "Cancelled!"
            self.bd.save_db(e.path)
            #save_file_path.update()

        pick_file_save_db = FilePicker(on_result=save_db)
        save_file_path = Text()

        # Open directory dialog
        def printer_db(e: FilePickerResultEvent):
            directory_path.value = e.path if e.path else "Cancelled!"
            if e.path:
                self.bd.generate_pdf(e.path)
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
                    controls = [ft.FloatingActionButton(icon=ft.icons.PALETTE, 
                                            text="Print",
                                            on_click = lambda e: pick_file_printer.save_file(),
                                            width=100
                                            ),
                                ft.FloatingActionButton(icon=ft.icons.SAVE, 
                                            text="Guargar",
                                            on_click = lambda e:  pick_file_save_db.save_file(),
                                            width=100
                                            ),
                                ft.FloatingActionButton(icon=ft.icons.DOWNLOAD_ROUNDED, 
                                            text="Cargar",
                                            on_click = lambda e: pick_files_load_bd.pick_files(),
                                            width=100
                                            )
                    ]
                    ),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.SCHOOL,
                    selected_icon=ft.icons.SCHOOL,
                    label="Profesor",
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.BOOKMARK),
                    selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                    label="Aula",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PEOPLE,
                    selected_icon_content=ft.Icon(ft.icons.PEOPLE),
                    label_content=ft.Text("Grupo"),
                ),
            ],
            on_change=on_change,  # Llamar al callback
            #expand=True
        )
        
        self.rail = rail
        
        

        # Layout principal
        
        
        
        super().__init__(
             controls = [
                rail,
                ft.VerticalDivider(width=2),
                content
            ],
            expand = True
        )
    
        enrouter_page.main_page = self
        
        
        
    #function to update page in cual 
    def update(self, update = False):
        
        selected_index = self.rail.selected_index
        
        if selected_index == 0:
            self.professor_page.update(update)
        elif selected_index == 1:
            self.classroom_page.update(update)
        elif selected_index == 2:
            self.group_page.update(update)
        

# al momento de agregar una materia todos los bloques que se colocaron dentro de el deben actualizarsede
        
# al momento de eliminar una materia todos los bloques que se colocaron dentro de el deben actualizarse


def main(page: ft.Page):
    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.BLUE
        )
    Bd = BD()
    
    main_page = MainPage(Bd, page)
    
    page.add(
        main_page
    )
    




# ? arreglar el problema de deslizamiento hacia abajo
# ! arreglar el caso de un tablero cuando no se tiene matterias
# ! arreglar el problema cuando no hay profesores, aulao grupos

