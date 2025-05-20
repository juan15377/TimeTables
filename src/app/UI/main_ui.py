import dearpygui.dearpygui as dpg 
from src.app.UI.windows_tags import *
dpg.create_context()
from src.app.UI.themes import tema_optimizado 

dpg.bind_theme(tema_optimizado)

from src.app.UI.windows import windows_manager

windows_manager.show_window(MAIN_WINDOW_TAG)

# Configuración del viewport
dpg.create_viewport(title="Sistema de Horarios", width=1000, height=800)
dpg.set_primary_window("main_window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()