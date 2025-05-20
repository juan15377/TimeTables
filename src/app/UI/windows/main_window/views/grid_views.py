
import dearpygui.dearpygui as dpg 
from src.app.database import database_manager
from src.app.UI.components import ProfessorSelector, ClassroomSelector, GroupSelector 
from src.app.UI.components.grid_subjects import ScheduleGrid 


class BaseItemGridView():
    
    def __init__(self, mode):
        def on_change_item_selected(sender, app_data, user_data):
            selected_id = self.item_selector.get_id_selected()
            if selected_id is not None:
                self.grid.set_id_mode(selected_id)
                print("Se actualizo la grilla")
            pass
            
        
        selectors = {
            "PROFESSOR": ProfessorSelector,
            "CLASSROOM": ClassroomSelector,
            "GROUP" : GroupSelector
        }
        
        item_selector = selectors[mode](database_manager, on_change_item_selected, 1)
        

        self.item_selector = item_selector
        self.grid = ScheduleGrid(database_manager, mode, 1)
        
        
    def update(self):
        self.grid.update()
        self.item_selector.update()
        
    def setup_ui(self, parent):
        
        with dpg.group(parent = parent):
        
            self.item_selector.setup_ui(parent)
            self.grid.setup_ui()
    
class ProfessorGridView(BaseItemGridView):
    
    def __init__(self):
        super().__init__("PROFESSOR") 

class ClassroomGridView(BaseItemGridView):
    
    def __init__(self):
        super().__init__("CLASSROOM") 
        
class GroupGridView(BaseItemGridView):
    def __init__(self):
        super().__init__("GROUP")
