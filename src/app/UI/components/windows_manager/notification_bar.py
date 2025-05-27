import dearpygui.dearpygui as dpg
import threading
import time

dpg.get_active_window()

class NotificationBar:
    def __init__(self):
        
        self.notification_active = False
        self.notification_window = None
    
    def show_notification(self, message, duration=3, notification_type="info"):
        # Si ya hay una notificación activa, la cerramos primero
        if self.notification_active and dpg.does_item_exist("notification_bar"):
            dpg.delete_item("notification_bar")
        
        print("Ventana activa", dpg.get_active_window())

        # Obtener dimensiones del viewport
        viewport_width = dpg.get_viewport_width()
        viewport_height = dpg.get_viewport_height()
        
        # Configurar colores según el tipo
        colors = {
            "info": ([0, 100, 200, 255], [255, 255, 255, 255]),      # Azul
            "success": ([0, 150, 0, 255], [255, 255, 255, 255]),     # Verde
            "warning": ([255, 165, 0, 255], [255, 255, 255, 255]),   # Naranja
            "error": ([200, 0, 0, 255], [255, 255, 255, 255])        # Rojo
        }
        
        bg_color, text_color = colors.get(notification_type, colors["info"])
        
        # Crear la ventana de notificación
        bar_height = 50
        bar_width = viewport_width
        pos_y = viewport_height - bar_height
        
        with dpg.window(label="", tag="notification_bar", 
                       width=bar_width, height=bar_height,
                       pos=[0, pos_y], no_title_bar=True, no_resize=True,
                       no_move=True, no_collapse=True, no_close=True,
                       no_scrollbar=True):
            
            # Establecer color de fondo
            with dpg.theme() as notification_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_WindowBg, bg_color)
                    dpg.add_theme_color(dpg.mvThemeCol_Text, text_color)
            
            dpg.bind_item_theme("notification_bar", notification_theme)
            
            # Contenido de la notificación
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=20)
                
                # Icono según el tipo
                icons = {
                    "info": "ℹ",
                    "success": "✓",
                    "warning": "⚠",
                    "error": "✗"
                }
                
                dpg.add_text(icons.get(notification_type, "ℹ"), 
                           color=text_color)
                dpg.add_spacer(width=10)
                dpg.add_text(message, color=text_color)
                
                # Botón cerrar a la derecha
                dpg.add_spacer(width=bar_width - 200)  # Espaciador para empujar a la derecha
                if dpg.add_button(label="✕", width=30, height=30,
                                callback=self.close_notification):
                    pass
        
        self.notification_active = True
        
        # Auto-cerrar después del tiempo especificado
        def auto_close():
            time.sleep(duration)
            self.close_notification()
        
        threading.Thread(target=auto_close, daemon=True).start()
    
    def close_notification(self):
        if dpg.does_item_exist("notification_bar"):
            dpg.delete_item("notification_bar")
        self.notification_active = False

# Crear instancia global del sistema de notificaciones
notification_system = NotificationBar()

def show_info_notification():
    notification_system.show_notification("Información: Operación completada correctamente", 4, "info")

def show_success_notification():
    notification_system.show_notification("Éxito: Archivo guardado correctamente", 3, "success")

def show_warning_notification():
    notification_system.show_notification("Advertencia: Algunos campos están vacíos", 5, "warning")

def show_error_notification():
    notification_system.show_notification("Error: No se pudo conectar al servidor", 6, "error")
