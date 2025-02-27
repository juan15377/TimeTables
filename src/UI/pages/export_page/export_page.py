import flet as ft 
from src.UI.database import database
from .components import ExportScheduleGrid, ItemSelectionPanel

class ExportPage(ft.Container):
    
    def __init__(self, page, query):
        
        def on_selected(pcg):
            self.container_export_schedule_grid.content = ExportScheduleGrid(pcg)
            self.container_export_schedule_grid.update()
            pass
        
        self.container_export_schedule_grid = ft.Container(
                            content =  ExportScheduleGrid(), 
                            expand = True)
        
        self.item_selection_panel = ItemSelectionPanel(
            page,
            database.professors.get(),
            database.classrooms.get(),
            database.groups.get(),
            on_selected=on_selected,
        )
        
        
        layout = ft.Row(
            controls = [
                self.item_selection_panel,
                self.container_export_schedule_grid,
            ],
            expand=True
        )
        
        super().__init__(
            content = layout,
            expand = True
        )
        pass
    
    
    