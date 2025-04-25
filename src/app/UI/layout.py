import dearpygui.dearpygui as dpg
from .route_manager import route_manager
import dearpygui_extend as dpge
import inspect
from src.app.database import database_manager
import os
from .main_views import VIEWS

def print_me(sender, app_data, user_data):
    print("HOLA")

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
    
    sub_tags = ["PROFESSOR-GRID",
    "PROFESSOR-LIST",
    "CLASSROOM-GRID",
    "CLASSROOM-LIST",
    "GROUP-GRID",
    "GROUP-LIST"]
    
    
    if tab_tag in sub_tags:
        route_manager.change_route(tab_tag)
    
def show_window(tag_window):
    if dpg.does_item_exist("main_content"):
        dpg.disable_item("main_content")
    dpg.show_item(tag_window)

def close_window(tag_window):
    dpg.hide_item(tag_window)
    if dpg.does_item_exist("main_content"):
        dpg.enable_item("main_content")
    
#! Ventana que se presenta para guardar una base de datos

# Ventana secundaria
with dpg.window(label="Save", tag="save_window", show=False, width=800, height=600):
    #clas_man.crear_interfaz("main_window")
    dpg.add_text(tag = "select_directory_save_database")
    dpg.add_input_text(tag = "name_save_database")
    
 
    def show_selected_file(sender, files, cancel_pressed):
        if not cancel_pressed:
            dpg.set_value('select_directory_save_database', files[0])
        
    dpge.add_file_browser(
        tag=None, 
        label=('Choose files', 'Select files or folders'), 
        width=600, 
        height=500, 
        pos=None, 
        default_path='~', 
        collapse_sequences=True, 
        collapse_sequences_checkbox=True, 
        sequence_padding='#', 
        show_hidden_files=True, 
        path_input_style=1, 
        add_filename_tooltip=False, 
        tooltip_min_length=100, 
        icon_size=1.0, 
        allow_multi_selection=False, 
        allow_drag=False, 
        allow_create_new_folder=True, 
        dirs_only=True, 
        show_as_window=False, 
        modal_window=True, 
        show_ok_cancel=True, 
        show_nav_icons=True, 
        user_data=None, 
        callback=show_selected_file
    )

    with dpg.group():
        def backup_database(sender, app_data, user_data):
            path = dpg.get_value("select_directory_save_database")
            name_file = dpg.get_value("name_save_database")
            
            file_path = os.path.join(path, name_file + ".db")
            
            print("FILE_PATH", file_path)
            database_manager.backup(file_path)
            
        dpg.add_button(label="Cerrar", callback= lambda s, a, u : close_window("save_window"))
        dpg.add_button(label="Backup", callback= backup_database)
    


    

with dpg.window(label="Sistema de Horarios", tag="main_window", width=780, height=580):
    # Barra de menú principal
    with dpg.menu_bar():
        with dpg.menu(label="Archivo"):
            dpg.add_menu_item(label="Guardar", callback = lambda s, a, u : show_window("save_window"))
            dpg.add_menu_item(label="Cargar", callback=print_me)
            dpg.add_menu_item(label="export", callback=print_me)
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
 
# 
#for (tag_view, view) in VIEWS.items():
#    view.setup_ui(tag_view)
    
VIEWS["PROFESSOR-GRID"].setup_ui("PROFESSOR-GRID")
VIEWS["PROFESSOR-LIST"].setup_ui("PROFESSOR-LIST")

VIEWS["CLASSROOM-GRID"].setup_ui("CLASSROOM-GRID")
VIEWS["CLASSROOM-LIST"].setup_ui("CLASSROOM-LIST")

VIEWS["GROUP-GRID"].setup_ui("GROUP-GRID")