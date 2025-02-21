import flet as ft 
from src.UI.database import database
from .components import ExportScheduleGrid, ItemSelectionPanel

class ExportPage(ft.Container):
    
    def __init__(self, page, query):
        
        self.export_schedule_grid = ExportScheduleGrid()
        self.item_selection_panel = ItemSelectionPanel(
            database.professors.get(),
            database.classrooms.get(),
            database.groups.get()
        )
        
        
        layout = ft.Row(
            controls = [
                self.export_schedule_grid,
                self.item_selection_panel,
            ],
            expand=True
        )
        
        super().__init__(
            content = layout,
            expand = True
        )
        pass
    
    
    