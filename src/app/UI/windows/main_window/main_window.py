from src.app.UI.components.windows_manager.windows_manager import Window, windows_manager
import dearpygui.dearpygui as dpg 
from .route_manager import route_manager
from src.app.UI.windows_tags import MAIN_WINDOW_TAG
from .views import MAIN_WINDOW_VIEWS 
from src.app.UI.windows_tags import SAVE_FILE_WINDOW_TAG, IMPORT_DATABASE_WINDOW_TAG, EXPORT_WINDOW_TAG

sub_tags = ["PROFESSOR-GRID",
    "PROFESSOR-LIST",
    "CLASSROOM-GRID",
    "CLASSROOM-LIST",
    "GROUP-GRID",
    "GROUP-LIST"]

def print_me(sender, app_data, user_data):
    pass 

def on_change_route(sender, app_data, user_data):
        
    tab_tag = dpg.get_item_user_data(app_data)
    
    if tab_tag in ["PROFESSOR", "CLASSROOM", "GROUP"]:
    
        if tab_tag == "PROFESSOR":
            sub_tag_selected = dpg.get_item_user_data(dpg.get_value("PROFESSOR-OPTIONS")) 
        elif tab_tag == "CLASSROOM":
            sub_tag_selected = dpg.get_item_user_data(dpg.get_value("CLASSROOM-OPTIONS")) 
        else :
            sub_tag_selected = dpg.get_item_user_data(dpg.get_value("GROUP-OPTIONS")) 

        route_manager.change_route(sub_tag_selected)
        return None 
    

    if tab_tag in sub_tags:
        route_manager.change_route(tab_tag)
    
def show_window(tag_window):
    if dpg.does_item_exist("main_content"):
        dpg.disable_item("main_content")
    dpg.show_item(tag_window)

class MainWindow(Window):
    
    def __init__(self, db):
        self.db = db 
        
        super().__init__(window_tag = MAIN_WINDOW_TAG,
                         height=100,
                         width=100,
                         no_resize=True)
        self.create()
        
    def update(self):
        
        for tag in sub_tags:
            route_manager.change_route(tag)
        
        pass 
    
        
    def _create_content(self):
                # Barra de menú principal
        with dpg.menu_bar():
            with dpg.menu(label="Archivo"):
                dpg.add_menu_item(label="Guardar", callback = lambda s, a, u : windows_manager.show_window(SAVE_FILE_WINDOW_TAG))
                dpg.add_menu_item(label="Cargar", callback=lambda s, a, u : windows_manager.show_window(IMPORT_DATABASE_WINDOW_TAG))
                dpg.add_menu_item(label="export", callback= lambda s, a, u : windows_manager.show_window(EXPORT_WINDOW_TAG))
                dpg.add_menu_item(label="Salir", callback=lambda: dpg.stop_dearpygui())

            with dpg.menu(label="Ayuda"):
                dpg.add_menu_item(label="Acerca de", callback=print_me)

        # Contenedor principal
        with dpg.group(tag="main"):
            # Pestañas principales
            with dpg.tab_bar(callback= on_change_route) as tab_id:
                dpg.set_item_user_data(tab_id, "MAIN-TAB")
                # Tab Professor
                with dpg.tab(label="PROFESSOR") as tab_id:
                    dpg.set_item_user_data(tab_id, "PROFESSOR")


                    with dpg.tab_bar(tag="PROFESSOR-OPTIONS", callback=on_change_route) as tab_id:
                        dpg.set_item_user_data(tab_id, "PROFESSOR-OPTIONS")

                        # Crear pestañas y configurar user_data para identificación
                        with dpg.tab(label="Grid", tag="PROFESSOR-GRID") as tab_id:
                            # Configurar user_data para esta pestaña
                            dpg.set_item_user_data(tab_id, "PROFESSOR-GRID")                        
                            pass

                        with dpg.tab(label="Lista", tag="PROFESSOR-LIST") as tab_id:
                            dpg.set_item_user_data(tab_id, "PROFESSOR-LIST")
                            pass
                # Tab Classroom
                with dpg.tab(label="CLASSROOM") as tab_id:
                    dpg.set_item_user_data(tab_id, "CLASSROOM")


                    with dpg.tab_bar(tag="CLASSROOM-OPTIONS", callback=on_change_route) as tab_id:
                        dpg.set_item_user_data(tab_id, "CLASSROOM-OPTIONS")


                        with dpg.tab(label="Grid", tag="CLASSROOM-GRID") as tab_id:
                            dpg.set_item_user_data(tab_id, "CLASSROOM-GRID")
                            pass

                        with dpg.tab(label="Lista", tag="CLASSROOM-LIST") as tab_id:
                            dpg.set_item_user_data(tab_id, "CLASSROOM-LIST")
                            pass
                # Tab Group
                with dpg.tab(label="GROUP") as tab_id:
                    dpg.set_item_user_data(tab_id, "GROUP")

                    with dpg.tab_bar(tag="GROUP-OPTIONS", callback=on_change_route) as tab_id:
                        dpg.set_item_user_data(tab_id, "GROUP-OPTIONS")

                        with dpg.tab(label="Grid", tag="GROUP-GRID") as tab_id:
                            dpg.set_item_user_data(tab_id, "GROUP-GRID")
                            pass 

                        with dpg.tab(label="Lista", tag="GROUP-LIST") as tab_id:
                            dpg.set_item_user_data(tab_id, "GROUP-LIST")
                            pass
                        
        MAIN_WINDOW_VIEWS["PROFESSOR-GRID"].setup_ui("PROFESSOR-GRID")
        MAIN_WINDOW_VIEWS["PROFESSOR-LIST"].setup_ui("PROFESSOR-LIST")
        
        MAIN_WINDOW_VIEWS["CLASSROOM-GRID"].setup_ui("CLASSROOM-GRID")
        MAIN_WINDOW_VIEWS["CLASSROOM-LIST"].setup_ui("CLASSROOM-LIST")  
        
        MAIN_WINDOW_VIEWS["GROUP-GRID"].setup_ui("GROUP-GRID")
        MAIN_WINDOW_VIEWS["GROUP-LIST"].setup_ui("GROUP-LIST")
        
        return super()._create_content()

