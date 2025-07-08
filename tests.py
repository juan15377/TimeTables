import  dearpygui.dearpygui as dpg

def build_grid(self):
    """Construir la cuadrícula del horario con encabezados fijos"""
    with dpg.group(parent=f"scrollable_grid_container_{self.mode}"):
        with dpg.table(
            header_row=True, 
            resizable=True, 
            policy=dpg.mvTable_SizingStretchProp,
            borders_innerH=True,
            borders_outerH=True,
            borders_innerV=True,
            borders_outerV=True,
            row_background=True
        ):
            # Agrega las columnas (una para cada día)
            dias = ["🕐 Hora", "📅 Lunes", "📅 Martes", "📅 Miércoles", "📅 Jueves", "📅 Viernes", "📅 Sábado", "📅 Domingo"]
            
            for i, dia in enumerate(dias):
                if dia == "🕐 Hora":
                    dpg.add_table_column(
                        label=dia,
                        width_fixed=True,           # Indica que es ancho fijo
                        init_width_or_weight=120,   # Tamaño en píxeles
                        no_resize=True              # Evita redimensionamiento manual
                    )
                else:
                    dpg.add_table_column(
                        label=dia,
                        width_stretch=True,         # Permite que se estire
                        no_resize=False             # Permite redimensionamiento manual
                    )
            
            # Fila de encabezados con horas
            with dpg.table_row():
                # Columna de horas con diseño mejorado
                with dpg.table_cell():
                    with dpg.group(horizontal=False):
                        for hour in self.hours:
                            with dpg.group():
                                btn = dpg.add_button(
                                    label=f"🕐 {hour}",
                                    width=-1,
                                    height=self.cell_height
                                )
                                # Tema especial para botones de hora
                                with dpg.theme() as hour_theme:
                                    with dpg.theme_component(dpg.mvButton):
                                        dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 218, 185, 255))  # Naranja claro
                                        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 200, 150, 255))
                                        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (255, 180, 120, 255))
                                        dpg.add_theme_color(dpg.mvThemeCol_Text, (70, 70, 70, 255))
                                        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8)
                                        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 4)
                                dpg.bind_item_theme(btn, hour_theme)
                
                # Columnas de días con diseño mejorado
                for column in range(7):
                    with dpg.table_cell():
                        with dpg.group(horizontal=False):
                            for row in range(30):
                                cell_tag = self.get_cell_tag(column, row)
                                
                                # Crear botón con estilo mejorado
                                with dpg.group():
                                    cell_btn = dpg.add_button(
                                        label="",
                                        width=-1,
                                        height=self.cell_height,
                                        tag=cell_tag,
                                        callback=self.cell_clicked,
                                        user_data=(column, row, None, None)
                                    )
                                    
                                    # Tema bonito para las celdas
                                    with dpg.theme() as cell_theme:
                                        with dpg.theme_component(dpg.mvButton):
                                            # Colores base más suaves
                                            dpg.add_theme_color(dpg.mvThemeCol_Button, (248, 248, 255, 255))  # Blanco azulado
                                            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (220, 230, 255, 255))  # Azul muy claro
                                            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 220, 255, 255))  # Azul claro
                                            dpg.add_theme_color(dpg.mvThemeCol_Text, (60, 60, 60, 255))
                                            
                                            # Estilos de borde y forma
                                            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
                                            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 2)
                                            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1)
                                            dpg.add_theme_color(dpg.mvThemeCol_Border, (200, 200, 220, 255))
                                    
                                    # Aplicar tema personalizado en lugar del default
                                    dpg.bind_item_theme(cell_tag, cell_theme)
                                
                                # Espaciado sutil entre celdas
                                if row < 29:  # No agregar espacio después de la última fila
                                    dpg.add_spacer(height=1)
                        
                        # Espaciado entre columnas
                        if column < 6:
                            dpg.add_spacer(width=2)

# Función auxiliar para crear temas adicionales (opcional)
def create_additional_themes(self):
    """Crear temas adicionales para diferentes estados de celdas"""
    
    # Tema para celdas ocupadas
    with dpg.theme() as occupied_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (173, 216, 230, 255))  # Azul claro
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (135, 206, 235, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100, 149, 237, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (25, 25, 112, 255))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 2)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (70, 130, 180, 255))
    
    # Tema para celdas conflictivas
    with dpg.theme() as conflict_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 182, 193, 255))  # Rosa claro
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 160, 180, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (255, 140, 160, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (139, 0, 0, 255))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 2)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (220, 20, 60, 255))
    
    # Tema para celdas seleccionadas
    with dpg.theme() as selected_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (152, 251, 152, 255))  # Verde claro
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (144, 238, 144, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (124, 252, 0, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 100, 0, 255))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8)
            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 2)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (34, 139, 34, 255))
    
    # Guardar temas para uso posterior
    self.themes.update({
        "occupied": occupied_theme,
        "conflict": conflict_theme,
        "selected": selected_theme
    })

# Función para aplicar tema global a la tabla (opcional)
def apply_global_table_theme(self):
    """Aplicar tema global a toda la tabla"""
    with dpg.theme() as table_theme:
        with dpg.theme_component(dpg.mvTable):
            dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, (70, 130, 180, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight, (200, 200, 220, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong, (150, 150, 170, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, (255, 255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt, (248, 248, 255, 255))
            dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 6, 4)
    
    return table_theme
