import dearpygui.dearpygui as dpg
from typing import Dict, Optional, Callable, List, Any, Union
from .notification_bar import NotificationBar
class Window:
    """Clase base para ventanas configurables"""
    
    def __init__(self, window_tag: str, label: str = "Ventana", 
                 width: int = 300, height: int = 200, 
                 pos: List[int] = None, on_close: Callable = None,
                 no_resize = False):
        self.window_tag = window_tag
        self.label = label
        self.width = width
        self.height = height
        self.pos = pos if pos is not None else [100, 100]
        self.on_close = on_close
        self._is_created = False
        self.no_resize = no_resize
        
        
        
    def create(self, parent: Optional[str] = None) -> str:
        """Crea la ventana si no existe"""
        if self._is_created and dpg.does_item_exist(self.window_tag):
            return self.window_tag
        
        with dpg.window(
            tag=self.window_tag,
            label=self.label,
            width=self.width,
            height=self.height,
            pos=self.pos,
            on_close=self.on_close if self.on_close else self._default_on_close,
            show=False, # ! initialize window hiding
            no_resize=self.no_resize
        ):
            self._create_content()
            
        self._is_created = True
        return self.window_tag
    
    def _default_on_close(self):
        """Comportamiento predeterminado al cerrar la ventana"""
        self.hide()
        
    def _create_content(self):
        """Método a sobrescribir en clases derivadas para añadir contenido a la ventana"""
        pass
    
    def show(self):
        """Muestra la ventana"""
        if not self._is_created:
            self.create()
        elif dpg.does_item_exist(self.window_tag):
            dpg.configure_item(self.window_tag, show=True)
    
    def hide(self):
        """Oculta la ventana"""
        if self._is_created and dpg.does_item_exist(self.window_tag):
            dpg.configure_item(self.window_tag, show=False)
    
    def toggle_visibility(self):
        """Alterna la visibilidad de la ventana"""
        if not self._is_created:
            self.show()
        elif self.is_visible():
            self.hide()
        else:
            self.show()
    
    def is_visible(self) -> bool:
        """Comprueba si la ventana está visible"""
        if self._is_created and dpg.does_item_exist(self.window_tag):
            return dpg.is_item_visible(self.window_tag)
        return False
    
    def set_position(self, x: int, y: int):
        """Cambia la posición de la ventana"""
        if self._is_created and dpg.does_item_exist(self.window_tag):
            self.pos = [x, y]
            dpg.configure_item(self.window_tag, pos=self.pos)
    
    def set_size(self, width: int, height: int):
        """Cambia el tamaño de la ventana"""
        if self._is_created and dpg.does_item_exist(self.window_tag):
            self.width = width
            self.height = height
            dpg.configure_item(self.window_tag, width=width, height=height)
    
    def set_title(self, title: str):
        """Cambia el título de la ventana"""
        if self._is_created and dpg.does_item_exist(self.window_tag):
            self.label = title
            dpg.configure_item(self.window_tag, label=title)
    
    def configure(self, **kwargs):
        """Configura múltiples parámetros a la vez"""
        if not self._is_created:
            # Si la ventana no está creada, solo actualizamos los atributos
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            return
            
        if dpg.does_item_exist(self.window_tag):
            # Actualiza las propiedades de la instancia
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            
            # Construye el diccionario de configuración para DearPyGUI
            config = {}
            if 'width' in kwargs:
                config['width'] = kwargs['width']
            if 'height' in kwargs:
                config['height'] = kwargs['height']
            if 'pos' in kwargs:
                config['pos'] = kwargs['pos']
            if 'label' in kwargs:
                config['label'] = kwargs['label']
            if 'show' in kwargs:
                config['show'] = kwargs['show']
            
            # Aplica la configuración
            if config:
                dpg.configure_item(self.window_tag, **config)


class WindowManager:
    """Gestor centralizado de ventanas"""
    
    _instance = None
    
    def __new__(cls):
        """Implementa el patrón Singleton para el WindowManager"""
        if cls._instance is None:
            cls._instance = super(WindowManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Inicializa el WindowManager una sola vez"""
        if not self._initialized:
            self._windows: Dict[str, Window] = {}
            self._initialized = True
            
        self.notification_system = NotificationBar()
    
    def register_window(self, window: Window) -> Window:
        """Registra una ventana en el gestor"""
        self._windows[window.window_tag] = window
        return window
    
    def create_window(self, window_class: type, window_tag: str, **kwargs) -> Window:
        """Crea y registra una ventana del tipo especificado"""
        if not issubclass(window_class, Window):
            raise TypeError("window_class debe ser una subclase de Window")
            
        window = window_class(window_tag=window_tag, **kwargs)
        return self.register_window(window)
    
    def get_window(self, window_tag: str) -> Optional[Window]:
        """Obtiene una ventana por su tag"""
        return self._windows.get(window_tag)
    
    def show_window(self, window_tag: str, **kwargs):
        """Muestra una ventana específica"""
        window = self.get_window(window_tag)
        if window:
            window.show(**kwargs)
    
    def hide_window(self, window_tag: str):
        """Oculta una ventana específica"""
        window = self.get_window(window_tag)
        if window:
            window.hide()
    
    def toggle_window(self, window_tag: str):
        """Alterna la visibilidad de una ventana específica"""
        window = self.get_window(window_tag)
        if window:
            window.toggle_visibility()
    
    def show_all_windows(self):
        """Muestra todas las ventanas registradas"""
        for window in self._windows.values():
            window.show()
    
    def hide_all_windows(self):
        """Oculta todas las ventanas registradas"""
        for window in self._windows.values():
            window.hide()
    
    def arrange_windows(self, mode: str = "cascade", margin: int = 30):
        """Organiza las ventanas en un patrón específico"""
        visible_windows = [w for w in self._windows.values() if w.is_visible()]
        
        if mode == "cascade":
            # Organiza las ventanas en cascada
            for i, window in enumerate(visible_windows):
                window.set_position(i * margin, i * margin)
        
        elif mode == "tile_horizontal":
            # Organiza las ventanas en mosaico horizontal
            viewport_width = dpg.get_viewport_width()
            window_width = viewport_width // max(1, len(visible_windows))
            
            for i, window in enumerate(visible_windows):
                window.set_position(i * window_width, 0)
                window.set_size(window_width, window.height)
        
        elif mode == "tile_vertical":
            # Organiza las ventanas en mosaico vertical
            viewport_height = dpg.get_viewport_height()
            window_height = viewport_height // max(1, len(visible_windows))
            
            for i, window in enumerate(visible_windows):
                window.set_position(0, i * window_height)
                window.set_size(window.width, window_height)
    
    def configure_window(self, window_tag: str, **kwargs):
        """Configura los parámetros de una ventana específica"""
        window = self.get_window(window_tag)
        if window:
            window.configure(**kwargs)
    
    def has_window(self, window_tag: str) -> bool:
        """Comprueba si existe una ventana con el tag especificado"""
        return window_tag in self._windows
    
    def remove_window(self, window_tag: str):
        """Elimina una ventana del gestor y de la interfaz"""
        window = self.get_window(window_tag)
        if window and dpg.does_item_exist(window_tag):
            dpg.delete_item(window_tag)
        if window_tag in self._windows:
            del self._windows[window_tag]
    
    def notife(self, message):
        self.notification_system.show_notification(message, 4, "info")
        pass 
        

windows_manager = WindowManager() 

# Ejemplo de uso con ventanas personalizadas
class MessageWindow(Window):
    """Ejemplo de una ventana de mensajes personalizada"""
    
    def __init__(self, window_tag: str, message: str = "Mensaje por defecto", **kwargs):
        super().__init__(window_tag=window_tag, **kwargs)
        self.message = message
        
    def _create_content(self):
        """Crea el contenido específico de esta ventana"""
        dpg.add_text(self.message)
        dpg.add_button(label="Cerrar", callback=self.hide)
        
    def set_message(self, message: str):
        """Actualiza el mensaje de la ventana"""
        self.message = message
        if self._is_created and dpg.does_item_exist(self.window_tag):
            # Necesitaríamos implementar una lógica para actualizar el texto
            # En un caso real, podríamos asignar un tag al texto para actualizarlo
            pass

