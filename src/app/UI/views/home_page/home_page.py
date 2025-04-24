from .components import ProfessorSelector, ClassroomSelector, GroupSelector 
from src.app.UI.components.grid_subjects.grid_subjects import ScheduleGrid
from src.app.database import database_manager
from src.app.UI.views.list_professors.professors import ClassroomsManager


import dearpygui.dearpygui as dpg

# Inicializa DearPyGUI primero
dpg.create_context()

# Crea los componentes principales
grilla = ScheduleGrid(database_manager, "PROFESSOR", 1)

# Define callbacks útiles para los selectores
def on_professor_selected(sender, app_data, user_data):
    selected_id = prof.get_id_selected()
    if selected_id is not None:
        grilla.set_id_mode(selected_id)

def on_classroom_selected(sender, app_data, user_data):
    selected_id = clas.get_id_selected()
    if selected_id is not None:
        print(f"Classroom selected: {selected_id}")

def on_group_selected(sender, app_data, user_data):
    selected_id = group.get_id_selected()
    if selected_id is not None:
        print(f"Group selected: {selected_id}")


def show_secondary_window():
    print("Intentando desactivar contenido_main")
    dpg.disable_item("main_content")
    dpg.show_item("ventana_secundaria")

def close_secondary_window():
    print("Volviendo a activar contenido_main")
    dpg.disable_item("ventana_secundaria")
    dpg.enable_item("main_content")

# Crea los selectores con callbacks adecuados
prof = ProfessorSelector(database_manager, on_professor_selected)
clas = ClassroomSelector(database_manager, on_classroom_selected)
group = GroupSelector(database_manager, on_group_selected)
clas_man = ClassroomsManager(database_manager)

# Ventana secundaria
with dpg.window(label="Ventana Secundaria", tag="ventana_secundaria", show=False, width=800, height=600):
    #clas_man.crear_interfaz("main_window")
    dpg.add_text("¡Hola desde la ventana secundaria!")
    dpg.add_button(label="Cerrar", callback=close_secondary_window)
    
    
# Tema global
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


# Ventana principal
with dpg.window(label="Window", tag="main_window"):
    
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
    
    # Barra de menú
    with dpg.group(tag = "main_content"):
        # Tab bar con sus contenidos
        with dpg.tab_bar(tag="test_tab_bar"):
            # Tab Professor
            with dpg.tab(label="Professor", tag="test_tab_1"):
                
                # Tab bar con sus contenidos
                with dpg.tab_bar(tag="test_tab_professor_grid"):
                    # Tab Professor
                    with dpg.tab(label="Professor", tag="bar_grid"):
                        prof.setup_ui("bar_grid")
                        
                    with dpg.tab(label="lista professores", tag="bar_list_professor"):
                        clas_man.crear_interfaz("bar_list_professor")
                        
                    
                    # Administrador de aulas dentro del tab de profesores
            # Tab Grupo
            with dpg.tab(label="Grupo", tag="test_tab_2"):
                with dpg.tab_bar(tag="test_tab_groups_grid"):
                    # Tab Professor
                    with dpg.tab(label="Professor", tag="bar_grid_grupos"):
                        group.setup_ui("bar_grid_grupos")
                        
                    with dpg.tab(label="lista professores", tag="bar_list_grupos"):
                        #clas_man.crear_interfaz("bar_list_professor")
                        dpg.add_button(label = "HOLA")
            # Tab Aula
            with dpg.tab(label="Aula", tag="test_tab_3"):
                clas.setup_ui("main_window")
                dpg.add_button(label="Abrir Ventana Secundaria", callback=show_secondary_window)
        
        grilla.setup_ui()

# Configuración del viewport
dpg.create_viewport(title="Sistema de Horarios", width=1000, height=800)
dpg.set_primary_window("main_window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

