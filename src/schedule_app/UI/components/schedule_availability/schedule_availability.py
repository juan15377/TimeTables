import dearpygui.dearpygui as dpg
import json
import os
from typing import List, Dict, Tuple
import numpy as np
from src.schedule_app.database import database_manager

class HorarioDisponibilidadApp:
    def __init__(self, mode, mode_id, db):
        self.mode = mode
        self.mode_id = mode_id
        self.db = db
        self.DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        self.HORAS_DIA = sorted([f"{i:02d}:00" for i in range(7, 22)] + [f"{i:02d}:30" for i in range(7, 22)])
        self.disponibilidad = {dia: {hora: False for hora in self.HORAS_DIA} for dia in self.DIAS_SEMANA}
        
        self.tema_disponible = None
        self.tema_no_disponible = None
        self.tema_principal = None
        self.tema_dia_seleccionado = None
        
        self.matrix_button_tags = np.array(
            [[
              f"button_availability_{hora}_{dia}" for dia in self.DIAS_SEMANA  
            ] for hora in self.DIAS_SEMANA]
        )
        
        self.crear_temas()
        #self.cargar_disponibilidad()
        
        dpg.bind_theme(self.tema_principal)

    def crear_temas(self):
        with dpg.theme() as self.tema_disponible:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [100, 180, 130, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [130, 210, 160, 255])
                dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255, 255])

        with dpg.theme() as self.tema_no_disponible:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [220, 100, 100, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [240, 120, 120, 255])
                dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255, 255])

        with dpg.theme() as self.tema_principal:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 4, 4)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 3)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 2)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 4)

        with dpg.theme() as self.tema_dia_seleccionado:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [70, 130, 180, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [90, 150, 200, 255])
                dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255, 255])

    def toggle_disponibilidad(self, sender, app_data, user_data):
        hora, dia, val = user_data
        self.disponibilidad[dia][hora] = not self.disponibilidad[dia][hora]
        self.actualizar_apariencia_celda(sender, dia, hora)

    def actualizar_apariencia_celda(self, tag, dia, hora):
        tema = self.tema_disponible if self.disponibilidad[dia][hora] else self.tema_no_disponible
        dpg.bind_item_theme(tag, tema)
        dpg.configure_item(tag, )

    def seleccionar_todo_dia(self, sender, app_data, user_data):
        dia = user_data
        nuevo_estado = not all(self.disponibilidad[dia].values())
        for hora in self.HORAS_DIA:
            self.disponibilidad[dia][hora] = nuevo_estado
            tag = f"button_availability_{hora}_{dia}"
            if dpg.does_item_exist(tag):
                self.actualizar_apariencia_celda(tag, dia, hora)

    def seleccionar_toda_hora(self, sender, app_data, user_data):
        hora = user_data
        nuevo_estado = not all(self.disponibilidad[dia][hora] for dia in self.DIAS_SEMANA)
        for dia in self.DIAS_SEMANA:
            self.disponibilidad[dia][hora] = nuevo_estado
            tag = f"button_availability_{hora}_{dia}"
            if dpg.does_item_exist(tag):
                self.actualizar_apariencia_celda(tag, dia, hora)

    def guardar_disponibilidad(self):
        "Guardar "
    def cargar_disponibilidad(self):
        cursor = self.db.db_connection.cursor()
        
        query = f"""
            SELECT VAL
            FROM {self.mode}_AVAILABILITY 
            WHERE ID_{self.mode} = {self.mode_id}
            ORDER BY ROW_POSITION, COLUMN_POSITION
        """
        
        print(query)
        cursor.execute(query)
        
        matrix_availability = np.array(cursor.fetchall())
        matrix_availability = matrix_availability.reshape(30, 7)# 30 hours and 7 days 
        
        for (idx_hour, hour) in enumerate(self.HORAS_DIA):
            for (idx_day, day) in enumerate(self.DIAS_SEMANA):
                # cargamos el valor
                availability = matrix_availability[idx_hour, idx_day]
                self.disponibilidad[day][hour] = availability
                
                button_tag = f"button_availability_{hour}_{day}"
                if availability:
                    dpg.configure_item(button_tag, user_data = (hour, day, True))
                    dpg.set_item_theme(button_tag, self.tema_disponible)
                else:
                    dpg.configure_item(button_tag, user_data = (hour, day, False))
                    dpg.set_item_theme(button_tag, self.tema_no_disponible)
        pass
        
    def crear_interfaz(self):
        with dpg.group(horizontal=False):  # <-- Agrupa todo en orden vertical
            dpg.add_text("Disponibilidad del profesor")

            with dpg.child_window(width=-1, height=500, autosize_x=True, horizontal_scrollbar=True):
                with dpg.table(header_row=True, resizable=False, policy=dpg.mvTable_SizingFixedFit,
                            borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):

                    col_width = 80
                    dpg.add_table_column(label=" ", width=col_width)
                    for dia in self.DIAS_SEMANA:
                        dpg.add_table_column(label=dia, width=col_width)

                    with dpg.table_row():
                        dpg.add_text("Todo →")
                        for dia in self.DIAS_SEMANA:
                            btn = dpg.add_button(label="Sel. Día", callback=self.seleccionar_todo_dia,
                                                user_data=dia, width=col_width - 10)
                            dpg.bind_item_theme(btn, self.tema_dia_seleccionado)

                    for (idx_hour,hora) in enumerate(self.HORAS_DIA):
                        with dpg.table_row():
                            with dpg.group(horizontal=True):
                                dpg.add_text(f"{hora}")
                                btn = dpg.add_button(label="→", callback=self.seleccionar_toda_hora,
                                                    user_data=hora, width=20)
                                dpg.bind_item_theme(btn, self.tema_dia_seleccionado)

                            for (idx_day,dia) in enumerate(self.DIAS_SEMANA):
                                button_tag = f"button_availability_{hora}_{dia}"
                                btn = dpg.add_button(label=" ", tag = button_tag, callback=self.toggle_disponibilidad,
                                                    user_data=(dia, hora, True), width=col_width - 10, height=25)
                                dpg.bind_item_theme(btn, self.tema_no_disponible)
                                
            # Contenido siempre visible debajo
            dpg.add_spacer(height=10)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Guardar", callback=self.guardar_disponibilidad, height=50, width=100)
                dpg.add_button(label="Guardar", callback=self.guardar_disponibilidad)
            dpg.add_text("", tag="estado_guardado")
            
        self.cargar_disponibilidad()



if __name__ == "__main__":
    dpg.create_context()
    app = HorarioDisponibilidadApp("PROFESSOR", 1, database_manager)

    with dpg.window(label="Disponibilidad de Horarios", tag="main_window"):
        app.crear_interfaz()

    dpg.create_viewport(title="Disponibilidad", width=700, height=620)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("main_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
