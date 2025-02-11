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


from src.models.database import DataBaseManager
from src.GUI.EnrouterPage import EnrouterPage
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

# la primera pagina sera algo inmutable



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
        

class Data:
    def __init__(self) -> None:
        self.counter = 0

        
class AlertChangesSave():
    

    def __init__(self, page, save_path):
        d = Data()
        page.snack_bar = ft.SnackBar(
        content=ft.Text("New Subject Created"),
        action="Alright!",
        )
    
        
        def on_click():
            page.snack_bar = ft.SnackBar(ft.Text(f"save changes in {save_path}"),
                                         bgcolor=ft.colors.GREEN_200)
            page.snack_bar.open = True
            d.counter += 1
            page.update()
        
        self.show = lambda : on_click()


class MainPage(ft.Container):
    
    
    def __init__(self, bd, page) -> None:
        
        self.page = page
        self.db = bd
        self.save_path_default = None
        self.enrouter_page = EnrouterPage(self, self.db, self.page)
        
        
        layout = self.get_layout(self.db)
        
        
        
        super().__init__(
            content = layout,
            expand = True
        )
                
        #return None 
        
    def get_layout(self, bd):
        self.db = bd
        # contenido de la pagina principal
        
        professor_page = ProfesorMainPage(self.db, lambda route : self.enrouter_page)
        classroom_page = ClassroomMainPage(self.db, lambda route : self.enrouter_page)
        group_page = GroupMainPage(self.db, lambda route : self.enrouter_page)
        
        self.professor_page = professor_page
        self.classroom_page = classroom_page
        self.group_page = group_page
        
        
        content_PCG =  ft.AnimatedSwitcher(
            content= ft.Column([professor_page], alignment=ft.MainAxisAlignment.START, expand=True,
                        ),
            expand=True,
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=200,
            reverse_duration=100,
            switch_in_curve=ft.AnimationCurve.EASE_IN,
            switch_out_curve=ft.AnimationCurve.EASE_IN_EXPO,
        )
        
        self.content_PCG = content_PCG
        
        
        def auto_save_file():
            if self.save_path_default is not None:
                self.db.save_db(self.save_path_default)
                alert_changes_save = AlertChangesSave(self.page, self.save_path_default)
                alert_changes_save.show()
                return None
            

        def on_keyboard(e: ft.KeyboardEvent):
            if e.key == "S" and e.ctrl:
                auto_save_file()
        
        self.page.on_keyboard_event = on_keyboard
        

        def on_change(e):
            # parche que se debe arreglar para que funcione de igual manera
            selected_index = e.control.selected_index
            before_selected = e.control.data 

            if int(before_selected) == int(selected_index):
                return None
            
            e.control.data = selected_index

            # Cambiar el contenido basado en la selección
            del content_PCG.content.controls[0]
            
            if selected_index == 0:  # Profesor
                content_PCG.content = ft.Column([professor_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            )
                professor_page.update(update = False)

            elif selected_index == 1:  # Aula
                content_PCG.content = ft.Column([classroom_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            )
                self.classroom_page.update(update = False)

            elif selected_index == 2:  # Grupo
                content_PCG.content = ft.Column([group_page], alignment=ft.MainAxisAlignment.START, expand=True,
                                            )
                self.group_page.update(update = False)

            self.page.update() 
            self.update(update = True)   
        
        
        # Pick files dialog
        def load_db(e: FilePickerResultEvent):
            path_load = e.files[0].path
            self.load_db(path_load)
    

        pick_files_load_bd = FilePicker(on_result=load_db)
        selected_files = Text()

        # Save file dialog
        def save_db(e: FilePickerResultEvent):
            path_save = e.path
            self.save_db(path_save)
            

        pick_file_save_db = FilePicker(on_result = save_db)
        save_file_path = Text()
        

        # Open directory dialog
        def printer_db(e: FilePickerResultEvent):
            print_path = e.path
            self.print_db(print_path)


        pick_file_printer = FilePicker(on_result=printer_db)
        directory_path = Text()
        
        
        self.page.overlay.extend([pick_files_load_bd, pick_file_save_db, pick_file_printer])


        # Barra de navegación
        rail = ft.NavigationRail(
            data = 0,
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
                                            ),
                    ]
                    ),
            
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.SCHOOL, size = 30),
                    selected_icon_content=ft.Icon(ft.icons.SCHOOL, size = 40),
                    label="Profesor",
                    
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.BOOKMARK, size = 30),
                    selected_icon_content=ft.Icon(ft.icons.BOOKMARK, size = 40),
                    label="Aula",
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.PEOPLE, size = 30),
                    selected_icon_content=ft.Icon(ft.icons.PEOPLE, size = 40),
                    label_content=ft.Text("Grupo"),
                ),
            ],
            on_change=on_change,  # Llamar al callback
            #expand=True
        )
        
        self.rail = rail
        
        layout = ft.Row(
            controls = [
                rail,
                ft.VerticalDivider(width=2),
                content_PCG
            ],
            expand = True
        )
        
        
        return layout
   
        pass
        
    #function to update page in cual 
    def update(self, update = False):
        
        selected_index = self.rail.selected_index
        
        if selected_index == 0:
            self.professor_page.update(update)
        elif selected_index == 1:
            self.classroom_page.update(update)
        elif selected_index == 2:
            self.group_page.update(update)
        

    
    def load_db(self, path_load):
        self.save_path_default = path_load
        self.db.load_db(path_load)
        self.enrouter_page.update_db(self.db)
        new_layout = self.get_layout(self.db)
        
        self.content = new_layout
        self.update()
        self.page.update()
        
        pass
    
    
    def save_db(self, path_save):
        self.save_path_default = path_save # se pone predeterminado esta path si se quiere guardar
        self.db.save_db(path_save)
        pass 
    
    
    def print_db(self, path_print):
        self.db.export.complete_schedule(path_print)
        
    def update_professor(self):
        self.professor_page.update(update = False)
        

# al momento de agregar una materia todos los bloques que se colocaron dentro de el deben actualizarsede
        
# al momento de eliminar una materia todos los bloques que se colocaron dentro de el deben actualizarse


def main(page: ft.Page):
    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.BLUE
        )
    Bd = DataBaseManager()
    
    page.theme_mode = "dark"
    main_page = MainPage(Bd, page)
    
    page.add(
        main_page
    )
    

# ? arreglar el problema de deslizamiento hacia abajo
# ! arreglar el caso de un tablero cuando no se tiene matterias
# ! arreglar el problema cuando no hay profesores, aulao grupos

