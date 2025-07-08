import dearpygui.dearpygui as dpg 


with dpg.theme() as tema_optimizado:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 6)
        #dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 10, 6)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 5)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 12, 12)
        dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 14)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (50, 50, 50))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (70, 70, 140))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (90, 90, 170))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (110, 110, 200))
    
    with dpg.theme_component(dpg.mvTable):
        dpg.add_theme_color(dpg.mvThemeCol_Header, (70, 70, 140))
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (90, 90, 160))
        dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (110, 110, 180))
        dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, (40, 40, 50))
        dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt, (50, 50, 60))
        