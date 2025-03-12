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
    _instance = None
    
    def __new__(cls, page: ft.Page, query):
        if cls._instance is None:
            cls._instance = super(HomePage, cls).__new__(cls)
            cls._instance.__initialized = False
        else:
            cls._instance.update()
        return cls._instance
    
    def __init__(self, page: ft.Page, query) -> None:
        if self.__initialized:
            return
        self.__initialized = True
        
        self.save_path_default = None
        self.page = page
        layout = self.get_layout()
        
        super().__init__(
            content=layout,
            expand=True
        )
        
    def get_layout(self):
        professor_page = ProfessorHomePage(self.page)
        classroom_page = ClassroomHomePage(self.page)
        group_page = GroupHomePage(self.page)
        
        self.professor_page = professor_page
        self.classroom_page = classroom_page
        self.group_page = group_page
        
        content_PCG = ft.AnimatedSwitcher(
            content=ft.Column([professor_page], alignment=ft.MainAxisAlignment.START, expand=True),
            expand=True,
            transition=ft.AnimatedSwitcherTransition.SCALE,
            duration=200,
            reverse_duration=100,
            switch_in_curve=ft.AnimationCurve.EASE_IN,
            switch_out_curve=ft.AnimationCurve.EASE_IN_EXPO,
        )
        
        self.content_PCG = content_PCG
    
        def on_change(e):
            selected_index = e.control.selected_index
            before_selected = e.control.data 

            if int(before_selected) == int(selected_index):
                return None
            
            e.control.data = selected_index
            del content_PCG.content.controls[0]
            
            if selected_index == 0:
                content_PCG.content = ft.Column([professor_page], alignment=ft.MainAxisAlignment.START, expand=True)
                professor_page.update(update_search=False)
            elif selected_index == 1:
                content_PCG.content = ft.Column([classroom_page], alignment=ft.MainAxisAlignment.START, expand=True)
                self.classroom_page.update(update_search=False)
            elif selected_index == 2:
                content_PCG.content = ft.Column([group_page], alignment=ft.MainAxisAlignment.START, expand=True)
                self.group_page.update(update_search=False)
                
            self.content_PCG.update()
            self.update(update=True)   
        
        pick_files_load_bd = FilePicker(on_result=self.load_database)
        selected_files = Text()

        pick_file_save_db = FilePicker(on_result=self.save_database)
        save_file_path = Text()
        
        pick_file_printer = FilePicker(on_result=self.export_database)
        directory_path = Text()
        
        self.page.overlay.extend([pick_files_load_bd, pick_file_save_db, pick_file_printer])

        rail = ft.NavigationRail(
            data=0,
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            leading=ft.Column(
                controls=[
                    ft.FloatingActionButton(icon=ft.icons.PALETTE, text="Export", on_click=lambda e: self.page.go("/EXPORT_SCHEDULE"), width=100),
                    ft.FloatingActionButton(icon=ft.icons.SAVE, text="Guardar", on_click=lambda e: pick_file_save_db.save_file(), width=100),
                    ft.FloatingActionButton(icon=ft.icons.DOWNLOAD_ROUNDED, text="Cargar", on_click=lambda e: pick_files_load_bd.pick_files(), width=100),
                ]
            ),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.SCHOOL, size=30), selected_icon_content=ft.Icon(ft.icons.SCHOOL, size=40), label="Profesor"),
                ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.BOOKMARK, size=30), selected_icon_content=ft.Icon(ft.icons.BOOKMARK, size=40), label="Aula"),
                ft.NavigationRailDestination(icon_content=ft.Icon(ft.icons.PEOPLE, size=30), selected_icon_content=ft.Icon(ft.icons.PEOPLE, size=40), label_content=ft.Text("Grupo")),
            ],
            on_change=on_change,
            expand=False
        )
        
        self.rail = rail
        
        layout = ft.Row(
            controls=[rail, ft.VerticalDivider(width=2), content_PCG],
            expand=True
        )
        
        return ft.Container(layout)
    
    def update(self, update=False):
        selected_index = self.rail.selected_index
        if selected_index == 0:
            self.professor_page.update(update_search=True)
        elif selected_index == 1:
            self.classroom_page.update(update_search=True)
        elif selected_index == 2:
            self.group_page.update(update_search=True)
    
    def load_database(self, e: FilePickerResultEvent):
        path_load = e.files[0].path
        self.load_db(path_load)
    
    def save_database(self, e: FilePickerResultEvent):
        path_save = e.path
        self.save_db(path_save)
    
    def export_database(self, e: FilePickerResultEvent):
        print_path = e.path
        self.print_db(print_path)
    
    def load_db(self, path_load):
        self.save_path_default = path_load
        self.db.load_db(path_load)
        self.enrouter_page.update_db(self.db)
        new_layout = self.get_layout()
        
        self.content = new_layout
        self.update()
        self.page.update()
    
    def save_db(self, path_save):
        self.save_path_default = path_save
        self.db.save_db(path_save)
    
    def print_db(self, path_print):
        self.db.export.complete_schedule(path_print)
    
    def update_professor(self):
        self.professor_page.update(update=False)
