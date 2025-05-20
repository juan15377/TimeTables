import dearpygui.dearpygui as dpg
import json
import os
from typing import List, Dict, Tuple
import numpy as np
from src.app.database import database_manager

class HorarioDisponibilidadApp:
    def __init__(self, mode, mode_id, db):
        self.mode = mode
        self.mode_id = mode_id
        self.db = db
        self.DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        self.HORAS_DIA = sorted([f"{i:02d}:00" for i in range(7, 22)] + [f"{i:02d}:30" for i in range(7, 22)])
        self.disponibilidad = {dia: {hora: False for hora in range(len(self.HORAS_DIA))} for dia in range(len(self.DIAS_SEMANA))}
        
        self.tema_disponible = None
        self.tema_no_disponible = None
        self.tema_principal = None
        self.tema_dia_seleccionado = None
        

        
        self.crear_temas()
        

    def crear_temas(self):
        with dpg.theme() as self.tema_disponible:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [100, 180, 130, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [130, 210, 160, 255])
                dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255, 255])
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)  # menor relleno dentro del botón
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0)   # sin separación entre botones

        with dpg.theme() as self.tema_no_disponible:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [220, 100, 100, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [240, 120, 120, 255])
                dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255, 255])
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 2, 2)  # menos relleno
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0)   # sin separación

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
        idx_day = user_data
        nuevo_estado = not all(self.disponibilidad[idx_day].values())
        for (idx_hour,hora) in enumerate(self.HORAS_DIA):
            self.disponibilidad[idx_day][idx_hour] = nuevo_estado
            tag = f"button_availability_{idx_hour}_{idx_day}"
            if dpg.does_item_exist(tag):
                self.actualizar_apariencia_celda(tag, idx_day, idx_hour)

    def seleccionar_toda_hora(self, sender, app_data, user_data):
        idx_hour = user_data
        nuevo_estado = not all(self.disponibilidad[idx_day][idx_hour] for idx_day in range(len(self.DIAS_SEMANA)))
        for (day_idx, dia) in enumerate(self.DIAS_SEMANA):
            self.disponibilidad[day_idx][idx_hour] = nuevo_estado
            tag = f"button_availability_{idx_hour}_{day_idx}"
            if dpg.does_item_exist(tag):
                self.actualizar_apariencia_celda(tag, day_idx, idx_hour)

    def guardar_disponibilidad(self):
        "Guardar la nueva seleccion de disponibilidad"
        
        for (idx_hour,hora) in enumerate(self.HORAS_DIA):
            for (idx_day,dia) in enumerate(self.DIAS_SEMANA):
                availability = self.disponibilidad[idx_day][idx_hour]
                if self.mode == "PROFESSOR":
                    self.db.professors.update_availability(self.mode_id, idx_hour+1, idx_day+1, availability)
                elif self.mode == "CLASSROOM":
                    self.db.classrooms.update_availability(self.mode_id, idx_hour+1, idx_day+1, availability)
                else:
                    self.db.groups.update_availability(self.mode_id, idx_hour+1, idx_day+1, availability)
        
        
    def cargar_disponibilidad(self, sender = None, app_data = None, user_data = None):
        
        query = f"""
            SELECT VAL
            FROM {self.mode}_AVAILABILITY 
            WHERE ID_{self.mode} = {self.mode_id}
            ORDER BY ROW_POSITION, COLUMN_POSITION
        """        
        
        cursor = self.db.execute_query(query)
        
        matrix_availability = np.array(cursor.fetchall())
        matrix_availability = matrix_availability.reshape(30, 7)# 30 hours and 7 days 
        
        for (idx_hour, hour) in enumerate(self.HORAS_DIA):
            for (idx_day, day) in enumerate(self.DIAS_SEMANA):
                # cargamos el valor
                availability = matrix_availability[idx_hour, idx_day]
                self.disponibilidad[idx_day][idx_hour] = availability
                
                button_tag = f"button_availability_{idx_hour}_{idx_day}"
                if availability:
                    dpg.configure_item(button_tag, user_data = (idx_hour, idx_day, True))
                    dpg.bind_item_theme(button_tag, self.tema_disponible)
                else:
                    dpg.configure_item(button_tag, user_data = (idx_hour, idx_day, False))
                    dpg.bind_item_theme(button_tag, self.tema_no_disponible)
                    
        cursor.close()
        
        pass

    def crear_interfaz(self):
        with dpg.group(horizontal=False):  

            with dpg.child_window(width=-1, height=-1, autosize_x=True, horizontal_scrollbar=True):
                with dpg.table(header_row=True, resizable=False, policy=dpg.mvTable_SizingFixedFit,
                            borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):

                    col_width = 80
                    dpg.add_table_column(label=" ", width=col_width)
                    for dia in self.DIAS_SEMANA:
                        dpg.add_table_column(label=dia, width=col_width)

                    with dpg.table_row():
                        dpg.add_text("Todo →")
                        for (idx_day,dia) in enumerate(self.DIAS_SEMANA):
                            btn = dpg.add_button(label="Sel. Día", callback=self.seleccionar_todo_dia,
                                                user_data=idx_day, width=col_width - 10)
                            dpg.bind_item_theme(btn, self.tema_dia_seleccionado)

                    for (idx_hour,hora) in enumerate(self.HORAS_DIA):
                        with dpg.table_row():
                            with dpg.group(horizontal=True):
                                dpg.add_text(f"{hora}")
                                btn = dpg.add_button(label="→", callback=self.seleccionar_toda_hora,
                                                    user_data=idx_hour, width=20)
                                dpg.bind_item_theme(btn, self.tema_dia_seleccionado)

                            for (idx_day,dia) in enumerate(self.DIAS_SEMANA):
                                button_tag = f"button_availability_{idx_hour}_{idx_day}"
                                btn = dpg.add_button(label=" ", tag = button_tag, callback=self.toggle_disponibilidad,
                                                    user_data=(idx_hour, idx_day, False), width=col_width - 10, height=25)
                                dpg.bind_item_theme(btn, self.tema_no_disponible)
               


        self.cargar_disponibilidad()

