import dearpygui.dearpygui as dpg





# Función para manejar el evento de guardar materia
def save_subject():
    codigo = dpg.get_value("input_codigo")
    nombre = dpg.get_value("input_nombre")
    
    if not codigo or not nombre:
        dpg.set_value("status", "Error: Todos los campos son obligatorios")
        return
    
    # Aquí iría el código para guardar en la base de datos
    # Por ejemplo: base_de_datos.agregar_materia(codigo, nombre)
    
    # Mensaje de éxito
    dpg.set_value("status", f"Materia guardada: {codigo} - {nombre}")
    
    # Limpiar los campos
    dpg.set_value("input_codigo", "")
    dpg.set_value("input_nombre", "")

# Inicializar DearPyGUI
dpg.create_context()
dpg.create_viewport(title="Sistema de Gestión Académica", width=600, height=300)
dpg.setup_dearpygui()

# Crear la ventana principal
with dpg.window(label="Añadir Materia", width=580, height=280, pos=(10, 10)):
    # Título
    dpg.add_text("Registrar Nueva Materia", color=(255, 255, 0))
    dpg.add_separator()
    
    # Formulario
    with dpg.group(horizontal=False):
        # Código de la materia
        dpg.add_text("Código de la materia:")
        dpg.add_input_text(tag="input_codigo", width=200)
        
        # Espacio
        dpg.add_spacer(height=10)
        
        # Nombre de la materia
        dpg.add_text("Nombre de la materia:")
        dpg.add_input_text(tag="input_nombre", width=400)
        
        # Espacio
        dpg.add_spacer(height=20)
        
        # Botones
        with dpg.group(horizontal=True):
            dpg.add_button(label="Guardar", callback=save_subject, width=100)
            dpg.add_button(label="Cancelar", callback=lambda: dpg.set_value("status", "Operación cancelada"), width=100)
        
        # Espacio
        dpg.add_spacer(height=10)
        
        # Status
        dpg.add_text("", tag="status")

# Mostrar la ventana
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()