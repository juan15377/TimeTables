from .main_views import * 
import dearpygui.dearpygui as dpg 
from ..database import database_manager
from .components import ProfessorSelector, ClassroomSelector, GroupSelector 
from .views import GestorProfesores, ClassroomsManager

ROUTES = {
    "PROFESSOR-GRID",
    "PROFESSOR-LIST",
    "CLASSROOM-GRID",
    "CLASSROOM-LIST",
    "GROUP-GRID",
    "GROUP-LIST"
}


ID_SELECTED = {
    "PROFESSOR" : None,
    "CLASSROOM" : None,
    "GROUP" : None
}

def delete_actual_content():
    dpg.delete_item("main_content")
    
 
def build_grid(route, mode, mode_id):
    global database_manager, ID_SELECTED
    delete_actual_content()
    
    grid = ScheduleGrid(database_manager, mode, mode_id)
    
    with dpg.group(tag = "main_content", parent = route):
        
        def on_change_item_selected(sender, app_data, user_data):
            selected_id = item_selector.get_id_selected()
            if selected_id is not None:
                grid.set_id_mode(selected_id)
                ID_SELECTED[mode] = selected_id
            pass 
        
        if mode == "PROFESSOR":
            item_selector = ProfessorSelector(database_manager, on_change_item_selected, mode_id)
        elif mode == "CLASSROOM":
            item_selector = ClassroomSelector(database_manager, on_change_item_selected, mode_id)
        else:
            item_selector = GroupSelector(database_manager, on_change_item_selected, mode_id)

        item_selector.setup_ui("main_content")
        grid.setup_ui()
        
    pass 
    
    

def build_list(route, mode):
    delete_actual_content()
    
    with dpg.group(tag = "main_content", parent = route):
        if mode == "PROFESSOR":
            print("SE ACTIVO LA LISTA DE PROFESSORES")
            list_items_UI = GestorProfesores(database_manager)
            pass
        elif mode == "CLASSROOM":
            "SE ACTIVO "
            list_items_UI = ClassroomsManager(database_manager)
            pass 
        else:
            dpg.add_button(label = "aun creandose .i.")
            return None
            pass 
        list_items_UI.setup_ui(route)
        pass


ROUTES = {
    "PROFESSOR-GRID",
    "PROFESSOR-LIST",
    "CLASSROOM-GRID",
    "CLASSROOM-LIST",
    "GROUP-GRID",
    "GROUP-LIST"
}

CALLBACK_ROUTES = {
    "PROFESSOR-GRID" : lambda query : build_grid("PROFESSOR-GRID", "PROFESSOR", query),
    "PROFESSOR-LIST" : lambda query : build_list("PROFESSOR-LIST", "PROFESSOR"),
    
    "CLASSROOM-GRID" : lambda query : build_grid("CLASSROOM-GRID", "CLASSROOM", query),
    "CLASSROOM-LIST" : lambda query : build_list("CLASSROOM-LIST", "CLASSROOM"),
    
    "GROUP-GRID" : lambda query : build_grid("GROUP-GRID", "GROUP", query),
    "GROUP-LIST" : lambda query : build_list("GROUP-LIST", "GROUP")
}

