import flet as ft
from .components import ProfessorHomePage, ClassroomHomePage, GroupHomePage
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
    FilePicker,
    FilePickerResultEvent
)

from src.models.database import *
from src.UI.database import database
from src.UI.components import alerts 


class HomePage(ft.Container):
    
    
    def __init__(self, page, query) -> None:
        
        self.save_path_default = None
        self.page = page
        layout = self.get_layout()
        
        super().__init__(
            content = layout,
            expand = True
        )
                
        #return None 
        
    def get_layout(self):
        # contenido de la pagina principal
        
        professor_page = ProfessorHomePage()
        classroom_page = ClassroomHomePage()
        group_page = GroupHomePage()
        
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
        def load_database(e: FilePickerResultEvent):
            path_load = e.files[0].path
            self.load_database(path_load)
    

        pick_files_load_bd = FilePicker(on_result=load_database)
        selected_files = Text()

        # Save file dialog
        def save_database(e: FilePickerResultEvent):
            path_save = e.path
            self.save_database(path_save)
            

        pick_file_save_db = FilePicker(on_result = save_database)
        save_file_path = Text()
        

        # Open directory dialog
        def export_database(e: FilePickerResultEvent):
            print_path = e.path
            self.print_db(print_path)


        pick_file_printer = FilePicker(on_result=export_database)
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
            expand=True
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
        
        
        return ft.Container(professor_page)
   
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