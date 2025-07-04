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
dpg.create_context()

# Crear la ventana principal
with dpg.window(label="Aplicación Principal", width=500, height=200):
    dpg.add_text("Haz clic en el botón para seleccionar un directorio:")
    dpg.add_button(label="Seleccionar Directorio", callback=show_directory_selector)
    dpg.add_separator()
    dpg.add_text("Ningún directorio seleccionado", tag="selected_path_text")

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

# Configurar Dear PyGui
dpg.create_viewport(title="Selector de Directorio", width=700, height=300)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()