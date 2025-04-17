from .components import ProfessorSelector, ClassroomSelector, GroupSelector 
from src.schedule_app.UI.components.grid_subjects.grid_subjects import ScheduleGrid
from src.schedule_app.database import database_manager


import dearpygui.dearpygui as dpg


grilla = ScheduleGrid(database_manager, "PROFESSOR", 1)
prof = ProfessorSelector(database_manager, lambda e, r, f: grilla.set_id_mode(prof.get_id_selected()))
clas = ClassroomSelector(database_manager, lambda e, j, k: print("HOLA"))
group = GroupSelector(database_manager, lambda e, j, k: print("HOLA"))


dpg.create_context()


with dpg.theme() as tema_optimizado:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 6)
        dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 10, 6)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 5)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 12, 12)
        dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 14)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (50, 50, 50))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (70, 70, 140))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (90, 90, 170))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (110, 110, 200))
    
    with dpg.theme_component(dpg.mvTable):
        dpg.add_theme_color(dpg.mvThemeCol_Header, (70, 70, 140))
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (90, 90, 160))
        dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (110, 110, 180))
        dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, (40, 40, 50))
        dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt, (50, 50, 60))

def print_me(sender):
    print(f"Menu Item: {sender}")

def change_tab(sender, app_data):
    # Obtener el tag del tab bar
    tab_bar = "test_tab_bar"
    
    # Cambiar al tab 2 si el botón presionado es el 100, sino al tab 1
    if sender == 100:
        dpg.set_value(tab_bar, "test_tab_2")  # Cambia a Tab 2
        
    else:
        dpg.set_value(tab_bar, "test_tab_1")  # Cambia a Tab 1

with dpg.window(label="Window", tag="main_window"):
    # Tab bar (asegúrate de que los tags de los tabs sean strings únicos)
    with dpg.menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Save", callback=print_me)
            dpg.add_menu_item(label="Save As", callback=print_me)

            with dpg.menu(label="Settings"):
                dpg.add_menu_item(label="Setting 1", callback=print_me, check=True)
                dpg.add_menu_item(label="Setting 2", callback=print_me)
                
        with dpg.menu(label="Export"):
            dpg.add_menu_item(label="Save", callback=print_me)
            dpg.add_menu_item(label="Save As", callback=print_me)

            with dpg.menu(label="Settings"):
                dpg.add_menu_item(label="Setting 1", callback=print_me, check=True)
                dpg.add_menu_item(label="Setting 2", callback=print_me)
        
        
    with dpg.tab_bar(tag="test_tab_bar"):
        # Tab 1
        with dpg.tab(label="Professor", tag="test_tab_1"):
            prof.setup_ui(parent="main_window")
                        
        # Tab 2
        with dpg.tab(label="Grupo", tag="test_tab_2"):
            group.setup_ui(parent = "main_window")
                #grilla.setup_ui()
            pass            
        with dpg.tab(label="Aula", tag="test_tab_3"):
            clas.setup_ui(parent="main_window")
                
    grilla.setup_ui()


# Configuración del viewport
dpg.create_viewport(title="Switch entre Tabs", width=1000, height=800)
dpg.set_primary_window("main_window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()