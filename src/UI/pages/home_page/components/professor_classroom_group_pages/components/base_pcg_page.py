import flet as ft
from src.UI.database import database
from src.UI.State import global_state 
from typing import Callable, Any
from src.models.database import PCG, DEFAULT_PCG
from src.UI.components.subjects_schedule_grid import SubjectScheduleGrid
from src.UI.components.search_bar_items import SearchBarItems


class BasePCGPage(ft.Container):
    def __init__(self, page, refresh_values : Callable,  value = DEFAULT_PCG):
        self.page = page
        
        def change_item():
            selected = self.search_values.get_value()
            self.load_item(selected) # al momento de cambiar de elemento, esto cambia el valor en BasePCGPage
            
        search_values = SearchBarItems(
            refresh_values(),
            refresh_values,
            on_change = change_item
        )
        
        self.search_values = search_values
        self.refresh_values = refresh_values
        self.value = value
                                
        self.layout = self.get_layout()
        
        super().__init__(
            content = ft.Row(
                controls = [self.layout],
                expand=True
            ),
            expand=True,
        )
        
        
    def get_layout(self):
                        
        def change_value():
            selected = self.search_values.get_value()
            self.load_item(selected)
            
        button_reset_subjects = ft.FloatingActionButton(
            icon=ft.icons.REFRESH,
            on_click=lambda e: print("10"),
            text = "Gestionar datos",
            focus_elevation= 10,
        )
        
        self.schedule_grid = SubjectScheduleGrid(self.page, self.value)
                
        layout = ft.Column(
            controls = [
                    ft.Row(
                        controls = [
                                    self.search_values,
                                    button_reset_subjects
                        ],
                    ),
                    ft.Row(
                        controls = [      
                            self.schedule_grid,
                        ],
                        expand = True
                    )
                    ],
                expand=True,
                spacing=20,
            )
        
        return layout 
                
        
    def load_item(self, value : PCG):
        self.value = value
        self.update_schedule_grid(value, update_in_page=True)
        self.search_values.update()
        
        
    def update(self, update_search = False, update_in_page = False):
        
        self.update_schedule_grid(self.value, update_in_page = update_in_page)
       
        if update_search:
            #super().update()  
            self.search_values.update()
            
    def update_schedule_grid(self, new_value : PCG, update_in_page = False):
        self.schedule_grid = SubjectScheduleGrid(self.page, new_value)
        self.layout.controls[1].controls = [self.schedule_grid]
        
        if update_in_page:
            self.layout.controls[1].update()
        
       
