import dearpygui.dearpygui as dpg

# Inicializar DearPyGUI
dpg.create_context()
dpg.create_viewport(title="Sistema de Gestión Académica", width=1200, height=700, resizable=True)

# Datos de ejemplo
horas = ["7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]
dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

profesores = ["García Martínez, Ana", "Fernández López, Carlos", "Rodríguez Sánchez, María", 
              "González Pérez, Juan", "Martínez Gómez, Elena"]
grupos = ["1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B"]
aulas = ["A101", "A102", "A103", "B201", "B202", "B203", "C301", "C302", "C303"]

materias = {
    "MAT101": "Matemáticas Básicas",
    "FIS102": "Física General",
    "QUI103": "Química Orgánica",
    "BIO104": "Biología Celular",
    "HIS201": "Historia Contemporánea"
}

# Estado y funciones de utilidad
seleccion_actual = {"profesor": None, "grupo": None, "aula": None, "materia": None}
celda_seleccionada = [None, None]  # [día, hora]
celdas_asignadas = {}  # (dia, hora): {"materia": "", "profesor": "", "grupo": "", "aula": ""}

last_resize_check = [0, 0]  # [width, height]

def resize_check():
    """Comprueba si ha cambiado el tamaño de la ventana y actualiza la UI si es necesario"""
    global last_resize_check
    
    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()
    
    # Solo actualizar si cambiaron las dimensiones
    if viewport_width != last_resize_check[0] or viewport_height != last_resize_check[1]:
        last_resize_check = [viewport_width, viewport_height]
        
        # Actualizar dimensiones de la ventana principal
        dpg.set_item_width("ventana_principal", viewport_width - 20)
        dpg.set_item_height("ventana_principal", viewport_height - 20)
        
        # Calcular dimensiones para los paneles divididos
        panel_izquierdo_width = int(viewport_width * 0.6) - 20
        panel_derecho_width = int(viewport_width * 0.4) - 20
        panel_height = viewport_height - 40
        
        # Actualizar tamaños de los paneles
        dpg.set_item_width("panel_izquierdo", panel_izquierdo_width)
        dpg.set_item_height("panel_izquierdo", panel_height)
        dpg.set_item_width("panel_derecho", panel_derecho_width)
        dpg.set_item_height("panel_derecho", panel_height)
        
        # Ajustar componentes dentro del panel derecho
        for lista_id in ["lista_profesores", "lista_grupos", "lista_aulas"]:
            dpg.set_item_width(lista_id, panel_derecho_width - 20)
        
        # Ajustar los campos de búsqueda
        search_width = panel_derecho_width - 80
        for search_id in ["buscar_profesor", "buscar_grupo", "buscar_aula"]:
            dpg.set_item_width(search_id, search_width)
        
        # Ajustar los contenedores de listas
        contenedor_width = panel_derecho_width - 40
        for cont_id in ["contenedor_profesores", "contenedor_grupos", "contenedor_aulas"]:
            dpg.set_item_width(cont_id, contenedor_width)
        
        # Ajustar los botones en listas
        btn_width = panel_derecho_width - 60
        for tipo, lista in [("profesor", profesores), ("grupo", grupos), ("aula", aulas)]:
            for i, _ in enumerate(lista):
                dpg.set_item_width(f"btn_{tipo}_{i}", btn_width)
        
        # Ajustar botones de navegación
        tab_btn_width = (panel_derecho_width - 20) // 3
        dpg.set_item_width("btn_profesores", tab_btn_width)
        dpg.set_item_width("btn_grupos", tab_btn_width)
        dpg.set_item_width("btn_aulas", tab_btn_width)
    
    return 0  # Continuar verificando

def filtrar_lista(sender, app_data, user_data):
    """Filtra los elementos en la lista según el texto de búsqueda"""
    tipo, items = user_data
    texto_busqueda = app_data.lower()
    
    # Ocultar/mostrar elementos según coincidencia
    for i, item in enumerate(items):
        if texto_busqueda == "" or texto_busqueda in item.lower():
            dpg.configure_item(f"item_{tipo}_{i}", show=True)
        else:
            dpg.configure_item(f"item_{tipo}_{i}", show=False)

def mostrar_lista(tipo):
    """Muestra la lista correspondiente y oculta las demás"""
    listas = ["lista_profesores", "lista_grupos", "lista_aulas"]
    for lista in listas:
        if lista == f"lista_{tipo}":
            dpg.configure_item(lista, show=True)
        else:
            dpg.configure_item(lista, show=False)

def seleccionar_item(sender, app_data, user_data):
    """Actualiza la selección cuando se hace clic en un ítem de las listas"""
    tipo, valor = user_data
    seleccion_actual[tipo] = valor
    # Actualizar la visualización de la selección actual
    dpg.set_value(f"{tipo}_seleccionado", f"{tipo.capitalize()}: {valor}")
    
    # Resaltar visualmente el botón seleccionado
    lista_items = profesores if tipo == "profesor" else (grupos if tipo == "grupo" else aulas)
    for i, item in enumerate(lista_items):
        if item == valor:
            dpg.configure_item(f"btn_{tipo}_{i}", color=[0, 200, 0])
        else:
            dpg.configure_item(f"btn_{tipo}_{i}", color=[0, 120, 255])

def celda_click(sender, app_data, user_data):
    """Maneja el clic en una celda de la cuadrícula"""
    dia, hora = user_data
    celda_seleccionada[0] = dia
    celda_seleccionada[1] = hora
    
    # Actualizar la visualización de la celda seleccionada
    dpg.set_value("celda_seleccionada", f"Día: {dia}, Hora: {hora}")
    
    # Mostrar información si la celda ya tiene asignación
    clave = (dia, hora)
    if clave in celdas_asignadas:
        datos = celdas_asignadas[clave]
        dpg.set_value("materia_seleccionada", f"Materia: {datos['materia']}")
        dpg.set_value("profesor_seleccionado", f"Profesor: {datos['profesor']}")
        dpg.set_value("grupo_seleccionado", f"Grupo: {datos['grupo']}")
        dpg.set_value("aula_seleccionada", f"Aula: {datos['aula']}")
    else:
        # Limpiar selecciones previas
        dpg.set_value("materia_seleccionada", "Materia: No seleccionada")
        dpg.set_value("profesor_seleccionado", "Profesor: No seleccionado")
        dpg.set_value("grupo_seleccionado", "Grupo: No seleccionado")
        dpg.set_value("aula_seleccionada", "Aula: No seleccionada")

def asignar_materia():
    """Asigna la materia, profesor, grupo y aula a la celda seleccionada"""
    if celda_seleccionada[0] is None or celda_seleccionada[1] is None:
        return
    
    dia, hora = celda_seleccionada
    clave = (dia, hora)
    
    # Verificar si tenemos todos los datos necesarios
    if not all([seleccion_actual["materia"], seleccion_actual["profesor"], 
                seleccion_actual["grupo"], seleccion_actual["aula"]]):
        return
    
    # Actualizar la asignación
    celdas_asignadas[clave] = {
        "materia": seleccion_actual["materia"],
        "profesor": seleccion_actual["profesor"],
        "grupo": seleccion_actual["grupo"],
        "aula": seleccion_actual["aula"]
    }
    
    # Actualizar la celda en la UI
    cell_tag = f"celda_{dia}_{hora}"
    datos = celdas_asignadas[clave]
    texto = f"{datos['materia']}\n{datos['profesor']}\nGrupo: {datos['grupo']}\nAula: {datos['aula']}"
    dpg.set_value(cell_tag, texto)
    
    # Cambiar color de fondo (simulado con un texto de color)
    dpg.configure_item(cell_tag, color=[0, 120, 0])

def seleccionar_materia(sender, app_data, user_data):
    """Selecciona una materia de la lista desplegable"""
    codigo, nombre = user_data
    seleccion_actual["materia"] = nombre
    dpg.set_value("materia_seleccionada", f"Materia: {nombre}")
    
    # Resaltar visualmente el botón seleccionado
    for cod in materias:
        if cod == codigo:
            dpg.configure_item(f"btn_materia_{cod}", color=[0, 200, 0])
        else:
            dpg.configure_item(f"btn_materia_{cod}", color=[0, 120, 255])

def limpiar_seleccion():
    """Limpia la selección actual y la celda seleccionada"""
    for tipo in seleccion_actual:
        seleccion_actual[tipo] = None
        dpg.set_value(f"{tipo}_seleccionado", f"{tipo.capitalize()}: No seleccionado")
    
    celda_seleccionada[0] = None
    celda_seleccionada[1] = None
    dpg.set_value("celda_seleccionada", "Ninguna celda seleccionada")
    
    # Restablecer colores de botones
    for cod in materias:
        dpg.configure_item(f"btn_materia_{cod}", color=[0, 120, 255])
    
    for tipo, lista in [("profesor", profesores), ("grupo", grupos), ("aula", aulas)]:
        for i, _ in enumerate(lista):
            dpg.configure_item(f"btn_{tipo}_{i}", color=[0, 120, 255])

def eliminar_asignacion():
    """Elimina la asignación de la celda seleccionada"""
    if celda_seleccionada[0] is None or celda_seleccionada[1] is None:
        return
    
    dia, hora = celda_seleccionada
    clave = (dia, hora)
    
    if clave in celdas_asignadas:
        del celdas_asignadas[clave]
        cell_tag = f"celda_{dia}_{hora}"
        dpg.set_value(cell_tag, "")
        dpg.configure_item(cell_tag, color=[255, 255, 255])
        limpiar_seleccion()

# Ventana principal con divisón en dos paneles
with dpg.window(label="Sistema de Gestión Académica", pos=(0, 0), width=1180, height=680, tag="ventana_principal"):
    
    # Crear un grupo horizontal para dividir la pantalla
    with dpg.group(horizontal=True):
        
        # --- PANEL IZQUIERDO: CUADRÍCULA DE MATERIAS ---
        with dpg.child_window(width=700, height=660, border=False, tag="panel_izquierdo"):
            dpg.add_text("CUADRÍCULA DE HORARIOS", color=[0, 120, 255])
            dpg.add_separator()
            
            # Encabezado de días
            with dpg.table(header_row=True, borders_innerH=True, borders_outerH=True, 
                          borders_innerV=True, borders_outerV=True, resizable=True, tag="tabla_horarios"):
                
                # Configurar columnas
                dpg.add_table_column(label="Hora")
                for dia in dias:
                    dpg.add_table_column(label=dia)
                
                # Filas con horarios
                for hora in horas:
                    with dpg.table_row():
                        dpg.add_text(hora)
                        
                        # Celdas para cada día
                        for dia in dias:
                            with dpg.table_cell():
                                cell_tag = f"celda_{dia}_{hora}"
                                dpg.add_text("", tag=cell_tag, wrap=150)
                                
                                # Área clicable sobre la celda
                                with dpg.item_handler_registry() as handler:
                                    dpg.add_item_clicked_handler(callback=celda_click, user_data=(dia, hora))
                                dpg.bind_item_handler_registry(cell_tag, handler)
            
            # Área de información y acciones
            dpg.add_spacer(height=10)
            dpg.add_text("CELDA SELECCIONADA", color=[0, 120, 255])
            dpg.add_text("Ninguna celda seleccionada", tag="celda_seleccionada")
            
            dpg.add_spacer(height=5)
            dpg.add_separator()
            dpg.add_spacer(height=5)
            
            # Selección de materia
            dpg.add_text("SELECCIÓN ACTUAL", color=[0, 120, 255])
            dpg.add_text("Materia: No seleccionada", tag="materia_seleccionada")
            dpg.add_text("Profesor: No seleccionado", tag="profesor_seleccionado")
            dpg.add_text("Grupo: No seleccionado", tag="grupo_seleccionado")
            dpg.add_text("Aula: No seleccionada", tag="aula_seleccionada")
            
            dpg.add_spacer(height=10)
            
            # Botones de acción
            with dpg.group(horizontal=True):
                dpg.add_button(label="Asignar", callback=asignar_materia, width=100)
                dpg.add_button(label="Eliminar", callback=eliminar_asignacion, width=100)
                dpg.add_button(label="Limpiar Selección", callback=limpiar_seleccion, width=150)
            
            # Combo para seleccionar materias
            dpg.add_spacer(height=10)
            dpg.add_text("Seleccionar Materia:")
            with dpg.group(horizontal=True):
                for codigo, nombre in materias.items():
                    dpg.add_button(label=f"{codigo}", callback=seleccionar_materia, 
                                   user_data=(codigo, nombre), width=80, tag=f"btn_materia_{codigo}")
            
        # --- PANEL DERECHO: RECURSOS (PROFESORES, GRUPOS, AULAS) ---
        with dpg.child_window(width=460, height=660, border=False, tag="panel_derecho"):
            dpg.add_text("RECURSOS", color=[0, 120, 255])
            dpg.add_separator()
            
            # Pestañas para cambiar entre recursos
            with dpg.group(horizontal=True):
                dpg.add_button(label="Profesores", callback=lambda: mostrar_lista("profesores"), 
                              width=150, tag="btn_profesores")
                dpg.add_button(label="Grupos", callback=lambda: mostrar_lista("grupos"), 
                              width=150, tag="btn_grupos")
                dpg.add_button(label="Aulas", callback=lambda: mostrar_lista("aulas"), 
                              width=150, tag="btn_aulas")
            
            dpg.add_spacer(height=10)
            
            # Lista de profesores
            with dpg.child_window(width=440, height=550, tag="lista_profesores"):
                dpg.add_text("LISTA DE PROFESORES", color=[0, 120, 255])
                dpg.add_separator()
                
                # Campo de búsqueda
                with dpg.group(horizontal=True):
                    dpg.add_text("Buscar:")
                    dpg.add_input_text(width=300, tag="buscar_profesor", 
                                      callback=filtrar_lista, 
                                      user_data=("profesor", profesores))
                
                dpg.add_spacer(height=10)
                
                # Contenedor para la lista scrollable
                with dpg.child_window(width=420, height=450, tag="contenedor_profesores"):
                    # Lista con selección
                    for i, profesor in enumerate(profesores):
                        with dpg.group(horizontal=True, tag=f"item_profesor_{i}"):
                            dpg.add_button(label=profesor, width=350, tag=f"btn_profesor_{i}", 
                                          callback=seleccionar_item, 
                                          user_data=("profesor", profesor))
            
            # Lista de grupos (inicialmente oculta)
            with dpg.child_window(width=440, height=550, tag="lista_grupos", show=False):
                dpg.add_text("LISTA DE GRUPOS", color=[0, 120, 255])
                dpg.add_separator()
                
                # Campo de búsqueda
                with dpg.group(horizontal=True):
                    dpg.add_text("Buscar:")
                    dpg.add_input_text(width=300, tag="buscar_grupo", 
                                      callback=filtrar_lista, 
                                      user_data=("grupo", grupos))
                
                dpg.add_spacer(height=10)
                
                # Contenedor para la lista scrollable
                with dpg.child_window(width=420, height=450, tag="contenedor_grupos"):
                    # Lista con selección
                    for i, grupo in enumerate(grupos):
                        with dpg.group(horizontal=True, tag=f"item_grupo_{i}"):
                            dpg.add_button(label=grupo, width=350, tag=f"btn_grupo_{i}", 
                                          callback=seleccionar_item, 
                                          user_data=("grupo", grupo))
            
            # Lista de aulas (inicialmente oculta)
            with dpg.child_window(width=440, height=550, tag="lista_aulas", show=False):
                dpg.add_text("LISTA DE AULAS", color=[0, 120, 255])
                dpg.add_separator()
                
                # Campo de búsqueda
                with dpg.group(horizontal=True):
                    dpg.add_text("Buscar:")
                    dpg.add_input_text(width=300, tag="buscar_aula", 
                                      callback=filtrar_lista, 
                                      user_data=("aula", aulas))
                
                dpg.add_spacer(height=10)
                
                # Contenedor para la lista scrollable
                with dpg.child_window(width=420, height=450, tag="contenedor_aulas"):
                    # Lista con selección
                    for i, aula in enumerate(aulas):
                        with dpg.group(horizontal=True, tag=f"item_aula_{i}"):
                            dpg.add_button(label=aula, width=350, tag=f"btn_aula_{i}", 
                                          callback=seleccionar_item, 
                                          user_data=("aula", aula))

# Configurar revisión periódica del tamaño
dpg.set_viewport_resize_callback(resize_check)

# Inicializar la aplicación
dpg.setup_dearpygui()
dpg.show_viewport()

# Ejecutar el ajuste inicial de tamaño
resize_check()

dpg.start_dearpygui()
dpg.destroy_context()