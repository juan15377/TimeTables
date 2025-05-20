from src.app.database import database_manager
import dearpygui.dearpygui as dpg
from src.app.UI.components.windows_manager import Window, windows_manager
from src.app.UI.windows_tags import SCHEDULE_AVAILABILITY_WINDOW_TAG
from src.app.UI.components.schedule_availability.schedule_availability import HorarioDisponibilidadApp


class ScheduleAvailabilityWindow(Window):
    
    def __init__(self, db):
        self.db = db
        
        self.grid_container_tag = "schedule_grid_container"
        
        super().__init__(SCHEDULE_AVAILABILITY_WINDOW_TAG,
                         height=600,
                         width=700,
                         no_resize=True
                         )
        self.container_buttons_tag = "button_schedule_availability_grid"
        
        super().create()
        pass 
    
    def _create_content(self):
        
        dpg.add_child_window(tag=self.grid_container_tag, width=-1, height=520,)
        dpg.add_spacer()
        with dpg.group(tag = self.container_buttons_tag):
            pass 
        
            
    def show(self, **kwargs): # ! rescribir el metodo de Window
        mode = kwargs["mode"]
        mode_id = kwargs["mode_id"]
        
        h = HorarioDisponibilidadApp(mode=mode, mode_id=mode_id, db = self.db)
        
        if dpg.does_alias_exist(self.grid_container_tag):
            dpg.delete_item(self.grid_container_tag, children_only=True)
            
        if dpg.does_alias_exist(self.container_buttons_tag):
            dpg.delete_item(self.container_buttons_tag, children_only=True)
        
        with dpg.group(parent=self.grid_container_tag):
            h.crear_interfaz()
        
        with dpg.group(parent=self.container_buttons_tag,horizontal=True):
            dpg.add_button(label = "Cargar Original", callback=lambda s, a, u : h.cargar_disponibilidad(), width=150, height=35)
            dpg.add_spacer()
            dpg.add_button(label = "Guardar Cambios", callback=lambda s, a, u : h.guardar_disponibilidad(), width=150, height=35)
            
        
        super().show()
    