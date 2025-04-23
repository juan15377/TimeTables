import dearpygui.dearpygui as dpg

dpg.create_context()

# Funciones para manejar las ventanas
def show_secondary_window():
    dpg.disable_item("contenido_main")     # Desactiva el contenido principal
    dpg.show_item("ventana_secundaria")    # Muestra la ventana secundaria

def close_secondary_window():
    dpg.hide_item("ventana_secundaria")    # Oculta la secundaria
    dpg.enable_item("contenido_main")      # Reactiva el contenido principal

# Ventana principal
with dpg.window(label = "Ventana Principal", tag = "main_window"):
    
    with dpg.group(tag="contenido_main"):  # Agrupa el contenido para poder desactivarlo
        dpg.add_text("Contenido principal activo")
        dpg.add_button(label="Abrir ventana secundaria", callback = show_secondary_window)

# Ventana secundaria (inicialmente oculta)
with dpg.window(label="Ventana Secundaria", tag="ventana_secundaria", show=False, width=300, height=200):
    dpg.add_text("Hola desde la ventana secundaria")
    dpg.add_button(label="Cerrar ventana secundaria", callback = close_secondary_window)

# Configuración del viewport
dpg.create_viewport(title="Ejemplo de Ventanas", width=500, height=400)
dpg.set_primary_window("main_window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
