import dearpygui.dearpygui as dpg
from typing import Dict, Any

def create_blue_theme() -> int:
    """Tema azul moderno para combos/inputs"""
    with dpg.theme() as theme_id:
        with dpg.theme_component(dpg.mvCombo):
            # Colores principales
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (30, 30, 30))    # Fondo azul
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))      # Texto blanco
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)           # Esquinas redondeadas
            
            # Estados interactivos
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (50, 110, 180))  # Hover
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (30, 90, 160))    # Clic/activo
            
            # Flecha desplegable
            dpg.add_theme_color(dpg.mvThemeCol_Button, (100, 160, 220))        # Normal
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (120, 180, 240)) # Hover
            
            # Lista desplegable
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (0, 0, 0))        # Fondo lista
            dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 0, 0))          # Selección
    return theme_id

def create_dark_theme() -> int:
    """Tema oscuro completo para toda la UI"""
    with dpg.theme() as theme_id:
        # Componentes básicos (ventanas, textos, etc.)
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 40))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (220, 220, 220))
        
        # Botones
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 60, 80))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (90, 90, 120))
    return theme_id

