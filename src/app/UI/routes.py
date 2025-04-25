from .main_views import VIEWS
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


def delete_actual_content():
    dpg.delete_item("main_content")
    
 
def update(route):
    global database_manager
    
    view = VIEWS[route]
    
    view.update()
    

CALLBACK_UPDATE_ROUTES = {
    "PROFESSOR-GRID" : lambda : update("PROFESSOR-GRID"),
    "PROFESSOR-LIST" : lambda : update("PROFESSOR-LIST"),
    
    "CLASSROOM-GRID" : lambda : update("CLASSROOM-GRID"),
    "CLASSROOM-LIST" : lambda : update("CLASSROOM-LIST"),
    
    "GROUP-GRID" : lambda : update("GROUP-GRID"),
    "GROUP-LIST" : lambda : update("GROUP-LIST")
}

