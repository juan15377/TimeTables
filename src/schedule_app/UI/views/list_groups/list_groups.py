import dearpygui.dearpygui as dpg
from typing import Dict, List, Set
import random

# Estructuras de datos
carreras: Set[str] = {"Ingeniería", "Medicina", "Derecho"}
semestres: Set[str] = {"1", "2", "3", "4", "5", "6"}
subgrupos: Set[str] = {"A", "B", "C"}
grupos: List[Dict] = []

dpg.create_context()
dpg.create_viewport(title='Gestión de Grupos', width=1100, height=850)

# Variables de estado
grupo_seleccionado = None
filtros = {"carrera": "", "semestre": "", "subgrupo": "", "nombre": ""}

# Tema optimizado con mejor espaciado
with dpg.theme() as tema_optimizado:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 4, 4)
        dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 4, 4)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 6, 4)

def generar_nombre_grupo(carrera: str, semestre: str, subgrupo: str) -> str:
    """Genera automáticamente el nombre del grupo"""
    return f"{carrera[:3].upper()}-{semestre}{subgrupo}"

def actualizar_lista_grupos():
    """Actualiza la lista de grupos aplicando los filtros"""
    dpg.delete_item("lista_grupos", children_only=True)
    
    for grupo in grupos:
        cumple_filtro = (
            (filtros["carrera"] == "" or grupo["carrera"] == filtros["carrera"]) and
            (filtros["semestre"] == "" or grupo["semestre"] == filtros["semestre"]) and
            (filtros["subgrupo"] == "" or grupo["subgrupo"] == filtros["subgrupo"]) and
            (filtros["nombre"] == "" or filtros["nombre"].lower() in grupo["nombre"].lower())
        )
        
        if cumple_filtro:
            with dpg.group(parent="lista_grupos", horizontal=True):
                dpg.add_selectable(
                    label=f"{grupo['nombre']} | {grupo['carrera']} | Sem {grupo['semestre']} | Grupo {grupo['subgrupo']}",
                    user_data=grupo["id"],
                    callback=lambda s, a, u: seleccionar_grupo(u),
                    width=800
                )
                dpg.add_button(
                    label="✕",
                    user_data=grupo["id"],
                    callback=lambda s, a, u: confirmar_eliminar_grupo(u),
                    width=25
                )

def seleccionar_grupo(grupo_id):
    """Maneja la selección de un grupo"""
    global grupo_seleccionado
    grupo_seleccionado = next(g for g in grupos if g["id"] == grupo_id)
    info = f"Seleccionado: {grupo_seleccionado['nombre']} ({grupo_seleccionado['carrera']} - Sem {grupo_seleccionado['semestre']}{grupo_seleccionado['subgrupo']})"
    dpg.set_value("info_grupo", info)
    dpg.configure_item("btn_eliminar_grupo", enabled=True)

def crear_grupo():
    """Crea un nuevo grupo con nombre generado automáticamente"""
    carrera = dpg.get_value("combo_carreras")
    semestre = dpg.get_value("combo_semestres")
    subgrupo = dpg.get_value("combo_subgrupos")
    
    if carrera and semestre and subgrupo:
        nuevo_id = max(g["id"] for g in grupos) + 1 if grupos else 1
        nombre = generar_nombre_grupo(carrera, semestre, subgrupo)
        
        grupos.append({
            "id": nuevo_id,
            "nombre": nombre,
            "carrera": carrera,
            "semestre": semestre,
            "subgrupo": subgrupo
        })
        actualizar_lista_grupos()

def confirmar_eliminar_grupo(grupo_id):
    """Muestra confirmación para eliminar grupo"""
    grupo = next(g for g in grupos if g["id"] == grupo_id)
    
    with dpg.window(modal=True, show=True, tag="modal_confirm", no_title_bar=True, width=300, height=150):
        dpg.add_text(f"¿Eliminar grupo {grupo['nombre']}?", wrap=280)
        dpg.add_spacer(height=15)
        with dpg.group(horizontal=True):
            dpg.add_button(
                label="Confirmar",
                callback=lambda: eliminar_grupo(grupo_id),
                width=120
            )
            dpg.add_button(
                label="Cancelar",
                callback=lambda: dpg.delete_item("modal_confirm"),
                width=120
            )

def eliminar_grupo(grupo_id):
    """Elimina un grupo"""
    global grupos, grupo_seleccionado
    grupos = [g for g in grupos if g["id"] != grupo_id]
    if grupo_seleccionado and grupo_seleccionado["id"] == grupo_id:
        grupo_seleccionado = None
        dpg.set_value("info_grupo", "Ningún grupo seleccionado")
        dpg.configure_item("btn_eliminar_grupo", enabled=False)
    actualizar_lista_grupos()

def gestionar_catalogos(sender, app_data, user_data):
    """Gestiona los catálogos de carreras, semestres y subgrupos"""
    tipo = user_data["tipo"]
    accion = user_data["accion"]
    valor = dpg.get_value(f"input_{tipo}")
    
    if accion == "agregar" and valor:
        if tipo == "carrera":
            carreras.add(valor)
        elif tipo == "semestre":
            semestres.add(valor)
        elif tipo == "subgrupo":
            subgrupos.add(valor)
        
        dpg.set_value(f"input_{tipo}", "")
        actualizar_combos()
    
    elif accion == "eliminar" and valor:
        if tipo == "carrera":
            carreras.discard(valor)
        elif tipo == "semestre":
            semestres.discard(valor)
        elif tipo == "subgrupo":
            subgrupos.discard(valor)
        
        dpg.set_value(f"input_{tipo}", "")
        actualizar_combos()

def actualizar_combos():
    """Actualiza los combos con los valores actualizados"""
    dpg.configure_item("combo_carreras", items=sorted(carreras))
    dpg.configure_item("combo_semestres", items=sorted(semestres))
    dpg.configure_item("combo_subgrupos", items=sorted(subgrupos))
    dpg.configure_item("filtro_carrera", items=[""] + sorted(carreras))
    dpg.configure_item("filtro_semestre", items=[""] + sorted(semestres))
    dpg.configure_item("filtro_subgrupo", items=[""] + sorted(subgrupos))

def aplicar_filtros():
    """Aplica los filtros de búsqueda"""
    filtros["nombre"] = dpg.get_value("filtro_nombre")
    filtros["carrera"] = dpg.get_value("filtro_carrera")
    filtros["semestre"] = dpg.get_value("filtro_semestre")
    filtros["subgrupo"] = dpg.get_value("filtro_subgrupo")
    actualizar_lista_grupos()

# Interfaz principal mejor organizada
with dpg.window(label="Gestión de Grupos", width=1080, height=830, tag="main_window"):
    # Panel de catálogos
    with dpg.collapsing_header(label="Administrar Catálogos", default_open=True):
        with dpg.tab_bar():
            with dpg.tab(label="Carreras"):
                with dpg.group(horizontal=True):
                    dpg.add_input_text(label="Nombre", tag="input_carrera", width=200)
                    dpg.add_button(
                        label="Agregar",
                        user_data={"tipo": "carrera", "accion": "agregar"},
                        callback=gestionar_catalogos,
                        width=80
                    )
                    dpg.add_button(
                        label="Eliminar",
                        user_data={"tipo": "carrera", "accion": "eliminar"},
                        callback=gestionar_catalogos,
                        width=80
                    )
            
            with dpg.tab(label="Semestres"):
                with dpg.group(horizontal=True):
                    dpg.add_input_text(label="Número", tag="input_semestre", width=200)
                    dpg.add_button(
                        label="Agregar",
                        user_data={"tipo": "semestre", "accion": "agregar"},
                        callback=gestionar_catalogos,
                        width=80
                    )
                    dpg.add_button(
                        label="Eliminar",
                        user_data={"tipo": "semestre", "accion": "eliminar"},
                        callback=gestionar_catalogos,
                        width=80
                    )
            
            with dpg.tab(label="Subgrupos"):
                with dpg.group(horizontal=True):
                    dpg.add_input_text(label="Letra", tag="input_subgrupo", width=200)
                    dpg.add_button(
                        label="Agregar",
                        user_data={"tipo": "subgrupo", "accion": "agregar"},
                        callback=gestionar_catalogos,
                        width=80
                    )
                    dpg.add_button(
                        label="Eliminar",
                        user_data={"tipo": "subgrupo", "accion": "eliminar"},
                        callback=gestionar_catalogos,
                        width=80
                    )
    
    # Panel de creación de grupos
    with dpg.group(horizontal=True):
        dpg.add_text("Crear Grupo:")
        dpg.add_combo(label="Carrera", items=sorted(carreras), tag="combo_carreras", width=180)
        dpg.add_combo(label="Semestre", items=sorted(semestres), tag="combo_semestres", width=100)
        dpg.add_combo(label="Subgrupo", items=sorted(subgrupos), tag="combo_subgrupos", width=100)
        dpg.add_button(label="Generar Grupo", callback=crear_grupo, width=120)
        dpg.add_text("(Nombre generado automáticamente)")
    
    # Filtros mejor organizados
    with dpg.table(header_row=False, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
        dpg.add_table_column(width_fixed=True, init_width_or_weight=200)
        dpg.add_table_column(width_fixed=True, init_width_or_weight=200)
        dpg.add_table_column(width_fixed=True, init_width_or_weight=200)
        dpg.add_table_column(width_fixed=True, init_width_or_weight=200)
        
        with dpg.table_row():
            dpg.add_input_text(label="Filtrar por nombre", tag="filtro_nombre", width=180, callback=aplicar_filtros)
            dpg.add_combo(label="Carrera", items=[""] + sorted(carreras), tag="filtro_carrera", width=180, callback=aplicar_filtros)
            dpg.add_combo(label="Semestre", items=[""] + sorted(semestres), tag="filtro_semestre", width=180, callback=aplicar_filtros)
            dpg.add_combo(label="Subgrupo", items=[""] + sorted(subgrupos), tag="filtro_subgrupo", width=180, callback=aplicar_filtros)
    
    with dpg.group(horizontal=True):
        dpg.add_button(
            label="Limpiar filtros",
            callback=lambda: [
                dpg.set_value("filtro_nombre", ""),
                dpg.set_value("filtro_carrera", ""),
                dpg.set_value("filtro_semestre", ""),
                dpg.set_value("filtro_subgrupo", ""),
                aplicar_filtros()
            ],
            width=120
        )
        dpg.add_text("", tag="contador_grupos")
    
    # Lista de grupos con mejor espaciado
    with dpg.child_window(height=400, tag="lista_grupos", border=True):
        actualizar_lista_grupos()
    
    # Panel inferior
    with dpg.group(horizontal=True):
        dpg.add_text("", tag="info_grupo")
        dpg.add_button(
            label="Eliminar grupo seleccionado",
            tag="btn_eliminar_grupo",
            enabled=False,
            callback=lambda: confirmar_eliminar_grupo(grupo_seleccionado["id"]) if grupo_seleccionado else None,
            width=180
        )

# Configuración final
dpg.bind_theme(tema_optimizado)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()