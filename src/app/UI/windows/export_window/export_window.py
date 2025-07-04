import dearpygui.dearpygui as dpg
from .list_classrooms import ListaAulasApp, ListaProfesoresApp
from .list_groups import ListaGruposApp
from src.app.database import database_manager
from src.app.UI.components.windows_manager import Window, windows_manager
from src.app.UI.windows_tags import EXPORT_WINDOW_TAG


import dearpygui.dearpygui as dpg
import dearpygui_extend as dpge

# Variable para almacenar la ruta seleccionada
selected_directory = ""

def show_selected_directory(sender, files, cancel_pressed):
    """Callback que se ejecuta cuando se selecciona un directorio"""
    global selected_directory
    if not cancel_pressed and files:
        selected_directory = files[0]
        dpg.set_value('selected_path_text', f"Directorio seleccionado: {selected_directory}")
        print(f"Directorio seleccionado: {selected_directory}")
        # Cerrar la ventana del selector después de seleccionar
        dpg.hide_item("directory_selector_window")
    else:
        print("Selección cancelada")
        # Cerrar la ventana si se cancela
        dpg.hide_item("directory_selector_window")

def show_directory_selector():
    """Mostrar la ventana del selector de directorio"""
    dpg.show_item("directory_selector_window")

# Crear el contexto de Dear PyGui

# Crear la ventana modal del selector (inicialmente oculta)
with dpg.window(
    label="Seleccionar Directorio", 
    width=650, 
    height=600,
    modal=True,
    show=False,
    tag="directory_selector_window"
):
    dpg.add_text("Selecciona un directorio y haz clic en 'Select files or folders':")
    dpg.add_separator()
    
    # Selector de archivos elegante usando dearpygui_extend
    dpge.add_file_browser(
        tag="directory_browser", 
        label=('Elegir Directorio', 'Seleccionar carpeta'), 
        width=600, 
        height=500, 
        pos=None, 
        default_path='~',  # Directorio home por defecto
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
        dirs_only=True,  # Solo directorios
        show_as_window=False, 
        modal_window=False,  # Ya es modal la ventana padre
        show_ok_cancel=True, 
        show_nav_icons=True, 
        user_data=None, 
        callback=show_selected_directory
    )



class ExportWindow(Window):
    def __init__(self, db):
        self.db = db
        self.tab_professors_tag = "list_professors_export"
        self.tab_classrooms_tag = "list_classrooms_export"
        self.tab_groups_tag = "list_groups_export"
        super().__init__(EXPORT_WINDOW_TAG, width = 600, height=600)
        super().create()
        
    def _create_content(self):
        dpg.add_text("Ningún directorio seleccionado", tag="selected_path_text")
        dpg.add_separator()
        dpg.add_button(label="Seleccionar Directorio", callback=show_directory_selector)
        
        with dpg.group(horizontal=True):
            dpg.add_button(label="Exportar Horario Completo", callback = lambda s, a, u : self.db.export.pdf.grid_formats.complete_schedule(selected_directory, "HORARIOS")),
            dpg.add_button(label="Exportar Horario Completo en un solo archivo")
            dpg.add_spacing()
        
        dpg.add_separator()
        
        with dpg.tab_bar(tag="test_tab_bar"):
            # Tab 1
            with dpg.tab(label="Professor"):
                with dpg.group(tag=self.tab_professors_tag):
                    pass
            
            # Tab 2
            with dpg.tab(label="Grupo"):
                with dpg.group(tag=self.tab_groups_tag):
                    pass
            
            # Tab 3
            with dpg.tab(label="Aula"):
                with dpg.group(tag=self.tab_classrooms_tag):
                    pass
    
    def show(self):
        lp = ListaProfesoresApp(self.db)
        lg = ListaGruposApp(self.db)
        la = ListaAulasApp(self.db)
        
        dpg.delete_item(self.tab_professors_tag, children_only=True)
        dpg.delete_item(self.tab_classrooms_tag, children_only=True)
        dpg.delete_item(self.tab_groups_tag, children_only=True)
        
        # Set the parent directly instead of creating new groups
        lp.setup_ui(parent=self.tab_professors_tag)
        lg.setup_ui(parent=self.tab_groups_tag)
        la.setup_ui(parent=self.tab_classrooms_tag)
        super().show()
        