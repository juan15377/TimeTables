import dearpygui.dearpygui as dpg 
from src.app.UI.windows_tags import *

def run_app():
    dpg.create_context()
    from src.app.UI.themes import tema_optimizado 

    dpg.bind_theme(tema_optimizado)

    from src.app.UI.windows import windows_manager

    windows_manager.show_window(MAIN_WINDOW_TAG)

    dpg.create_viewport(title="Sistema de Horarios", width=1120, height=850)
    dpg.set_primary_window(MAIN_WINDOW_TAG, True)
    #dpg.set_viewport_resizable(False)  # <- Esta línea evita que el usuario cambie el tamaño
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
