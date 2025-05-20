from .views import MAIN_WINDOW_VIEWS
import dearpygui.dearpygui as dpg 
from src.app.database import database_manager

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
    
    view = MAIN_WINDOW_VIEWS[route]
    
    view.update()
    

CALLBACK_UPDATE_ROUTES = {
    "PROFESSOR-GRID" : lambda : update("PROFESSOR-GRID"),
    "PROFESSOR-LIST" : lambda : update("PROFESSOR-LIST"),
    
    "CLASSROOM-GRID" : lambda : update("CLASSROOM-GRID"),
    "CLASSROOM-LIST" : lambda : update("CLASSROOM-LIST"),
    
    "GROUP-GRID" : lambda : update("GROUP-GRID"),
    "GROUP-LIST" : lambda : update("GROUP-LIST")
}

