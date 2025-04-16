import dearpygui.dearpygui as dpg
import re

# Inicializar DearPyGUI
dpg.create_context()
dpg.create_viewport(title="Lista de Profesores", width=600, height=500)

# Lista de profesores para el ejemplo (podría ser mucho más grande)
profesores = [
    "García Martínez, Ana",
    "Fernández López, Carlos",
    "Rodríguez Sánchez, María",
    "González Pérez, Juan",
    "Martínez Gómez, Elena",
    "López Fernández, Pedro",
    "Sánchez Torres, Laura",
    "Pérez Ruiz, Miguel",
    "Gómez Navarro, Carmen",
    "Torres Vázquez, José",
    # Añade más profesores aquí para simular una lista grande
]

#Para casos de prueba con grandes cantidades de datos
import random
apellidos = ["García", "Fernández", "Rodríguez", "González", "Martínez", "López", "Sánchez", "Pérez", "Gómez", "Torres"]
nombres = ["Ana", "Carlos", "María", "Juan", "Elena", "Pedro", "Laura", "Miguel", "Carmen", "José"]
for i in range(5000):  # Para generar 1000 profesores aleatorios
    profesores.append(f"{random.choice(apellidos)} {random.choice(apellidos)}, {random.choice(nombres)}")

# Diccionario para almacenar eficientemente el estado de selección
seleccion_profesores = {profesor: False for profesor in profesores}

# Crea una lista de pares (profesor, índice) para mantener un orden original estable
profesores_con_indice = [(profesor, i) for i, profesor in enumerate(profesores)]

def ordenar_por_coincidencia(sender, app_data):
    """Ordena los profesores por coincidencia con el término de búsqueda"""
    termino_busqueda = dpg.get_value("busqueda").lower()
    
    if not termino_busqueda:
        # Si no hay término de búsqueda, mostrar en orden original
        profesores_ordenados = profesores_con_indice.copy()
    else:
        # Calcular puntuación de coincidencia para cada profesor
        def calcular_puntuacion(item):
            profesor, indice_original = item
            profesor_lower = profesor.lower()
            # Mayor puntuación para coincidencias exactas al inicio
            if profesor_lower.startswith(termino_busqueda):
                return (3, indice_original)
            # Puntuación media para coincidencias en cualquier parte
            elif termino_busqueda in profesor_lower:
                return (2, indice_original)
            # Menor puntuación para coincidencias parciales
            elif any(parte in profesor_lower for parte in termino_busqueda.split()):
                return (1, indice_original)
            # Sin coincidencia, mantener al final pero en orden original
            return (0, indice_original)
        
        # Ordenar por puntuación (mayor primero) y luego por índice original
        profesores_ordenados = sorted(profesores_con_indice, key=calcular_puntuacion, reverse=True)
    
    # Actualizar la lista mostrada de manera eficiente
    actualizar_lista_ui(profesores_ordenados)

def actualizar_lista_ui(items_ordenados):
    """Actualiza la UI con los profesores ordenados de manera eficiente"""
    dpg.delete_item("lista_profesores", children_only=True)
    
    # Limita a 100 resultados visibles para mejor rendimiento
    items_mostrados = items_ordenados[:100]
    
    # Añade los elementos a la UI
    for profesor, _ in items_mostrados:
        with dpg.group(horizontal=True, parent="lista_profesores"):
            dpg.add_checkbox(
                label="", 
                default_value=seleccion_profesores[profesor], 
                callback=lambda s, a, u: actualizar_seleccion(u), 
                user_data=profesor
            )
            dpg.add_text(profesor)
    
    # Mostrar información sobre la cantidad total y mostrada
    if len(items_ordenados) > 100:
        dpg.add_text(f"Mostrando 100 de {len(items_ordenados)} profesores...", parent="lista_profesores")

def actualizar_seleccion(profesor):
    """Actualiza el estado de selección de un profesor"""
    seleccion_profesores[profesor] = not seleccion_profesores[profesor]

def seleccionar_todos():
    """Selecciona todos los profesores"""
    for profesor in profesores:
        seleccion_profesores[profesor] = True
    
    # Forzar actualización de la UI
    ordenar_por_coincidencia(None, None)

def deseleccionar_todos():
    """Deselecciona todos los profesores"""
    for profesor in profesores:
        seleccion_profesores[profesor] = False
    
    # Forzar actualización de la UI
    ordenar_por_coincidencia(None, None)

def mostrar_seleccionados():
    """Muestra los profesores seleccionados"""
    seleccionados = [prof for prof, estado in seleccion_profesores.items() if estado]
    cantidad = len(seleccionados)
    
    if cantidad == 0:
        texto = "Ningún profesor seleccionado"
    elif cantidad <= 10:
        texto = ", ".join(seleccionados)
    else:
        texto = f"{cantidad} profesores seleccionados"
    
    dpg.set_value("profesores_seleccionados", texto)

# Ventana principal
with dpg.window(label="Lista de Profesores", pos=(0, 0), width=580, height=480, tag="ventana_principal"):
    # Área de búsqueda
    with dpg.group(horizontal=True):
        dpg.add_text("Buscar:")
        dpg.add_input_text(tag="busqueda", width=300, callback=ordenar_por_coincidencia)
    
    dpg.add_spacer(height=5)
    
    # Botones de selección múltiple
    with dpg.group(horizontal=True):
        dpg.add_button(label="Seleccionar Todos", callback=seleccionar_todos, width=150)
        dpg.add_button(label="Deseleccionar Todos", callback=deseleccionar_todos, width=150)
    
    dpg.add_spacer(height=10)
    
    # Lista de profesores con checkboxes
    with dpg.child_window(width=550, height=300, tag="lista_profesores"):
        # Se rellena inicialmente con la función ordenar_por_coincidencia
        pass
    
    dpg.add_spacer(height=10)
    
    # Botón para mostrar seleccionados
    dpg.add_button(label="Mostrar Profesores Seleccionados", callback=mostrar_seleccionados)
    
    # Área para mostrar los profesores seleccionados
    dpg.add_text("Profesores seleccionados:", bullet=True)
    dpg.add_text("Ningún profesor seleccionado", tag="profesores_seleccionados", wrap=500)

# Inicializar la lista con todos los profesores en orden original
ordenar_por_coincidencia(None, None)

# Configuración del renderizado
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()