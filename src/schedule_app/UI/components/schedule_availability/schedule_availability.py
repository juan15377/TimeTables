import dearpygui.dearpygui as dpg
import json
import os
from typing import List, Dict, Tuple

# Configuración inicial
dpg.create_context()
dpg.create_viewport(title='Disponibilidad de Horarios', width=1100, height=700)

# Variables globales
DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
HORAS_DIA = [f"{i:02d}:00" for i in range(7, 22)] + [f"{i:02d}:30" for i in range(7, 22)]
HORAS_DIA.sort()
PROFESOR_ID = 0  # Esto vendría del sistema principal

# Estado de la cuadrícula (inicialmente todo en False = no disponible)
disponibilidad = {dia: {hora: False for hora in HORAS_DIA} for dia in DIAS_SEMANA}

# Temas
with dpg.theme() as tema_disponible:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, [100, 180, 130, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [130, 210, 160, 255])
        dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255, 255])

with dpg.theme() as tema_no_disponible:
    with dpg.theme_component(dpg.mvButton):
        # Cambio de gris a rojo para indicar no disponibilidad
        dpg.add_theme_color(dpg.mvThemeCol_Button, [220, 100, 100, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [240, 120, 120, 255])
        dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255, 255])

with dpg.theme() as tema_principal:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 4, 4)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 3)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 2)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 4)

with dpg.theme() as tema_dia_seleccionado:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, [70, 130, 180, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [90, 150, 200, 255])
        dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255, 255])

# Funciones
def toggle_disponibilidad(sender, app_data, user_data):
    """Cambia el estado de disponibilidad de una celda y actualiza su apariencia"""
    dia, hora = user_data
    disponibilidad[dia][hora] = not disponibilidad[dia][hora]
    actualizar_apariencia_celda(sender, dia, hora)

def actualizar_apariencia_celda(tag, dia, hora):
    """Actualiza la apariencia visual de una celda según su estado"""
    if disponibilidad[dia][hora]:
        dpg.bind_item_theme(tag, tema_disponible)
    else:
        dpg.bind_item_theme(tag, tema_no_disponible)

def seleccionar_todo_dia(sender, app_data, user_data):
    """Selecciona o deselecciona todas las horas de un día"""
    dia = user_data
    # Determinar si el día está completamente seleccionado
    todas_seleccionadas = all(disponibilidad[dia].values())
    
    # Invertir el estado actual
    nuevo_estado = not todas_seleccionadas
    
    # Aplicar a todas las horas del día
    for hora in HORAS_DIA:
        disponibilidad[dia][hora] = nuevo_estado
        tag = f"{dia}_{hora}"
        if dpg.does_item_exist(tag):
            actualizar_apariencia_celda(tag, dia, hora)

def seleccionar_toda_hora(sender, app_data, user_data):
    """Selecciona o deselecciona una hora específica para todos los días"""
    hora = user_data
    
    # Determinar si la hora está completamente seleccionada en todos los días
    todos_dias_seleccionados = all(disponibilidad[dia][hora] for dia in DIAS_SEMANA)
    
    # Invertir el estado actual
    nuevo_estado = not todos_dias_seleccionados
    
    # Aplicar a todos los días para esta hora
    for dia in DIAS_SEMANA:
        disponibilidad[dia][hora] = nuevo_estado
        tag = f"{dia}_{hora}"
        if dpg.does_item_exist(tag):
            actualizar_apariencia_celda(tag, dia, hora)

def guardar_disponibilidad():
    """Guarda la disponibilidad en un archivo JSON"""
    datos = {
        "profesor_id": PROFESOR_ID,
        "disponibilidad": disponibilidad
    }
    
    try:
        with open(f"disponibilidad_profesor_{PROFESOR_ID}.json", "w") as f:
            json.dump(datos, f, indent=4)
        dpg.set_value("estado_guardado", "✓ Guardado correctamente")
    except Exception as e:
        dpg.set_value("estado_guardado", f"✗ Error al guardar: {str(e)}")

def cargar_disponibilidad():
    """Carga la disponibilidad desde un archivo JSON si existe"""
    global disponibilidad
    archivo = f"disponibilidad_profesor_{PROFESOR_ID}.json"
    
    if os.path.exists(archivo):
        try:
            with open(archivo, "r") as f:
                datos = json.load(f)
                disponibilidad = datos["disponibilidad"]
                
            # Actualizar la interfaz gráfica con los datos cargados
            for dia in DIAS_SEMANA:
                for hora in HORAS_DIA:
                    tag = f"{dia}_{hora}"
                    if dpg.does_item_exist(tag):
                        actualizar_apariencia_celda(tag, dia, hora)
                        
            dpg.set_value("estado_guardado", "✓ Datos cargados correctamente")
            return True
        except Exception as e:
            dpg.set_value("estado_guardado", f"✗ Error al cargar: {str(e)}")
            return False
    
    return False

def seleccionar_todo():
    """Selecciona todas las celdas de la cuadrícula"""
    for dia in DIAS_SEMANA:
        for hora in HORAS_DIA:
            disponibilidad[dia][hora] = True
            tag = f"{dia}_{hora}"
            if dpg.does_item_exist(tag):
                actualizar_apariencia_celda(tag, dia, hora)

def deseleccionar_todo():
    """Deselecciona todas las celdas de la cuadrícula"""
    for dia in DIAS_SEMANA:
        for hora in HORAS_DIA:
            disponibilidad[dia][hora] = False
            tag = f"{dia}_{hora}"
            if dpg.does_item_exist(tag):
                actualizar_apariencia_celda(tag, dia, hora)

# Interfaz de usuario
with dpg.window(label="Disponibilidad de Horarios", width=1080, height=680, tag="main_window"):
    with dpg.group(horizontal=False):
        # Información y controles superiores
        with dpg.group(horizontal=True):
            dpg.add_text("Configuración de disponibilidad horaria")
            dpg.add_spacer(width=20)
            dpg.add_button(label="Seleccionar Todo", callback=seleccionar_todo)
            dpg.add_spacer(width=10)
            dpg.add_button(label="Deseleccionar Todo", callback=deseleccionar_todo)
            dpg.add_spacer(width=20)
            dpg.add_button(label="Guardar", callback=lambda: guardar_disponibilidad())
            dpg.add_spacer(width=10)
            dpg.add_text("", tag="estado_guardado")
        
        dpg.add_spacer(height=10)
        dpg.add_separator()
        dpg.add_spacer(height=10)
        
        # Instrucciones
        dpg.add_text("Instrucciones: Haga clic en las celdas para marcar/desmarcar su disponibilidad.")
        dpg.add_text("Verde = Disponible | Rojo = No disponible")  # Actualizado para reflejar el cambio de color
        dpg.add_spacer(height=10)
        
        # Cuadrícula de disponibilidad
        # Configurar todas las columnas para que tengan el mismo ancho usando la política de tamaño fijo
        with dpg.table(header_row=True, resizable=False, policy=dpg.mvTable_SizingFixedFit, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
            # Columnas (días de la semana + encabezado de horas)
            col_width = 80  # Ancho fijo para todas las columnas
            
            # Primera columna para las horas
            dpg.add_table_column(label=" ", width=col_width)
            
            # Columnas para los días con el mismo ancho
            for dia in DIAS_SEMANA:
                dpg.add_table_column(label=dia, width=col_width)
            
            # Botones para seleccionar toda una hora
            with dpg.table_row():
                dpg.add_text("Todo →")
                for dia in DIAS_SEMANA:
                    btn_dia = dpg.add_button(label="Sel. Día", callback=seleccionar_todo_dia, user_data=dia, width=col_width-10)
                    dpg.bind_item_theme(btn_dia, tema_dia_seleccionado)
            
            # Filas (horas del día)
            for hora in HORAS_DIA:
                with dpg.table_row():
                    # Primera columna: hora + botón para seleccionar toda la fila
                    with dpg.group(horizontal=True):
                        dpg.add_text(f"{hora}")
                        btn_hora = dpg.add_button(label="→", callback=seleccionar_toda_hora, user_data=hora, width=20)
                        dpg.bind_item_theme(btn_hora, tema_dia_seleccionado)
                    
                    # Resto de columnas: celdas de disponibilidad
                    for dia in DIAS_SEMANA:
                        tag = f"{dia}_{hora}"
                        btn = dpg.add_button(label=" ", tag=tag, callback=toggle_disponibilidad, 
                                             user_data=(dia, hora), width=col_width-10, height=25)
                        # Aplicar tema inicial (no disponible por defecto)
                        dpg.bind_item_theme(btn, tema_no_disponible)

# Aplicar tema principal
dpg.bind_theme(tema_principal)

# Intenta cargar datos guardados previamente
cargar_disponibilidad()

# Configuración final
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()