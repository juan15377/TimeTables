import dearpygui.dearpygui as dpg
import random
import time
from typing import List, Dict

# Generador de nombres aleatorios
nombres = ["Juan", "Maria", "Carlos", "Ana", "Luisa", "Pedro", "Laura", "Jose", "Sofia", "Miguel"]
apellidos = ["Garcia", "Lopez", "Martinez", "Gonzalez", "Rodriguez", "Perez", "Sanchez", "Ramirez", "Flores", "Diaz"]

def generar_profesores(cantidad: int = 10000) -> List[Dict]:
    return [{
        "id": i + 1,
        "nombre": f"{random.choice(nombres)} {random.choice(apellidos)}"
    } for i in range(cantidad)]

# Configuración inicial
profesores = generar_profesores()
dpg.create_context()
dpg.create_viewport(title='Gestión de Profesores', width=900, height=800)

# Variables de estado
profesor_seleccionado = None
nuevo_id = max(p["id"] for p in profesores) + 1 if profesores else 1
ultima_busqueda = ""

# Tema mejorado con mejor aspecto visual
with dpg.theme() as tema_principal:
    with dpg.theme_component(dpg.mvAll):
        # Espaciado general
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 4)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 6, 4)
        dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 4, 4)
        # Bordes y esquinas
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
        dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 3)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5)
        # Colores
        dpg.add_theme_color(dpg.mvThemeCol_Button, [100, 140, 230, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [130, 170, 255, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [80, 120, 210, 255])
        dpg.add_theme_color(dpg.mvThemeCol_Header, [100, 140, 230, 120])
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, [130, 170, 255, 160])

# Tema para botones de eliminación
with dpg.theme() as tema_eliminar:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, [230, 100, 100, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [255, 130, 130, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [210, 80, 80, 255])
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)

# Tema para botones de acción positiva
with dpg.theme() as tema_accion:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, [100, 180, 130, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [130, 210, 160, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [80, 160, 110, 255])
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)

# Tema para botones de disponibilidad
with dpg.theme() as tema_disponibilidad:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, [70, 130, 180, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [100, 160, 210, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [50, 110, 160, 255])
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)

# Tema para botones de materias
with dpg.theme() as tema_materias:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, [180, 120, 70, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [210, 150, 100, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [160, 100, 50, 255])
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)

# Cache para búsquedas
cache_busqueda = {}
profesores_filtrados = profesores.copy()  # Inicializar con todos los profesores

def actualizar_lista(force: bool = False):
    """Actualiza la lista con paginación y caching"""
    global ultima_busqueda, cache_busqueda, profesor_seleccionado, profesores_filtrados
    
    filtro = dpg.get_value("filtro_nombre").lower()
    pagina = dpg.get_value("pagina_actual")
    por_pagina = dpg.get_value("items_por_pagina")
    
    # Si cambia el filtro o se fuerza la actualización, limpiar caché y buscar nuevamente
    if force or filtro != ultima_busqueda:
        start_time = time.time()
        profesores_filtrados = [p for p in profesores if filtro in p["nombre"].lower()]
        cache_busqueda[filtro] = profesores_filtrados
        print(f"Filtrado completado en {time.time()-start_time:.3f}s ({len(profesores_filtrados)} resultados)")
        ultima_busqueda = filtro
        # Resetear la página al cambiar el filtro
        pagina = 1
        dpg.set_value("pagina_actual", pagina)
    else:
        profesores_filtrados = cache_busqueda.get(filtro, profesores_filtrados)
    
    total_paginas = max(1, (len(profesores_filtrados) + por_pagina - 1) // por_pagina)
    dpg.configure_item("total_paginas", label=f"de {total_paginas}")
    dpg.configure_item("pagina_actual", max_value=total_paginas)
    
    # Calcular inicio y fin para paginación
    inicio = (pagina - 1) * por_pagina
    fin = min(inicio + por_pagina, len(profesores_filtrados))
    
    dpg.delete_item("lista_profesores", children_only=True)
    
    for profesor in profesores_filtrados[inicio:fin]:
        with dpg.group(parent="lista_profesores", horizontal=True):
            # Nombre del profesor con ancho fijo
            dpg.add_selectable(
                label=f"{profesor['nombre']}",
                user_data=profesor["id"],
                callback=lambda s, a, u: seleccionar_profesor(u),
                width=560
            )
            
            # Contenedor para los botones con ancho fijo
            with dpg.group(horizontal=True, width=120):
                # Botón de materias con tamaño reducido
                btn_materias = dpg.add_button(
                    label="Materias",
                    user_data=profesor["id"],
                    callback=lambda s, a, u: mostrar_materias(u),
                    width=30,
                    height=20
                )
                dpg.bind_item_theme(btn_materias, tema_materias)
                
                # Botón de disponibilidad con tamaño reducido
                btn_disponibilidad = dpg.add_button(
                    label="Disponibilidad",
                    user_data=profesor["id"],
                    callback=lambda s, a, u: mostrar_disponibilidad(u),
                    width=80,
                    height=20
                )
                dpg.bind_item_theme(btn_disponibilidad, tema_disponibilidad)
                
                # Botón de eliminar con tamaño reducido
                btn_eliminar = dpg.add_button(
                    label="×",
                    user_data=profesor["id"],
                    callback=lambda s, a, u: confirmar_eliminar(u),
                    width=30,
                    height=20
                )
                dpg.bind_item_theme(btn_eliminar, tema_eliminar)

    # Actualizar contador
    dpg.configure_item("contador_total", label=f"Total profesores: {len(profesores)}")


def cambiar_pagina(sender, data):
    """Función específica para cambiar la página y actualizar la lista"""
    actualizar_lista()

def seleccionar_profesor(prof_id):
    global profesor_seleccionado
    profesor_seleccionado = next(p for p in profesores if p["id"] == prof_id)
    dpg.set_value("info_profesor", f"Seleccionado: {profesor_seleccionado['nombre']} (ID: {profesor_seleccionado['id']})")

def mostrar_materias(prof_id):
    """Muestra la ventana de materias para el profesor seleccionado"""
    profesor = next(p for p in profesores if p["id"] == prof_id)
    
    # Verificar si ya existe una ventana de materias abierta y cerrarla
    if dpg.does_item_exist("ventana_materias"):
        dpg.delete_item("ventana_materias")
    
    with dpg.window(modal=True, show=True, tag="ventana_materias", 
                   label=f"Materias de {profesor['nombre']}", 
                   width=500, height=400, pos=[200, 200]):
        dpg.add_text("Esta ventana permitirá gestionar las materias del profesor.")
        dpg.add_spacer(height=10)
        
        dpg.add_text("Aquí se implementará la lista de materias y opciones para agregar/eliminar.")
        dpg.add_spacer(height=20)
        
        # Solo como demostración - Aquí irían los controles reales
        with dpg.child_window(height=200, border=True):
            dpg.add_text(f"Profesor: {profesor['nombre']} (ID: {profesor['id']})")
            dpg.add_text("Funcionalidad de gestión de materias a implementar.")
        
        dpg.add_spacer(height=20)
        with dpg.group(horizontal=True):
            btn_agregar_materia = dpg.add_button(
                label="Agregar Materia",
                callback=lambda: None,  # Implementar en el futuro
                width=150
            )
            dpg.bind_item_theme(btn_agregar_materia, tema_accion)
            
            dpg.add_spacer(width=20)
            
            dpg.add_button(
                label="Cerrar",
                callback=lambda: dpg.delete_item("ventana_materias"),
                width=150
            )

def mostrar_disponibilidad(prof_id):
    """Muestra la ventana de disponibilidad para el profesor seleccionado"""
    profesor = next(p for p in profesores if p["id"] == prof_id)
    
    # Verificar si ya existe una ventana de disponibilidad abierta y cerrarla
    if dpg.does_item_exist("ventana_disponibilidad"):
        dpg.delete_item("ventana_disponibilidad")
    
    with dpg.window(modal=True, show=True, tag="ventana_disponibilidad", 
                   label=f"Disponibilidad de {profesor['nombre']}", 
                   width=500, height=400, pos=[200, 200]):
        dpg.add_text("Esta ventana permitirá definir la disponibilidad horaria del profesor.")
        dpg.add_spacer(height=10)
        
        dpg.add_text("Aquí se implementará un calendario o una grilla de horarios.")
        dpg.add_spacer(height=20)
        
        # Solo como demostración - Aquí irían los controles reales
        with dpg.child_window(height=200, border=True):
            dpg.add_text(f"Profesor: {profesor['nombre']} (ID: {profesor['id']})")
            dpg.add_text("Funcionalidad de disponibilidad a implementar.")
        
        dpg.add_spacer(height=20)
        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Cerrar",
                callback=lambda: dpg.delete_item("ventana_disponibilidad"),
                width=150
            )

def agregar_profesor():
    global nuevo_id, profesores
    
    nombre = dpg.get_value("nuevo_profesor").strip()
    if not nombre:
        return
    
    nuevo_prof = {"id": nuevo_id, "nombre": nombre}
    profesores.append(nuevo_prof)
    nuevo_id += 1
    
    dpg.set_value("nuevo_profesor", "")
    cache_busqueda.clear()
    actualizar_lista(force=True)
    dpg.set_value("info_profesor", f"Agregado: {nombre} (Total: {len(profesores)})")

def confirmar_eliminar(prof_id):
    profesor = next(p for p in profesores if p["id"] == prof_id)
    
    with dpg.window(modal=True, show=True, tag="modal_confirm", label="Confirmación", width=400, height=150, pos=[250, 300]):
        dpg.add_text(f"¿Está seguro que desea eliminar a {profesor['nombre']}?")
        dpg.add_spacer(height=20)
        with dpg.group(horizontal=True):
            btn_confirm = dpg.add_button(
                label="Confirmar",
                callback=lambda: eliminar_profesor(prof_id),
                width=150
            )
            dpg.bind_item_theme(btn_confirm, tema_eliminar)
            
            btn_cancel = dpg.add_button(
                label="Cancelar",
                callback=lambda: dpg.delete_item("modal_confirm"),
                width=150
            )

def eliminar_profesor(prof_id):
    global profesores, profesor_seleccionado
    
    profesores = [p for p in profesores if p["id"] != prof_id]
    if profesor_seleccionado and profesor_seleccionado["id"] == prof_id:
        profesor_seleccionado = None
        dpg.set_value("info_profesor", "Ningún profesor seleccionado")
    
    cache_busqueda.clear()
    dpg.delete_item("modal_confirm")
    actualizar_lista(force=True)

# Interfaz de usuario
with dpg.window(label="Gestión de Profesores", width=880, height=780, tag="main_window"):
    with dpg.group(horizontal=False):
        # Sección de búsqueda
        with dpg.child_window(height=80, label="Búsqueda"):
            with dpg.group(horizontal=True):
                dpg.add_input_text(
                    label="Buscar por nombre", 
                    tag="filtro_nombre",
                    width=300,
                    callback=lambda: actualizar_lista(force=True)
                )
                btn_limpiar = dpg.add_button(
                    label="Limpiar filtro",
                    callback=lambda: [dpg.set_value("filtro_nombre", ""), actualizar_lista(force=True)]
                )
        
        # Agregar nuevo profesor
        with dpg.child_window(height=80, label="Agregar profesor"):
            with dpg.group(horizontal=True):
                dpg.add_input_text(
                    label="Nombre completo",
                    tag="nuevo_profesor",
                    width=300,
                    on_enter=True,
                    callback=agregar_profesor
                )
                btn_agregar = dpg.add_button(
                    label="Agregar",
                    callback=agregar_profesor
                )
                dpg.bind_item_theme(btn_agregar, tema_accion)
        
        # Agregar sección de información del profesor
        with dpg.child_window(height=50, label="Información"):
            dpg.add_text("Ningún profesor seleccionado", tag="info_profesor")
        
        # Paginación
        with dpg.child_window(height=65, label="Paginación"):
            with dpg.group(horizontal=True):
                dpg.add_text("Página:")
                # Cambiamos el callback específico para la paginación
                dpg.add_input_int(
                    tag="pagina_actual",
                    default_value=1,
                    min_value=1,
                    min_clamped=True,
                    width=80,
                    step=1,
                    callback=cambiar_pagina  # Usamos la función específica de cambio de página
                )
                dpg.add_text("", tag="total_paginas")
                dpg.add_spacer(width=20)
                dpg.add_text("Items por página:")
                dpg.add_input_int(
                    tag="items_por_pagina",
                    default_value=50,
                    min_value=10,
                    max_value=200,
                    min_clamped=True,
                    max_clamped=True,
                    width=80,
                    step=10,
                    callback=lambda: [dpg.set_value("pagina_actual", 1), actualizar_lista(force=True)]
                )
                dpg.add_spacer(width=20)
                # Añadir contador total
                dpg.add_text("Total profesores: 0", tag="contador_total")
        
        # Lista de profesores
        with dpg.child_window(label="Lista de profesores", height=450, tag="contenedor_lista", border=True):
            with dpg.child_window(tag="lista_profesores", height=-1, border=False):
                pass
        

# Aplicar tema principal
dpg.bind_theme(tema_principal)

# Inicializar lista
actualizar_lista(force=True)

# Configuración final
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()