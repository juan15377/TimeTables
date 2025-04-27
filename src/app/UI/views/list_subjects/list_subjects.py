import dearpygui.dearpygui as dpg
from typing import List, Dict, Set
import sys

# Estructura de datos para materias (con más datos de ejemplo)
materias: List[Dict] = [
    {
        "codigo": "MAT-101",
        "nombre": "Matemáticas Básicas",
        "min_slots": 5,
        "max_slots": 30,
        "total_slots": 25,
        "profesor": "Dr. Juan Pérez",
        "aula": "A-101",
        "grupos": ["ING-1-A", "ING-1-B", "ECO-1-A"]
    },
    {
        "codigo": "FIS-201",
        "nombre": "Física Avanzada",
        "min_slots": 10,
        "max_slots": 25,
        "total_slots": 18,
        "profesor": "Dra. Ana García",
        "aula": "B-203",
        "grupos": ["ING-3-A", "ING-3-B"]
    },
    {
        "codigo": "QUI-105",
        "nombre": "Química Orgánica",
        "min_slots": 8,
        "max_slots": 20,
        "total_slots": 15,
        "profesor": "Dr. Carlos López",
        "aula": "LAB-01",
        "grupos": ["ING-2-A", "BIO-2-A"]
    }
]

# Datos de profesores
profesores = [
    "Dr. Juan Pérez",
    "Dra. Ana García",
    "Dr. Carlos López",
    "Dra. María Rodríguez",
    "Dr. José Martínez",
    "Dra. Laura Sánchez",
    "Dr. Roberto Fernández",
    "Dra. Patricia González",
    "Dr. Miguel Torres",
    "Dra. Carmen Díaz"
]

# Datos de aulas
aulas = [
    "A-101", "A-102", "A-103", "A-104", "A-105",
    "B-201", "B-202", "B-203", "B-204", "B-205",
    "LAB-01", "LAB-02", "LAB-03", "LAB-04",
    "AUD-1", "AUD-2"
]

# Datos de grupos (carrera-semestre-grupo)
carreras = ["ING", "ECO", "MED", "DER", "BIO", "ARQ"]
semestres = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
letras_grupo = ["A", "B", "C", "D"]

# Generar todos los grupos posibles
todos_grupos = []
for carrera in carreras:
    for semestre in semestres:
        for letra in letras_grupo:
            todos_grupos.append(f"{carrera}-{semestre}-{letra}")

dpg.create_context()
dpg.create_viewport(title='Sistema de Gestión de Materias', width=1200, height=900)

# Variables de estado
materia_seleccionada = None
filtro_nombre = ""
filtro_codigo = ""
filtro_profesor = ""
filtro_aula = ""
grupos_seleccionados = set()
profesor_seleccionado = ""
aula_seleccionada = ""

# Tema optimizado con mejor visibilidad
with dpg.theme() as tema_optimizado:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 6)
        dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 10, 6)
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

def filtrar_lista(lista, filtro):
    """Filtra una lista según un texto de filtro"""
    if not filtro:
        return lista
    filtro = filtro.lower()
    return [item for item in lista if filtro in item.lower()]

def actualizar_lista_profesores(sender=None, app_data=None, user_data=None, modal_prefix=""):
    """Actualiza la lista de profesores según el filtro"""
    filtro_tag = f"{modal_prefix}filtro_profesores"
    combo_tag = f"{modal_prefix}combo_profesores"
    
    filtro = dpg.get_value(filtro_tag) if dpg.does_item_exist(filtro_tag) else ""
    lista_filtrada = filtrar_lista(profesores, filtro)
    
    if dpg.does_item_exist(combo_tag):
        dpg.configure_item(combo_tag, items=lista_filtrada)

def actualizar_lista_aulas(sender=None, app_data=None, user_data=None, modal_prefix=""):
    """Actualiza la lista de aulas según el filtro"""
    filtro_tag = f"{modal_prefix}filtro_aulas"
    combo_tag = f"{modal_prefix}combo_aulas"
    
    filtro = dpg.get_value(filtro_tag) if dpg.does_item_exist(filtro_tag) else ""
    lista_filtrada = filtrar_lista(aulas, filtro)
    
    if dpg.does_item_exist(combo_tag):
        dpg.configure_item(combo_tag, items=lista_filtrada)

def actualizar_lista_grupos(container_tag="lista_grupos", current_grupos=None):
    """Actualiza la lista de grupos según el estado actual"""
    if dpg.does_item_exist(container_tag):
        dpg.delete_item(container_tag, children_only=True)
        
        grupos_actuales = current_grupos if current_grupos is not None else grupos_seleccionados
        
        for grupo in todos_grupos:
            is_selected = grupo in grupos_actuales
            dpg.add_selectable(
                label=grupo,
                parent=container_tag,
                callback=toggle_grupo,
                user_data=(grupo, container_tag),
                default_value=is_selected
            )

def toggle_grupo(sender, app_data, user_data):
    """Alterna un grupo en la selección"""
    grupo, container_tag = user_data
    
    # Determinar si estamos en la ventana de creación o edición
    if container_tag == "modal_create_grupos":
        # Ventana de creación
        global grupos_seleccionados
        
        if grupo in grupos_seleccionados:
            grupos_seleccionados.remove(grupo)
        else:
            grupos_seleccionados.add(grupo)
        
        # Actualizar contador de grupos
        contador_tag = "modal_create_contador_grupos"
        if dpg.does_item_exist(contador_tag):
            dpg.set_value(contador_tag, f"Grupos seleccionados: {len(grupos_seleccionados)}")
    
    elif container_tag == "modal_edit_grupos":
        # Ventana de edición
        if not materia_seleccionada:
            return
            
        grupos = set(materia_seleccionada.get("grupos", []))
        
        if grupo in grupos:
            grupos.remove(grupo)
        else:
            grupos.add(grupo)
        
        materia_seleccionada["grupos"] = list(grupos)
        
        # Actualizar contador de grupos
        contador_tag = "modal_edit_contador_grupos"
        if dpg.does_item_exist(contador_tag):
            dpg.set_value(contador_tag, f"Grupos seleccionados: {len(grupos)}")

def actualizar_lista():
    """Actualiza la lista de materias aplicando filtros"""
    # Asegurarnos que la tabla existe antes de modificarla
    if not dpg.does_item_exist("lista_materias"):
        return
        
    # Eliminar filas existentes
    for item in dpg.get_item_children("lista_materias", 1):
        dpg.delete_item(item)
    
    # Contador para alternar colores de filas
    contador_filas = 0
    
    for materia in materias:
        cumple_filtro = (
            (filtro_nombre.lower() in materia["nombre"].lower()) and
            (filtro_codigo.lower() in materia["codigo"].lower())
        )
        
        if cumple_filtro:
            # Crear una fila con un ID único
            row_id = f"row_{materia['codigo']}_{contador_filas}"
            with dpg.table_row(parent="lista_materias", tag=row_id):
                # Celda código
                with dpg.table_cell():
                    dpg.add_text(materia["codigo"])
                
                # Celda nombre
                with dpg.table_cell():
                    dpg.add_text(materia["nombre"])
                
                # Celda slots
                with dpg.table_cell():
                    slots_str = f"{materia['total_slots']} (min {materia['min_slots']}, max {materia['max_slots']})"
                    dpg.add_text(slots_str)
                
                # Celda profesor
                with dpg.table_cell():
                    dpg.add_text(materia["profesor"])
                
                # Celda aula
                with dpg.table_cell():
                    dpg.add_text(materia["aula"])
                
                # Celda grupos
                with dpg.table_cell():
                    grupos_str = ", ".join(materia.get("grupos", [])[:3])
                    if len(materia.get("grupos", [])) > 3:
                        grupos_str += f"... (+{len(materia.get('grupos', [])) - 3})"
                    dpg.add_text(grupos_str)
                
                # Celda acciones
                with dpg.table_cell():
                    with dpg.group(horizontal=True):
                        dpg.add_button(
                            label="Editar",
                            user_data=materia["codigo"],
                            callback=lambda s, a, u: abrir_modal_edicion(u),
                            width=70
                        )
                        dpg.add_button(
                            label="✕",
                            user_data=materia["codigo"],
                            callback=lambda s, a, u: confirmar_eliminar(u),
                            width=30,
                            tag=f"btn_eliminar_{materia['codigo']}"
                        )
            
            contador_filas += 1
    
    # Actualizar contador de materias
    if dpg.does_item_exist("contador_materias"):
        dpg.set_value("contador_materias", f"Total materias mostradas: {contador_filas} de {len(materias)}")


def abrir_modal_creacion():
    """Abre la ventana modal para crear una nueva materia"""
    global grupos_seleccionados
    grupos_seleccionados = set()
    
    # Calcular posición central
    window_width = 800
    window_height = 650  # Aumentado para acomodar más elementos
    pos_x = (dpg.get_viewport_width() - window_width) // 2
    pos_y = (dpg.get_viewport_height() - window_height) // 2
    
    with dpg.window(
        label="Crear Nueva Materia",
        width=window_width,
        height=window_height,
        pos=[pos_x, pos_y],
        modal=True,
        tag="modal_create",
        on_close=limpiar_campos_creacion
    ):
        # Contenido del formulario
        with dpg.group():
            # Primera fila: código y nombre
            with dpg.group(horizontal=True):
                dpg.add_input_text(label="Código", tag="modal_create_codigo", width=120)
                dpg.add_input_text(label="Nombre", tag="modal_create_nombre", width=400)
            
            # Segunda fila: slots
            with dpg.group(horizontal=True):
                dpg.add_input_int(label="Mín. Slots", tag="modal_create_min_slots", width=120, min_value=1, min_clamped=True, default_value=5)
                dpg.add_input_int(label="Máx. Slots", tag="modal_create_max_slots", width=120, min_value=1, min_clamped=True, default_value=30)
                dpg.add_input_int(label="Total Slots", tag="modal_create_total_slots", width=120, min_value=1, min_clamped=True, default_value=15)
            
            # Tercera fila: modalidad (presencial/online)
            with dpg.group(horizontal=True):
                dpg.add_text("Modalidad:")
                dpg.add_radio_button(
                    items=["Presencial", "Online", "Híbrida"],
                    tag="modal_create_modalidad",
                    default_value="Presencial",
                    horizontal=True,
                    callback=lambda s, a, u: toggle_aula_selector(a)
                )
            
            # Cuarta fila: profesor (con búsqueda mejorada)
            dpg.add_text("Profesor:")
            with dpg.group(horizontal=True):
                dpg.add_input_text(
                    hint="Buscar profesor...",
                    tag="modal_create_filtro_profesores",
                    width=300,
                    callback=lambda s, a, u: actualizar_lista_profesores(modal_prefix="modal_create_")
                )
                dpg.add_button(
                    label="Buscar",
                    callback=lambda: actualizar_lista_profesores(modal_prefix="modal_create_"),
                    width=80
                )
            
            dpg.add_combo(
                items=profesores,
                tag="modal_create_combo_profesores",
                width=400
            )
            
            # Quinta fila: aula (con búsqueda mejorada)
            with dpg.collapsing_header(label="Información de Aula", tag="modal_create_aula_header", default_open=True):
                dpg.add_text("Aula:")
                with dpg.group(horizontal=True):
                    dpg.add_input_text(
                        hint="Buscar aula...",
                        tag="modal_create_filtro_aulas",
                        width=300,
                        callback=lambda s, a, u: actualizar_lista_aulas(modal_prefix="modal_create_")
                    )
                    dpg.add_button(
                        label="Buscar",
                        callback=lambda: actualizar_lista_aulas(modal_prefix="modal_create_"),
                        width=80
                    )
                
                dpg.add_combo(
                    items=aulas,
                    tag="modal_create_combo_aulas",
                    width=400
                )
            
            # Sexta fila: administración de grupos
            dpg.add_separator()
            dpg.add_text("Administración de Grupos", color=[255, 255, 0])
            
            # Búsqueda y selección de grupos
            with dpg.group(horizontal=True):
                dpg.add_input_text(
                    hint="Buscar grupo...",
                    tag="modal_create_filtro_grupos",
                    width=300,
                    callback=lambda s, a, u: actualizar_lista_grupos_disponibles()
                )
                dpg.add_button(
                    label="Buscar",
                    callback=lambda: actualizar_lista_grupos_disponibles(),
                    width=80
                )
            
            with dpg.group(horizontal=True):
                # Grupos disponibles
                with dpg.child_window(width=380, height=150, border=True):
                    dpg.add_text("Grupos Disponibles:")
                    dpg.add_table(
                        tag="modal_create_tabla_grupos_disponibles",
                        header_row=True,
                        borders_innerH=True,
                        borders_outerH=True,
                        borders_innerV=True,
                        borders_outerV=True
                    )
                    
                    # Agregar encabezados a la tabla
                    with dpg.table_row():
                        dpg.add_table_cell()
                        dpg.add_text("ID")
                        dpg.add_text("Nombre")
                        dpg.add_text("Carrera")
                
                # Botones para agregar/quitar
                with dpg.group(width=40):
                    dpg.add_spacer(height=60)
                    dpg.add_button(
                        label=">>",
                        callback=agregar_grupo_seleccionado,
                        width=40
                    )
                    dpg.add_spacer(height=10)
                    dpg.add_button(
                        label="<<",
                        callback=quitar_grupo_seleccionado,
                        width=40
                    )
                
                # Grupos seleccionados
                with dpg.child_window(width=380, height=150, border=True):
                    dpg.add_text("Grupos Asignados:")
                    dpg.add_table(
                        tag="modal_create_tabla_grupos_asignados",
                        header_row=True,
                        borders_innerH=True,
                        borders_outerH=True,
                        borders_innerV=True,
                        borders_outerV=True
                    )
                    
                    # Agregar encabezados a la tabla
                    with dpg.table_row():
                        dpg.add_table_cell()
                        dpg.add_text("ID")
                        dpg.add_text("Nombre")
                        dpg.add_text("Carrera")
            
            dpg.add_text("Grupos seleccionados: 0", tag="modal_create_contador_grupos")
            
            # Botones de acción
            dpg.add_separator()
            dpg.add_spacer(height=10)
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Guardar",
                    callback=agregar_materia,
                    width=150
                )
                dpg.add_button(
                    label="Cancelar",
                    callback=lambda: dpg.delete_item("modal_create"),
                    width=150
                )
    
    # Actualizar listas dinámicas
    actualizar_lista_grupos_disponibles()
    actualizar_lista_profesores(modal_prefix="modal_create_")
    actualizar_lista_aulas(modal_prefix="modal_create_")


def toggle_aula_selector(value):
    """Habilita o deshabilita el selector de aula según la modalidad"""
    if value == "Online":
        dpg.configure_item("modal_create_aula_header", default_open=False)
        dpg.disable_item("modal_create_combo_aulas")
        dpg.disable_item("modal_create_filtro_aulas")
    else:
        dpg.configure_item("modal_create_aula_header", default_open=True)
        dpg.enable_item("modal_create_combo_aulas")
        dpg.enable_item("modal_create_filtro_aulas")


def actualizar_lista_grupos_disponibles():
    """Actualiza la lista de grupos disponibles según el filtro"""
    filtro = dpg.get_value("modal_create_filtro_grupos").lower()
    
    # Limpiar tabla existente, manteniendo los encabezados
    dpg.delete_item("modal_create_tabla_grupos_disponibles", children_only=True, slot=1)
    
    # Recrear encabezados
    with dpg.table_row(parent="modal_create_tabla_grupos_disponibles"):
        dpg.add_table_cell()
        dpg.add_text("ID")
        dpg.add_text("Nombre")
        dpg.add_text("Carrera")
    
    # Filtrar y agregar grupos que no estén ya seleccionados
    for grupo in grupos:
        if grupo["id"] in grupos_seleccionados:
            continue
            
        if filtro and filtro not in grupo["nombre"].lower() and filtro not in grupo["carrera"].lower():
            continue
            
        with dpg.table_row(parent="modal_create_tabla_grupos_disponibles"):
            dpg.add_checkbox(
                callback=lambda s, a, u: seleccionar_grupo_disponible(u),
                user_data=grupo["id"]
            )
            dpg.add_text(grupo["id"])
            dpg.add_text(grupo["nombre"])
            dpg.add_text(grupo["carrera"])


def actualizar_tabla_grupos_asignados():
    """Actualiza la tabla de grupos asignados"""
    # Limpiar tabla existente, manteniendo los encabezados
    dpg.delete_item("modal_create_tabla_grupos_asignados", children_only=True, slot=1)
    
    # Recrear encabezados
    with dpg.table_row(parent="modal_create_tabla_grupos_asignados"):
        dpg.add_table_cell()
        dpg.add_text("ID")
        dpg.add_text("Nombre")
        dpg.add_text("Carrera")
    
    # Agregar grupos seleccionados
    for grupo_id in grupos_seleccionados:
        # Buscar información del grupo
        grupo = next((g for g in grupos if g["id"] == grupo_id), None)
        if grupo:
            with dpg.table_row(parent="modal_create_tabla_grupos_asignados"):
                dpg.add_checkbox(
                    default_value=True,
                    callback=lambda s, a, u: seleccionar_grupo_asignado(u),
                    user_data=grupo["id"]
                )
                dpg.add_text(grupo["id"])
                dpg.add_text(grupo["nombre"])
                dpg.add_text(grupo["carrera"])
    
    # Actualizar contador
    dpg.set_value("modal_create_contador_grupos", f"Grupos seleccionados: {len(grupos_seleccionados)}")


def seleccionar_grupo_disponible(grupo_id):
    """Marca un grupo disponible para ser agregado"""
    global grupos_para_agregar
    if "grupos_para_agregar" not in globals():
        global grupos_para_agregar
        grupos_para_agregar = set()
    
    if grupo_id in grupos_para_agregar:
        grupos_para_agregar.remove(grupo_id)
    else:
        grupos_para_agregar.add(grupo_id)


def seleccionar_grupo_asignado(grupo_id):
    """Marca un grupo asignado para ser eliminado"""
    global grupos_para_quitar
    if "grupos_para_quitar" not in globals():
        global grupos_para_quitar
        grupos_para_quitar = set()
    
    if grupo_id in grupos_para_quitar:
        grupos_para_quitar.remove(grupo_id)
    else:
        grupos_para_quitar.add(grupo_id)


def agregar_grupo_seleccionado():
    """Agrega los grupos seleccionados a la lista de asignados"""
    global grupos_seleccionados, grupos_para_agregar
    
    if "grupos_para_agregar" in globals() and grupos_para_agregar:
        grupos_seleccionados.update(grupos_para_agregar)
        grupos_para_agregar.clear()
        
        # Actualizar ambas tablas
        actualizar_lista_grupos_disponibles()
        actualizar_tabla_grupos_asignados()


def quitar_grupo_seleccionado():
    """Quita los grupos seleccionados de la lista de asignados"""
    global grupos_seleccionados, grupos_para_quitar
    
    if "grupos_para_quitar" in globals() and grupos_para_quitar:
        grupos_seleccionados.difference_update(grupos_para_quitar)
        grupos_para_quitar.clear()
        
        # Actualizar ambas tablas
        actualizar_lista_grupos_disponibles()
        actualizar_tabla_grupos_asignados()


def actualizar_lista_profesores(modal_prefix=""):
    """Actualiza la lista de profesores según el filtro"""
    filtro = dpg.get_value(f"{modal_prefix}filtro_profesores").lower()
    
    # Filtrar profesores
    profesores_filtrados = [
        p for p in profesores 
        if not filtro or filtro in p["nombre"].lower() or filtro in p["id"].lower()
    ]
    
    # Actualizar el combo
    dpg.configure_item(
        f"{modal_prefix}combo_profesores",
        items=[f"{p['id']} - {p['nombre']}" for p in profesores_filtrados]
    )


def actualizar_lista_aulas(modal_prefix=""):
    """Actualiza la lista de aulas según el filtro"""
    filtro = dpg.get_value(f"{modal_prefix}filtro_aulas").lower()
    
    # Filtrar aulas
    aulas_filtradas = [
        a for a in aulas 
        if not filtro or filtro in a["nombre"].lower() or filtro in a["edificio"].lower()
    ]
    
    # Actualizar el combo
    dpg.configure_item(
        f"{modal_prefix}combo_aulas",
        items=[f"{a['id']} - {a['edificio']} {a['nombre']}" for a in aulas_filtradas]
    )


def agregar_materia():
    """Guarda la nueva materia con los datos proporcionados"""
    codigo = dpg.get_value("modal_create_codigo")
    nombre = dpg.get_value("modal_create_nombre")
    min_slots = dpg.get_value("modal_create_min_slots")
    max_slots = dpg.get_value("modal_create_max_slots")
    total_slots = dpg.get_value("modal_create_total_slots")
    profesor = dpg.get_value("modal_create_combo_profesores")
    modalidad = dpg.get_value("modal_create_modalidad")
    
    # Validar campos obligatorios
    if not codigo or not nombre or not profesor or (modalidad != "Online" and not dpg.get_value("modal_create_combo_aulas")):
        dpg.configure_item("modal_info_error", show=True)
        return
    
    # Obtener aula solo si no es online
    aula = None
    if modalidad != "Online":
        aula = dpg.get_value("modal_create_combo_aulas")
    
    # Crear nueva materia con los datos
    nueva_materia = {
        "id": codigo,
        "nombre": nombre,
        "min_slots": min_slots,
        "max_slots": max_slots,
        "total_slots": total_slots,
        "profesor": profesor.split(" - ")[0] if " - " in profesor else profesor,
        "aula": aula.split(" - ")[0] if aula and " - " in aula else aula,
        "modalidad": modalidad,
        "grupos": list(grupos_seleccionados)
    }
    
    # Agregar a la lista de materias
    materias.append(nueva_materia)
    
    # Actualizar tabla principal
    #actualizar_tabla_materias()
    
    # Cerrar modal
    dpg.delete_item("modal_create")
    
    # Mostrar mensaje de éxito
    dpg.configure_item("modal_info_success", show=True)


def limpiar_campos_creacion():
    """Limpia los campos del formulario de creación"""
    global grupos_seleccionados
    grupos_seleccionados = set()
    if "grupos_para_agregar" in globals():
        global grupos_para_agregar
        grupos_para_agregar.clear()
    if "grupos_para_quitar" in globals():
        global grupos_para_quitar
        grupos_para_quitar.clear()

def abrir_modal_edicion(codigo):
    """Abre la ventana modal para editar una materia"""
    global materia_seleccionada
    materia_seleccionada = next((m for m in materias if m["codigo"] == codigo), None)
    
    if not materia_seleccionada:
        return
    
    # Calcular posición central
    window_width = 800
    window_height = 600
    pos_x = (dpg.get_viewport_width() - window_width) // 2
    pos_y = (dpg.get_viewport_height() - window_height) // 2
    
    with dpg.window(
        label=f"Editar Materia [{materia_seleccionada['codigo']}]",
        width=window_width,
        height=window_height,
        pos=[pos_x, pos_y],
        modal=True,
        tag="modal_edit"
    ):
        # Contenido del formulario
        with dpg.group():
            # Primera fila: código y nombre
            with dpg.group(horizontal=True):
                dpg.add_input_text(
                    label="Código", 
                    tag="modal_edit_codigo", 
                    width=120, 
                    default_value=materia_seleccionada["codigo"]
                )
                dpg.add_input_text(
                    label="Nombre", 
                    tag="modal_edit_nombre", 
                    width=300, 
                    default_value=materia_seleccionada["nombre"]
                )
            
            # Segunda fila: slots
            with dpg.group(horizontal=True):
                dpg.add_input_int(
                    label="Mín. Slots", 
                    tag="modal_edit_min_slots", 
                    width=120, 
                    min_value=1, 
                    min_clamped=True, 
                    default_value=materia_seleccionada["min_slots"]
                )
                dpg.add_input_int(
                    label="Máx. Slots", 
                    tag="modal_edit_max_slots", 
                    width=120, 
                    min_value=1, 
                    min_clamped=True, 
                    default_value=materia_seleccionada["max_slots"]
                )
                dpg.add_input_int(
                    label="Total Slots", 
                    tag="modal_edit_total_slots", 
                    width=120, 
                    min_value=1, 
                    min_clamped=True, 
                    default_value=materia_seleccionada["total_slots"]
                )
            
            # Tercera fila: profesor (con filtro)
            with dpg.group(horizontal=True):
                dpg.add_text("Profesor:")
                dpg.add_input_text(
                    label="Filtrar", 
                    tag="modal_edit_filtro_profesores", 
                    width=200, 
                    callback=lambda s, a, u: actualizar_lista_profesores(modal_prefix="modal_edit_")
                )
                dpg.add_combo(
                    items=profesores, 
                    tag="modal_edit_combo_profesores", 
                    width=300,
                    default_value=materia_seleccionada["profesor"]
                )
            
            # Cuarta fila: aula (con filtro)
            with dpg.group(horizontal=True):
                dpg.add_text("Aula:")
                dpg.add_input_text(
                    label="Filtrar", 
                    tag="modal_edit_filtro_aulas", 
                    width=200, 
                    callback=lambda s, a, u: actualizar_lista_aulas(modal_prefix="modal_edit_")
                )
                dpg.add_combo(
                    items=aulas, 
                    tag="modal_edit_combo_aulas", 
                    width=300,
                    default_value=materia_seleccionada["aula"]
                )
            
            # Quinta fila: grupos
            dpg.add_text("Seleccione grupos para la materia:")
            grupos_count = len(materia_seleccionada.get("grupos", []))
            dpg.add_text(f"Grupos seleccionados: {grupos_count}", tag="modal_edit_contador_grupos")
            
            # Lista de grupos en una ventana con scroll
            with dpg.child_window(height=200, width=-1, border=True):
                with dpg.group(tag="modal_edit_grupos"):
                    # Los grupos se añaden dinámicamente
                    pass
            
            # Botones de acción
            dpg.add_spacer(height=20)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Guardar Cambios", callback=actualizar_materia, width=150)
                dpg.add_button(label="Cancelar", callback=lambda: dpg.delete_item("modal_edit"), width=150)
        
        # Actualizar listas dinámicas
        actualizar_lista_grupos("modal_edit_grupos", set(materia_seleccionada.get("grupos", [])))

def verificar_duplicado(codigo, excluir=None):
    """Verifica si ya existe un código duplicado"""
    for materia in materias:
        if materia["codigo"] == codigo and materia["codigo"] != excluir:
            return True
    return False

def agregar_materia():
    """Agrega una nueva materia"""
    codigo = dpg.get_value("modal_create_codigo").strip()
    nombre = dpg.get_value("modal_create_nombre").strip()
    
    # Validaciones básicas
    if not codigo or not nombre:
        mostrar_error("Los campos Código y Nombre son obligatorios")
        return
    
    # Verificar si ya existe el código
    if verificar_duplicado(codigo):
        mostrar_error(f"Ya existe una materia con el código {codigo}")
        return
    
    min_s = dpg.get_value("modal_create_min_slots")
    max_s = dpg.get_value("modal_create_max_slots")
    total_s = dpg.get_value("modal_create_total_slots")
    profesor = dpg.get_value("modal_create_combo_profesores")
    aula = dpg.get_value("modal_create_combo_aulas")
    
    # Validaciones adicionales
    if not profesor:
        mostrar_error("Debe seleccionar un profesor")
        return
        
    if not aula:
        mostrar_error("Debe seleccionar un aula")
        return
    
    # Validación de slots
    if not (min_s <= total_s <= max_s):
        mostrar_error("Error: El total debe estar entre el mínimo y máximo")
        return
    
    # Validación de grupos
    if len(grupos_seleccionados) == 0:
        mostrar_error("Debe seleccionar al menos un grupo")
        return
    
    nueva_materia = {
        "codigo": codigo,
        "nombre": nombre,
        "min_slots": min_s,
        "max_slots": max_s,
        "total_slots": total_s,
        "profesor": profesor,
        "aula": aula,
        "grupos": list(grupos_seleccionados)
    }
    
    materias.append(nueva_materia)
    dpg.delete_item("modal_create")
    actualizar_lista()
    mostrar_exito(f"Materia {codigo} agregada correctamente")


def actualizar_materia():
    """Actualiza la materia seleccionada"""
    if not materia_seleccionada:
        return
    
    codigo_original = materia_seleccionada["codigo"]
    nuevo_codigo = dpg.get_value("modal_edit_codigo").strip()
    nombre = dpg.get_value("modal_edit_nombre").strip()
    
    # Validaciones básicas
    if not nuevo_codigo or not nombre:
        mostrar_error("Los campos Código y Nombre son obligatorios")
        return
    
    # Verificar si ya existe el código (excepto el mismo)
    if nuevo_codigo != codigo_original and verificar_duplicado(nuevo_codigo, codigo_original):
        mostrar_error(f"Ya existe una materia con el código {nuevo_codigo}")
        return
    
    # Validación de slots
    min_s = dpg.get_value("modal_edit_min_slots")
    max_s = dpg.get_value("modal_edit_max_slots")
    total_s = dpg.get_value("modal_edit_total_slots")
    profesor = dpg.get_value("modal_edit_combo_profesores")
    aula = dpg.get_value("modal_edit_combo_aulas")
    
    # Validaciones adicionales
    if not profesor:
        mostrar_error("Debe seleccionar un profesor")
        return
        
    if not aula:
        mostrar_error("Debe seleccionar un aula")
        return
    
    # Validación de slots
    if not (min_s <= total_s <= max_s):
        mostrar_error("Error: El total debe estar entre el mínimo y máximo")
        return
    
    # Validación de grupos
    if len(materia_seleccionada.get("grupos", [])) == 0:
        mostrar_error("Debe seleccionar al menos un grupo")
        return
    
    # Actualizar datos
    materia_seleccionada.update({
        "codigo": nuevo_codigo,
        "nombre": nombre,
        "min_slots": min_s,
        "max_slots": max_s,
        "total_slots": total_s,
        "profesor": profesor,
        "aula": aula
        # Los grupos ya se actualizan directamente en el toggle_edit_grupo
    })
    
    dpg.delete_item("modal_edit")
    actualizar_lista()
    mostrar_exito(f"Materia {nuevo_codigo} actualizada correctamente")



def confirmar_eliminar(codigo):
    """Muestra confirmación para eliminar"""
    materia = next((m for m in materias if m["codigo"] == codigo), None)
    if not materia:
        return
    
    with dpg.window(
        modal=True, 
        show=True, 
        tag="modal_confirm", 
        label="Confirmar eliminación",
        width=400, 
        height=200,
        pos=[dpg.get_viewport_width() // 2 - 200, dpg.get_viewport_height() // 2 - 100]
    ):
        dpg.add_text(f"¿Está seguro que desea eliminar la materia?")
        dpg.add_text(f"Código: {materia['codigo']}")
        dpg.add_text(f"Nombre: {materia['nombre']}")
        dpg.add_spacer(height=20)
        
        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Confirmar",
                callback=lambda: eliminar_materia(codigo),
                width=150
            )
            dpg.add_spacer(width=20)
            dpg.add_button(
                label="Cancelar",
                callback=lambda: dpg.delete_item("modal_confirm"),
                width=150
            )

def eliminar_materia(codigo):
    """Elimina una materia"""
    global materias, materia_seleccionada
    
    # Encontrar la materia a eliminar
    materia = next((m for m in materias if m["codigo"] == codigo), None)
    if not materia:
        dpg.delete_item("modal_confirm")
        return
    
    # Eliminar la materia
    materias = [m for m in materias if m["codigo"] != codigo]
    
    # Si es la materia en edición, cerrar panel
    if materia_seleccionada and materia_seleccionada["codigo"] == codigo:
        materia_seleccionada = None
        if dpg.does_item_exist("modal_edit"):
            dpg.delete_item("modal_edit")
    
    actualizar_lista()
    dpg.delete_item("modal_confirm")
    mostrar_exito(f"Materia {codigo} eliminada correctamente")

def limpiar_campos_creacion():
    """Limpia los campos de creación"""
    global grupos_seleccionados
    grupos_seleccionados = set()

def aplicar_filtros():
    """Aplica los filtros de búsqueda"""
    global filtro_nombre, filtro_codigo
    filtro_nombre = dpg.get_value("filtro_nombre")
    filtro_codigo = dpg.get_value("filtro_codigo")
    actualizar_lista()

def limpiar_filtros():
    """Limpia los filtros de búsqueda"""
    dpg.set_value("filtro_codigo", "")
    dpg.set_value("filtro_nombre", "")
    aplicar_filtros()

def mostrar_error(mensaje):
    """Muestra un mensaje de error"""
    with dpg.window(
        modal=True, 
        show=True, 
        tag="modal_mensaje", 
        label="Error",
        width=400, 
        height=150,
        pos=[dpg.get_viewport_width() // 2 - 200, dpg.get_viewport_height() // 2 - 75]
    ):
        dpg.add_text(mensaje, color=(255, 100, 100), wrap=380)
        dpg.add_spacer(height=20)
        dpg.add_button(
            label="Aceptar",
            callback=lambda: dpg.delete_item("modal_mensaje"),
            width=100
        )

def mostrar_exito(mensaje):
    """Muestra un mensaje de éxito"""
    with dpg.window(
        modal=True, 
        show=True, 
        tag="modal_exito", 
        label="Éxito",
        width=400, 
        height=150,
        pos=[dpg.get_viewport_width() // 2 - 200, dpg.get_viewport_height() // 2 - 75]
    ):
        dpg.add_text(mensaje, color=(100, 255, 100), wrap=380)
        dpg.add_spacer(height=20)
        dpg.add_button(
            label="Aceptar",
            callback=lambda: dpg.delete_item("modal_exito"),
            width=100
        )
    
def crear_interfaz_principal():
    """Crea la interfaz principal de la aplicación"""
    
    # Ventana principal
    with dpg.window(tag="ventana_principal", label="Sistema de Gestión de Materias"):
        
        # Cabecera
        with dpg.group():
            dpg.add_text("Sistema de Gestión de Materias", color=(220, 220, 255))
            dpg.add_separator()
        
        # Panel de filtros
        with dpg.collapsing_header(label="Filtros de búsqueda", default_open=True):
            with dpg.group(horizontal=True):
                dpg.add_input_text(label="Código", tag="filtro_codigo", width=150)
                dpg.add_input_text(label="Nombre", tag="filtro_nombre", width=250)
                dpg.add_button(label="Aplicar", callback=aplicar_filtros, width=100)
                dpg.add_button(label="Limpiar", callback=limpiar_filtros, width=100)
        
        # Botón para agregar nueva materia
        with dpg.group(horizontal=True):
            dpg.add_button(label="Nueva Materia", callback=abrir_modal_creacion, width=150)
            dpg.add_spacer(width=20)
            dpg.add_text("", tag="contador_materias")
        
        dpg.add_spacer(height=10)
        
        # Tabla de materias
        with dpg.table(
            tag="lista_materias",
            header_row=True,
            policy=dpg.mvTable_SizingFixedFit,
            resizable=True,
            borders_outerH=True,
            borders_innerV=True,
            borders_innerH=True,
            borders_outerV=True,
            scrollY=True,
            height=500
        ):
            # Definir columnas
            dpg.add_table_column(label="Código", width_fixed=True, width=100)
            dpg.add_table_column(label="Nombre", width_stretch=True, init_width_or_weight=300)
            dpg.add_table_column(label="Acciones", width_fixed=True, width=120)



# Código para iniciar la aplicación
def iniciar_aplicacion():
    crear_interfaz_principal()
    actualizar_lista()
    dpg.setup_dearpygui()
    dpg.set_primary_window("ventana_principal", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    iniciar_aplicacion()