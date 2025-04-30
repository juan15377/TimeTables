import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title="Botón Flotante Sobre Todos los Elementos", width=800, height=600)
dpg.setup_dearpygui()

# Crea un tema personalizado para el botón con alta transparencia
with dpg.theme() as button_theme:
    with dpg.theme_component(dpg.mvButton):
        # Color principal del botón (R,G,B,A) - Alta transparencia
        dpg.add_theme_color(dpg.mvThemeCol_Button, [255, 100, 100, 80])
        # Color cuando se pasa el ratón por encima
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [255, 150, 150, 100])
        # Color cuando se hace clic
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [200, 50, 50, 120])
        # Color del texto
        dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255, 200])
        # Redondeo de las esquinas
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)

# Crea un tema para la ventana flotante (sin bordes ni decoración)
with dpg.theme() as floating_window_theme:
    with dpg.theme_component(dpg.mvWindowAppItem):
        # Fondo transparente
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, [0, 0, 0, 0])
        # Sin borde
        dpg.add_theme_color(dpg.mvThemeCol_Border, [0, 0, 0, 0])
        # Sin título
        dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0)

def update_floating_window_position(sender, app_data):
    # Obtener posición actual del ratón
    mouse_pos = dpg.get_mouse_pos(local=False)
    
    # Actualizar la posición de la ventana flotante
    dpg.configure_item("floating_window", pos=[mouse_pos[0]-75, mouse_pos[1]-20])

# Ventana principal con contenido normal
with dpg.window(tag="main_window", label="Ventana Principal", width=800, height=600):
    # Añadimos algunos elementos de ejemplo para mostrar que no son afectados
    dpg.add_text("Este es contenido de la ventana principal")
    dpg.add_button(label="Botón Normal 1", width=120, height=30)
    dpg.add_input_text(label="Campo de texto", default_value="Prueba")
    dpg.add_slider_float(label="Slider", default_value=0.5, max_value=1.0)
    
    # Añadimos más botones para demostrar
    for i in range(5):
        dpg.add_button(label=f"Botón {i+2}", width=120, height=30)

# Creamos nuestra ventana flotante al final para que esté encima de las demás
with dpg.window(tag="floating_window", label="", no_title_bar=True, no_resize=True,
                no_move=True, no_scrollbar=True, no_collapse=True,
                no_background=True, width=150, height=40, on_close=False,
                # Usamos la capa frontal para asegurarnos que esté al frente
                pos=[0, 0]):
    # Botón que sigue al cursor
    dpg.add_button(label="Sígueme", tag="following_button", width=150, height=40)
    # Aplica el tema al botón
    dpg.bind_item_theme("following_button", button_theme)

# Aplica el tema a la ventana flotante
dpg.bind_item_theme("floating_window", floating_window_theme)

# Registra el handler para actualizar la posición en cada fotograma
with dpg.handler_registry():
    dpg.add_mouse_move_handler(callback=update_floating_window_position)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()