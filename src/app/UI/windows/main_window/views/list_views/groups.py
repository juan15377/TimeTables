import dearpygui.dearpygui as dpg
from typing import Dict, List, Set
import random

from src.app.UI.components.windows_manager import windows_manager
from src.app.database import database_manager
from src.app.UI.components.schedule_availability.schedule_availability import HorarioDisponibilidadApp
from src.app.UI.components.items_groups_manager import ItemsGroupsManager, get_id
from src.app.UI.windows_tags import SUBJECTS_MANAGER_WINDOW_TAG, SCHEDULE_AVAILABILITY_WINDOW_TAG
import dearpygui.dearpygui as dpg
from typing import Dict, List, Set
import random

import re 

class GroupCatalogManager():
    """
    Sender - {combo_edit_careers, combo_edit_semesters, combo_edit_subgroups}
    """
    
    def __init__(self, db, on_update_items):
        self.db = db 
        self.on_update_items = on_update_items
        
        self.combo_careers_tag = "combo_edit_careers"
        self.combo_semesters_tag = "combo_edit_semesters"
        self.combo_subgroups_tag = "combo_edit_subgroups"
        
        
        self.items = ItemsGroupsManager(db)
        

        #self.update()
    
        
    def setup_ui(self):
        with dpg.tab_bar():
            with dpg.tab(label="Carreras"):
                with dpg.group(horizontal=True):
                    dpg.add_input_text(label="Nombre", tag="input_carrera", width=300)
                    dpg.add_button(
                        label="Agregar",
                        user_data={"tipo": "carrera", "accion": "agregar"},
                        callback=self.gestionar_catalogos,
                        width=80
                    )
                    dpg.add_combo(
                        items= list(self.items.get_careers()),
                        width=300,
                        id = self.combo_careers_tag
                    )
                    dpg.add_button(
                        label="Eliminar",
                        user_data={"tipo": "carrera", "accion": "eliminar"},
                        callback=self.gestionar_catalogos,
                        width=80
                    )
            
            with dpg.tab(label="Semestres"):
                with dpg.group(horizontal=True):
                    dpg.add_input_text(label="Número", tag="input_semestre", width=200)
                    dpg.add_button(
                        label="Agregar",
                        user_data={"tipo": "semestre", "accion": "agregar"},
                        callback=self.gestionar_catalogos,
                        width=80
                    )
                    
                    dpg.add_combo(
                        items= list(self.items.get_semesters()),
                        width=300,
                        id = self.combo_semesters_tag
                    )
                    dpg.add_button(
                        label="Eliminar",
                        user_data={"tipo": "semestre", "accion": "eliminar"},
                        callback=self.gestionar_catalogos,
                        width=80
                    )
            
            with dpg.tab(label="Subgrupos"):
                with dpg.group(horizontal=True):
                    dpg.add_input_text(label="Letra", tag="input_subgrupo", width=200)
                    dpg.add_button(
                        label="Agregar",
                        user_data={"tipo": "subgrupo", "accion": "agregar"},
                        callback=self.gestionar_catalogos,
                        width=80
                    )
                    dpg.add_combo(
                        items= list(self.items.get_subgroups()),
                        width=300,
                        id = self.combo_subgroups_tag
                    )
                    dpg.add_button(
                        label="Eliminar",
                        user_data={"tipo": "subgrupo", "accion": "eliminar"},
                        callback=self.gestionar_catalogos,
                        width=80
                    )
        self.update()
        
    def gestionar_catalogos(self, sender, app_data, user_data):
        """Gestiona los catálogos de carreras, semestres y subgrupos"""
        tipo = user_data["tipo"]
        accion = user_data["accion"]
        valor = dpg.get_value(f"input_{tipo}")
        
        if accion == "agregar" and valor:
            if tipo == "carrera":
                self.db.groups.careers.new(valor)
                self.items.update_careers()
            elif tipo == "semestre":
                self.db.groups.semesters.new(valor)
                self.items.update_semesters()
            elif tipo == "subgrupo":
                self.db.groups.subgroups.new(valor)
                self.items.update_subgroups()
            
            dpg.set_value(f"input_{tipo}", "")
            self.update_combos()
        
        elif accion == "eliminar" and valor:
            if tipo == "carrera":
                self.carreras.discard(valor)
            elif tipo == "semestre":
                self.semestres.discard(valor)
            elif tipo == "subgrupo":
                self.subgrupos.discard(valor)
            
            dpg.set_value(f"input_{tipo}", "")
            self.update_combos()
            
        self.on_update_items(1,1,1)

    def update(self):
        
        self.items.update()
        
        self.update_combos()


    def update_combos(self):
        """Actualiza los combos con los valores actualizados"""
        dpg.configure_item(self.combo_careers_tag, items=sorted(self.items.get_careers()))
        dpg.configure_item(self.combo_semesters_tag, items=sorted(self.items.get_semesters()))
        dpg.configure_item(self.combo_subgroups_tag, items=sorted(self.items.get_subgroups()))
    

class CreateGroupUI():
    
    def __init__(self, db, on_create_group):
        self.db = db 
        self.on_create_group = on_create_group
        
        self.combo_careers_tag =  "selected_career_combo_for_group_creation"
        self.combo_semesters_tag = "selected_semester_combo_for_group_creation"
        self.combo_subgroups_tag = "selected_subgroup_combo_for_group_creation"
        
        self.items = ItemsGroupsManager(db)
        

        

    def setup_ui(self):
        
        with dpg.group(horizontal=True):

            dpg.add_text("Carrera")
            dpg.add_combo(items=sorted(self.items.get_careers()), tag= self.combo_careers_tag, width=250)
                
            dpg.add_text("Semestre")
            dpg.add_combo(items=sorted(self.items.get_semesters()), tag=self.combo_semesters_tag, width=250)
            
            dpg.add_text("Subgrupo")
            dpg.add_combo(items=sorted(self.items.get_subgroups()), tag=self.combo_subgroups_tag, width=250)
            
            dpg.add_button(label="+", callback=self.create_group,)
        pass 
    
    
    def create_group(self, sender, app_data, user_data):
        
        
        
        career_id = get_id(dpg.get_value(self.combo_careers_tag))
        semester_id = get_id(dpg.get_value(self.combo_semesters_tag))
        subgroup_id = get_id(dpg.get_value(self.combo_subgroups_tag))
        
        print(career_id, semester_id, subgroup_id)
        
        
        self.db.groups.new(career_id, semester_id, subgroup_id)
        print("se creo nuevo grupo")
        
        self.on_create_group(sender, app_data, user_data)
        
        
        
        pass
        
        
    def update_combos(self):
        dpg.configure_item(self.combo_careers_tag, items=sorted(self.items.get_careers()))
        dpg.configure_item(self.combo_semesters_tag, items=sorted(self.items.get_semesters()))
        dpg.configure_item(self.combo_subgroups_tag, items=sorted(self.items.get_subgroups()))
    
        
        pass 
    
    
    def update(self):
        self.update_combos()
        pass 

class GroupsManager:
    """
    Clase que gestiona grupos académicos con una interfaz gráfica usando DearPyGui.
    Permite crear, filtrar y eliminar grupos basados en carrera, semestre y subgrupo.
    También gestiona materias y horarios para cada grupo.
    """
    
    def __init__(self, db):
        # Estructuras de datos{"Ingeniería", "Medicina", "Derecho"}
        self.db = db
        
        
        self.table_groups_tag = "table_groups_manager"
        
        
        def on_new_group(sender, app_data, user_data):
            self.actualizar_combos()
            self.filtrar_grupos()
            self.actualizar_lista_grupos()
            self.limpiar_filtros()
            print("SE AGREGO UN NUEVO GRUPO")
            pass  
        
        def on_update_items(sender, app_data, user_data):
            self.create_group.update()
            self.aplicar_filtros()
            self.actualizar_combos()
            
            
        self.items = ItemsGroupsManager(db)
        
        self.grupos: List[Dict] = self.items.get_groups()
        self.grupos_filtrados = self.grupos 
        
        
        self.create_group = CreateGroupUI(self.db, on_new_group)
        
        
        self.group_catalog_manager = GroupCatalogManager(db, on_update_items)

        
        
        self.combo_careers_tag =  "selected_career_combo_for_group_filter"
        self.combo_semesters_tag = "selected_semester_combo_for_group_filter"
        self.combo_subgroups_tag = "selected_subgroup_combo_for_group_filter"
        
        

        self.pagina_actual = 1
        self.elementos_por_pagina = 10  # Ajustable según necesidad
        self.total_paginas = 1
        self.filter_groups = []
        
        
        # Variables de estado
        self.grupo_seleccionado = None
        self.filtros = {"carrera": "", "semestre": "", "subgrupo": "", "nombre": ""}
        
        # Variables para paginación
        self.pagina_actual = 1
        self.elementos_por_pagina = 100  # Ajustable según necesidad
        self.total_paginas = 1
        self.grupos_filtrados = []
        
        # Inicialización de DearPyGui
        dpg.create_viewport(title='Gestión de Grupos', width=1100, height=850)
        
        # Crear tema
        self._crear_temas()
        #self.actualizar_lista_grupos()
                
        """Crea un tema personalizado con mejor espaciado"""
    def _crear_temas(self):
        """Crea los temas de la interfaz"""
        # Tema principal
        with dpg.theme() as self.tema_principal:
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
        with dpg.theme() as self.tema_eliminar:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [230, 100, 100, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [255, 130, 130, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [210, 80, 80, 255])
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)

        # Tema para botones de acción positiva
        with dpg.theme() as self.tema_accion:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [100, 180, 130, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [130, 210, 160, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [80, 160, 110, 255])
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)

        # Tema para botones de detalles primarios
        with dpg.theme() as self.tema_detalle1:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [70, 100, 180, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [100, 160, 210, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [50, 110, 160, 255])
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)

        # Tema para botones de detalles secundarios
        with dpg.theme() as self.tema_detalle2:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [180, 120, 70, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [210, 150, 100, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [160, 100, 50, 255])
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
        
    
    def setup_ui(self, parent):
        """Construye toda la interfaz de usuario"""
        with dpg.group(parent = parent):
            # Panel de catálogos
            # ! catalogos 
            with dpg.collapsing_header(label="Administrar Catálogos", default_open=True):
                self.group_catalog_manager.setup_ui()

            # ! crear un grupo 
            with dpg.collapsing_header(label="Crear Grupo", default_open=True):
                                
                self.create_group.setup_ui()
            
            
            # ! filters and list groups
            with dpg.collapsing_header(label="Filtros", default_open=True):

                with dpg.group(horizontal=True):
                    
                    dpg.add_text("Carrera")
                    dpg.add_combo(items=[""] + sorted(self.items.get_careers()), tag=self.combo_careers_tag, width=250, callback=self.aplicar_filtros)
                    
                    dpg.add_text("Semestre")
                    dpg.add_combo(items=[""] + sorted(self.items.get_semesters()), tag=self.combo_semesters_tag, width=250, callback=self.aplicar_filtros)
                        
                    dpg.add_text("Subgrupo")
                    dpg.add_combo(items=[""] + sorted(self.items.get_subgroups()), tag=self.combo_subgroups_tag, width=250, callback=self.aplicar_filtros)
                    
                with dpg.group(horizontal=True):
                    dpg.add_input_text(label="Filtrar por nombre", tag="filtro_nombre", width=250, callback=self.aplicar_filtros)

                    dpg.add_button(
                        label="Limpiar filtros",
                        callback=self.limpiar_filtros,
                        width=120
                    )
                    dpg.add_text("", tag="contador_grupos")


             # Controles de paginación
            dpg.add_spacing()
            with dpg.group(horizontal=True, tag="controles_paginacion"):
                dpg.add_button(
                    label="<<",
                    callback=lambda: self.cambiar_pagina("primera"),
                    tag="btn_primera_pagina",
                    width=40
                )
                
                dpg.add_button(
                    label="<",
                    callback=lambda: self.cambiar_pagina("anterior"),
                    tag="btn_anterior_pagina",
                    width=40
                )
                
                dpg.add_text("Página: 0/0", tag="texto_pagina")
                dpg.add_button(
                    label=">",
                    callback=lambda: self.cambiar_pagina("siguiente"),
                    tag="btn_siguiente_pagina",
                    width=40
                )
                
                dpg.add_button(
                    label=">>",
                    callback=lambda: self.cambiar_pagina("ultima"),
                    tag="btn_ultima_pagina",
                    width=40
                )
                
                dpg.add_spacer(width=20)
                dpg.add_combo(
                    label="Elementos por página",
                    items=["10", "25", "50", "100"],
                    default_value="10",
                    callback=lambda s, a: self.cambiar_elementos_por_pagina(int(a)),
                    width=100
                )
                
                dpg.add_input_int(
                    label="Ir a página",
                    width=80,
                    min_value=1,
                    max_value=9999,
                    default_value=1,
                    tag="input_ir_pagina"
                )
                dpg.add_button(
                    label="Ir",
                    callback=lambda: self.ir_a_pagina(dpg.get_value("input_ir_pagina")),
                    width=40
                )
            
            # Lista de grupos con mejor espaciado
            with dpg.child_window(height=600, tag="lista_groups_manager", border=True):
                pass  # Se llenará con actualizar_lista_grupos
            
            self.aplicar_filtros()
            
    
    def _callback_eliminar_seleccionado(self):
        """Callback para el botón de eliminar grupo seleccionado"""
        if self.grupo_seleccionado:
            self.confirmar_eliminar_grupo(self.grupo_seleccionado["id"])
    
    def limpiar_filtros(self):
        """Limpia todos los filtros aplicados"""
        dpg.set_value("filtro_nombre", "")
        dpg.set_value(self.combo_careers_tag, "")
        dpg.set_value(self.combo_semesters_tag, "")
        dpg.set_value(self.combo_subgroups_tag, "")
        self.aplicar_filtros()
    
    def generar_nombre_grupo(self, carrera: str, semestre: str, subgrupo: str) -> str:
        """Genera automáticamente el nombre del grupo"""
        return f"{carrera[:3].upper()}-{semestre}{subgrupo}"
    
    def filtrar_grupos(self):
        """Filtra los grupos según los criterios aplicados"""
        self.grupos_filtrados = self.items.get_filtered_groups(
            self.filtros["nombre"].lower(),
            get_id(self.filtros["carrera"]),
            get_id(self.filtros["semestre"]),
            get_id(self.filtros["subgrupo"])
        )
        
        print(self.grupos_filtrados)

        # Actualizar total de páginas
        self.total_paginas = max(1, (len(self.grupos_filtrados) + self.elementos_por_pagina - 1) // self.elementos_por_pagina)
        
        # Asegurar que la página actual sea válida
        if self.pagina_actual > self.total_paginas:
            self.pagina_actual = self.total_paginas
        
        # Actualizar contador
        dpg.set_value("contador_grupos", f"Mostrando {len(self.grupos_filtrados)} de {len(self.grupos)} grupos")
        
        # Actualizar indicador de página
        dpg.set_value("texto_pagina", f"Página: {self.pagina_actual}/{self.total_paginas}")
        
        
  

    
    def actualizar_lista_grupos(self):
        """Actualiza la lista de grupos mostrando solo la página actual"""
        # Primero filtramos los grupos
        self.filtrar_grupos()
        
        # Limpiamos la lista actual
        dpg.delete_item("lista_groups_manager", children_only=True)
        
        # Calculamos los índices de inicio y fin para la página actual
        inicio = (self.pagina_actual - 1) * self.elementos_por_pagina
        fin = min(inicio + self.elementos_por_pagina, len(self.grupos_filtrados))
        
        # Mostramos solo los grupos de la página actual
        
                    # Agregar encabezados de tabla
        with dpg.table(header_row=True, borders_innerH=True, borders_outerH=True,
                        borders_innerV=True, borders_outerV=True, tag=self.table_groups_tag, 
                        parent="lista_groups_manager"):
                
            # Definir columnas
            dpg.add_table_column(label="ID", width_fixed=True, width=50)
            dpg.add_table_column(label="Carrera", width_fixed=True, width=100)
            dpg.add_table_column(label="Semestre", width_stretch=True, init_width_or_weight=250)
            dpg.add_table_column(label="Subgrupo", width_fixed=True, width=150)
            
            dpg.add_table_column(label="PROGRESO", width_fixed=True,init_width_or_weight=100)
            dpg.add_table_column(label="Materias", width_fixed=True, init_width_or_weight=120)
            dpg.add_table_column(label="Horario", width_fixed=True, init_width_or_weight=120)
            dpg.add_table_column(label="Eliminar", width_fixed=True, width=100)
                
            for i in range(inicio, fin):
            
            
                grupo = self.grupos_filtrados[i]
            
        

                # Agregar filas con datos filtrados
                with dpg.table_row():
                    dpg.add_text(f"{grupo['id']}")
                    dpg.add_text(f"{grupo['carrera']}")
                    dpg.add_text(f"{grupo['semestre']}")
                    dpg.add_text(f"{grupo['subgrupo']}")
                    
                    group_id = grupo["id"]
                    print(group_id)
                    
                    dpg.add_progress_bar(width=-1,  default_value=grupo["progress"], overlay=f"{grupo["progress"]*100}%")  
                    
                    def show_subjects_window(mode_id):
                        windows_manager.show_window(SUBJECTS_MANAGER_WINDOW_TAG, mode = "GROUP", mode_id = mode_id)   
                        
                    def delete_group(mode_id):
                        self.db.groups.remove(mode_id)
                        self.actualizar_lista_grupos()
                        
                    btn = dpg.add_button(label = "Materias", callback= lambda s, a, mode_id : show_subjects_window(mode_id=mode_id),
                                   user_data= group_id,
                                    width = -1)
                    
                    dpg.bind_item_theme(btn, self.tema_detalle1)
                    
                    btn = dpg.add_button(label = "Horario", callback= lambda s, a, mode_id : windows_manager.show_window(SCHEDULE_AVAILABILITY_WINDOW_TAG, mode = "GROUP", mode_id = mode_id),
                                   user_data= group_id,
                                    width = -1)
                    
                    dpg.bind_item_theme(btn, self.tema_detalle2)
                    
                    
                    btn = dpg.add_button(label = "X", callback= lambda s, a, mode_id : delete_group(mode_id),
                                   user_data= group_id,
                                    width = -1)
                    
                    dpg.bind_item_theme(btn, self.tema_eliminar)
                    
                    
                        #
                    ## Columna de acciones
                    #with dpg.group(horizontal=True):
                        #    btn_ver = dpg.add_button(label="Ver", width=70, callback=lambda s, a, u: self.ver_detalles(u), user_data=dato)
                        #    dpg.add_spacer(width=5)
                        #    btn_eliminar = dpg.add_button(label="Eliminar", width=70, callback=lambda s, a, u: self.eliminar_fila(u), user_data=dato['id'])
                        #    
                        #    # Aplicar temas a los botones
                        #    dpg.bind_item_theme(btn_ver, self.theme_btn_ver)
                        #    dpg.bind_item_theme(btn_eliminar, self.theme_btn_eliminar)

            return None 

        
        # Actualizar estado de los botones de navegación
        self.actualizar_botones_navegacion()
    
    def actualizar_botones_navegacion(self):
        """Actualiza el estado de habilitación de los botones de navegación"""
        # Botones de primera página y anterior
        dpg.configure_item("btn_primera_pagina", enabled=self.pagina_actual > 1)
        dpg.configure_item("btn_anterior_pagina", enabled=self.pagina_actual > 1)
        
        # Botones de siguiente página y última
        dpg.configure_item("btn_siguiente_pagina", enabled=self.pagina_actual < self.total_paginas)
        dpg.configure_item("btn_ultima_pagina", enabled=self.pagina_actual < self.total_paginas)
    
    def cambiar_pagina(self, accion):
        """Cambia la página según la acción especificada"""
        if accion == "primera":
            self.pagina_actual = 1
        elif accion == "anterior" and self.pagina_actual > 1:
            self.pagina_actual -= 1
        elif accion == "siguiente" and self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
        elif accion == "ultima":
            self.pagina_actual = self.total_paginas
        
        # Actualizar lista con la nueva página
        self.actualizar_lista_grupos()
    
    def ir_a_pagina(self, numero_pagina):
        """Salta a una página específica"""
        if 1 <= numero_pagina <= self.total_paginas:
            self.pagina_actual = numero_pagina
            self.actualizar_lista_grupos()
    
    def cambiar_elementos_por_pagina(self, cantidad):
        """Cambia la cantidad de elementos mostrados por página"""
        self.elementos_por_pagina = cantidad
        self.pagina_actual = 1  # Resetear a la primera página
        self.actualizar_lista_grupos()
    
    def seleccionar_grupo(self, grupo_id):
        """Maneja la selección de un grupo"""
        self.grupo_seleccionado = next(g for g in self.grupos if g["id"] == grupo_id)
        info = f"Seleccionado: {self.grupo_seleccionado['nombre']} ({self.grupo_seleccionado['carrera']} - Sem {self.grupo_seleccionado['semestre']}{self.grupo_seleccionado['subgrupo']})"
        dpg.set_value("info_grupo", info)
        dpg.configure_item("btn_eliminar_grupo", enabled=True)

    
    def confirmar_eliminar_grupo(self, grupo_id):
        """Muestra confirmación para eliminar grupo"""
        grupo = next(g for g in self.grupos if g["id"] == grupo_id)
        
        # Usar un ID único para la ventana modal para evitar conflictos
        modal_id = f"modal_confirm_{grupo_id}"
        
        with dpg.window(modal=True, show=True, tag=modal_id, no_title_bar=True, width=300, height=150, label="Confirmar eliminación"):
            dpg.add_text(f"¿Eliminar grupo {grupo['nombre']}?", wrap=280)
            dpg.add_spacer(height=15)
            
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Confirmar",
                    callback=lambda: self.eliminar_grupo(grupo_id, modal_id),
                    width=120
                )
                dpg.add_button(
                    label="Cancelar",
                    callback=lambda: dpg.delete_item(modal_id),
                    width=120
                )
    
    def eliminar_grupo(self, grupo_id, modal_id=None):
        """Elimina un grupo"""
        self.grupos = [g for g in self.grupos if g["id"] != grupo_id]
        
        if self.grupo_seleccionado and self.grupo_seleccionado["id"] == grupo_id:
            self.grupo_seleccionado = None
            dpg.set_value("info_grupo", "Ningún grupo seleccionado")
            dpg.configure_item("btn_eliminar_grupo", enabled=False)
        
        # Cerrar ventana modal si se proporciona un ID
        if modal_id and dpg.does_item_exist(modal_id):
            dpg.delete_item(modal_id)
        
        # Actualizar la lista de grupos (conservando la página actual si es posible)
        self.actualizar_lista_grupos()
    
    def gestionar_catalogos(self, sender, app_data, user_data):
        """Gestiona los catálogos de carreras, semestres y subgrupos"""
        tipo = user_data["tipo"]
        accion = user_data["accion"]
        valor = dpg.get_value(f"input_{tipo}")
        
        if accion == "agregar" and valor:
            if tipo == "carrera":
                self.carreras.add(valor)
            elif tipo == "semestre":
                self.semestres.add(valor)
            elif tipo == "subgrupo":
                self.subgrupos.add(valor)

            dpg.set_value(f"input_{tipo}", "")
            self.actualizar_combos()


        elif accion == "eliminar" and valor:
            if tipo == "carrera":
                self.carreras.discard(valor)
            elif tipo == "semestre":
                self.semestres.discard(valor)
            elif tipo == "subgrupo":
                self.subgrupos.discard(valor)
            
            dpg.set_value(f"input_{tipo}", "")
            self.actualizar_combos()
    
    def actualizar_combos(self):
        """Actualiza los combos con los valores actualizados"""
        dpg.configure_item("combo_carreras", items=sorted(self.carreras))
        dpg.configure_item("combo_semestres", items=sorted(self.semestres))
        dpg.configure_item("combo_subgrupos", items=sorted(self.subgrupos))
        dpg.configure_item("filtro_carrera", items=[""] + sorted(self.carreras))
        dpg.configure_item("filtro_semestre", items=[""] + sorted(self.semestres))
        dpg.configure_item("filtro_subgrupo", items=[""] + sorted(self.subgrupos))
    
    def aplicar_filtros(self):
        """Aplica los filtros de búsqueda"""
        self.filtros["nombre"] = dpg.get_value("filtro_nombre")
        self.filtros["carrera"] = dpg.get_value("filtro_carrera")
        self.filtros["semestre"] = dpg.get_value("filtro_semestre")
        self.filtros["subgrupo"] = dpg.get_value("filtro_subgrupo")
        # Resetear a la primera página cuando se aplica un filtro
        self.pagina_actual = 1
        self.actualizar_lista_grupos()
    
    def mostrar_materias(self, grupo_id):
        """Muestra las materias del grupo seleccionado"""
        grupo = next(g for g in self.grupos if g["id"] == grupo_id)
        
        # ID único para esta ventana
        ventana_id = f"ventana_materias_{grupo_id}"
        
        # Verificar si la ventana ya existe
        if dpg.does_item_exist(ventana_id):
            dpg.delete_item(ventana_id)
        
        with dpg.window(
            label=f"Materias: {grupo['nombre']}", 
            tag=ventana_id,
            width=400, 
            height=300, 
            pos=[200, 200], 
            modal=True,
            no_close=False
        ):
            dpg.add_text(f"Carrera: {grupo['carrera']} | Semestre: {grupo['semestre']}")
            dpg.add_separator()
            
            # Verificar si hay materias
            if 'materias' in grupo and grupo['materias']:
                for i, materia in enumerate(grupo['materias']):
                    with dpg.group(horizontal=True):
                        dpg.add_text(f"{i+1}. {materia}")
                        dpg.add_button(
                            label="✕",
                            callback=lambda s, a, u: self.eliminar_materia(grupo_id, u),
                            user_data=(grupo_id, materia),
                            width=25
                        )
            else:
                dpg.add_text("No hay materias asignadas.")
            
            dpg.add_separator()
            
            # Agregar una nueva materia
            with dpg.group(horizontal=True):
                dpg.add_input_text(tag=f"nueva_materia_{grupo_id}", width=200)
                dpg.add_button(
                    label="Agregar materia",
                    callback=lambda: self.agregar_materia(
                        grupo_id, 
                        dpg.get_value(f"nueva_materia_{grupo_id}")
                    ),
                    width=120
                )
    
    def eliminar_materia(self, grupo_id, datos):
        """Elimina una materia de un grupo"""
        grupo_id, materia = datos
        grupo = next(g for g in self.grupos if g["id"] == grupo_id)
        
        if 'materias' in grupo and materia in grupo['materias']:
            grupo['materias'].remove(materia)
            
            # Actualizar la ventana de materias
            self.mostrar_materias(grupo_id)
    
    def agregar_materia(self, grupo_id, nueva_materia):
        """Agrega una materia al grupo"""
        if nueva_materia.strip():
            grupo = next(g for g in self.grupos if g["id"] == grupo_id)
            
            if 'materias' not in grupo:
                grupo['materias'] = []
            
            if nueva_materia not in grupo['materias']:
                grupo['materias'].append(nueva_materia)
            
            dpg.set_value(f"nueva_materia_{grupo_id}", "")
            
            self.mostrar_materias(grupo_id)
    
    def mostrar_horario(self, grupo_id):
        """Muestra los horarios disponibles del grupo"""
        grupo = next(g for g in self.grupos if g["id"] == grupo_id)
        
        # ID único para esta ventana
        ventana_id = f"ventana_horario_{grupo_id}"
        
        # Verificar si la ventana ya existe
        if dpg.does_item_exist(ventana_id):
            dpg.delete_item(ventana_id)
        
        with dpg.window(
            label=f"Horario: {grupo['nombre']}", 
            tag=ventana_id,
            width=400, 
            height=400, 
            pos=[300, 200], 
            modal=True,
            no_close=False
        ):
            dpg.add_text(f"Carrera: {grupo['carrera']} | Semestre: {grupo['semestre']}")
            dpg.add_separator()
            
            # Mostrar horarios por turno
            if 'horarios' in grupo and grupo['horarios']:
                for turno, horas in grupo['horarios'].items():
                    with dpg.collapsing_header(label=f"Turno {turno}", default_open=True):
                        if horas:
                            for hora in horas:
                                with dpg.group(horizontal=True):
                                    dpg.add_text(f"{hora}")
                                    dpg.add_button(
                                        label="✕",
                                        callback=lambda s, a, u: self.eliminar_horario(u[0], u[1], u[2]),
                                        user_data=(grupo_id, turno, hora),
                                        width=25
                                    )
                        else:
                            dpg.add_text("No hay horarios asignados para este turno.")
            else:
                dpg.add_text("No hay horarios asignados.")
            
            dpg.add_separator()
            
            # Agregar un nuevo horario
            with dpg.group():
                dpg.add_combo(
                    label="Turno", 
                    items=list(self.horarios_disponibles.keys()),
                    tag=f"nuevo_turno_{grupo_id}",
                    width=150
                )
                dpg.add_input_text(
                    label="Horario (formato HH:MM-HH:MM)", 
                    tag=f"nuevo_horario_{grupo_id}", 
                    width=200
                )
                dpg.add_button(
                    label="Agregar horario",
                    callback=lambda: self.agregar_horario(
                        grupo_id, 
                        dpg.get_value(f"nuevo_turno_{grupo_id}"),
                        dpg.get_value(f"nuevo_horario_{grupo_id}")
                    ),
                    width=120
                )
    
    def eliminar_grupo(self, grupo_id, modal_id=None):
        """Elimina un grupo"""
        self.grupos = [g for g in self.grupos if g["id"] != grupo_id]
        
        if self.grupo_seleccionado and self.grupo_seleccionado["id"] == grupo_id:
            self.grupo_seleccionado = None
            dpg.set_value("info_grupo", "Ningún grupo seleccionado")
            dpg.configure_item("btn_eliminar_grupo", enabled=False)
        
        # Cerrar ventana modal si se proporciona un ID
        if modal_id and dpg.does_item_exist(modal_id):
            dpg.delete_item(modal_id)
        
        self.actualizar_lista_grupos()
    
    def gestionar_catalogos(self, sender, app_data, user_data):
        """Gestiona los catálogos de carreras, semestres y subgrupos"""
        tipo = user_data["tipo"]
        accion = user_data["accion"]
        valor = dpg.get_value(f"input_{tipo}")
        
        if accion == "agregar" and valor:
            if tipo == "carrera":
                self.carreras.add(valor)
            elif tipo == "semestre":
                self.semestres.add(valor)
            elif tipo == "subgrupo":
                self.subgrupos.add(valor)
            
            dpg.set_value(f"input_{tipo}", "")
            self.actualizar_combos()
        
        elif accion == "eliminar" and valor:
            if tipo == "carrera":
                self.carreras.discard(valor)
            elif tipo == "semestre":
                self.semestres.discard(valor)
            elif tipo == "subgrupo":
                self.subgrupos.discard(valor)
            
            dpg.set_value(f"input_{tipo}", "")
            self.actualizar_combos()
    
    def actualizar_combos(self):
        """Actualiza los combos con los valores actualizados"""
        dpg.configure_item(self.combo_careers_tag, items=sorted(self.items.get_careers()))
        dpg.configure_item(self.combo_semesters_tag, items=sorted(self.items.get_semesters()))
        dpg.configure_item(self.combo_subgroups_tag, items=sorted(self.items.get_subgroups()))

    def aplicar_filtros(self):
        """Aplica los filtros de búsqueda"""
        self.filtros["nombre"] = dpg.get_value("filtro_nombre")
        self.filtros["carrera"] = dpg.get_value(self.combo_careers_tag)
        self.filtros["semestre"] = dpg.get_value(self.combo_semesters_tag)
        self.filtros["subgrupo"] = dpg.get_value(self.combo_subgroups_tag)
        self.actualizar_lista_grupos()
    
    def mostrar_materias(self, grupo_id):
        """Muestra las materias del grupo seleccionado"""
        grupo = next(g for g in self.grupos if g["id"] == grupo_id)
        
        # ID único para esta ventana
        ventana_id = f"ventana_materias_{grupo_id}"
        
        # Verificar si la ventana ya existe
        if dpg.does_item_exist(ventana_id):
            dpg.delete_item(ventana_id)
        
        with dpg.window(
            label=f"Materias: {grupo['nombre']}", 
            tag=ventana_id,
            width=400, 
            height=300, 
            pos=[200, 200], 
            modal=True,
            no_close=False
        ):
            dpg.add_text(f"Carrera: {grupo['carrera']} | Semestre: {grupo['semestre']}")
            dpg.add_separator()
            
            # Verificar si hay materias
            if 'materias' in grupo and grupo['materias']:
                for i, materia in enumerate(grupo['materias']):
                    with dpg.group(horizontal=True):
                        dpg.add_text(f"{i+1}. {materia}")
                        dpg.add_button(
                            label="✕",
                            callback=lambda s, a, u: self.eliminar_materia(grupo_id, u),
                            user_data=(grupo_id, materia),
                            width=25
                        )
            else:
                dpg.add_text("No hay materias asignadas.")
            
            dpg.add_separator()
            
            # Agregar una nueva materia
            with dpg.group(horizontal=True):
                dpg.add_input_text(tag=f"nueva_materia_{grupo_id}", width=200)
                dpg.add_button(
                    label="Agregar materia",
                    callback=lambda: self.agregar_materia(
                        grupo_id, 
                        dpg.get_value(f"nueva_materia_{grupo_id}")
                    ),
                    width=120
                )
    
    def eliminar_materia(self, grupo_id, datos):
        """Elimina una materia de un grupo"""
        grupo_id, materia = datos
        grupo = next(g for g in self.grupos if g["id"] == grupo_id)
        
        if 'materias' in grupo and materia in grupo['materias']:
            grupo['materias'].remove(materia)
            
            # Actualizar la ventana de materias
            self.mostrar_materias(grupo_id)
    
    def agregar_materia(self, grupo_id, nueva_materia):
        """Agrega una materia al grupo"""
        if nueva_materia.strip():
            grupo = next(g for g in self.grupos if g["id"] == grupo_id)
            
            if 'materias' not in grupo:
                grupo['materias'] = []
            
            if nueva_materia not in grupo['materias']:
                grupo['materias'].append(nueva_materia)
            
            # Limpiar el campo de texto
            dpg.set_value(f"nueva_materia_{grupo_id}", "")
            
            # Actualizar la ventana
            self.mostrar_materias(grupo_id)
    
    def mostrar_horario(self, grupo_id):
        """Muestra los horarios disponibles del grupo"""
        grupo = next(g for g in self.grupos if g["id"] == grupo_id)
        
        # ID único para esta ventana
        ventana_id = f"ventana_horario_{grupo_id}"
        
        # Verificar si la ventana ya existe
        if dpg.does_item_exist(ventana_id):
            dpg.delete_item(ventana_id)
        
        with dpg.window(
            label=f"Horario: {grupo['nombre']}", 
            tag=ventana_id,
            width=400, 
            height=400, 
            pos=[300, 200], 
            modal=True,
            no_close=False
        ):
            dpg.add_text(f"Carrera: {grupo['carrera']} | Semestre: {grupo['semestre']}")
            dpg.add_separator()
            
            # Mostrar horarios por turno
            if 'horarios' in grupo and grupo['horarios']:
                for turno, horas in grupo['horarios'].items():
                    with dpg.collapsing_header(label=f"Turno {turno}", default_open=True):
                        if horas:
                            for hora in horas:
                                with dpg.group(horizontal=True):
                                    dpg.add_text(f"{hora}")
                                    dpg.add_button(
                                        label="✕",
                                        callback=lambda s, a, u: self.eliminar_horario(u[0], u[1], u[2]),
                                        user_data=(grupo_id, turno, hora),
                                        width=25
                                    )
                        else:
                            dpg.add_text("No hay horarios asignados para este turno.")
            else:
                dpg.add_text("No hay horarios asignados.")
            
            dpg.add_separator()
            
            # Agregar un nuevo horario
            with dpg.group():
                dpg.add_combo(
                    label="Turno", 
                    items=list(self.horarios_disponibles.keys()),
                    tag=f"nuevo_turno_{grupo_id}",
                    width=150
                )
                dpg.add_input_text(
                    label="Horario (formato HH:MM-HH:MM)", 
                    tag=f"nuevo_horario_{grupo_id}", 
                    width=200
                )
                dpg.add_button(
                    label="Agregar horario",
                    callback=lambda: self.agregar_horario(
                        grupo_id, 
                        dpg.get_value(f"nuevo_turno_{grupo_id}"),
                        dpg.get_value(f"nuevo_horario_{grupo_id}")
                    ),
                    width=120
                )
    
    def eliminar_horario(self, grupo_id, turno, hora):
        """Elimina un horario específico de un grupo"""
        grupo = next(g for g in self.grupos if g["id"] == grupo_id)
        
        if 'horarios' in grupo and turno in grupo['horarios'] and hora in grupo['horarios'][turno]:
            grupo['horarios'][turno].remove(hora)
            
            # Actualizar la ventana de horarios
            self.mostrar_horario(grupo_id)
    
    def agregar_horario(self, grupo_id, turno, horario):
        """Agrega un horario al grupo"""
        if turno and horario.strip():
            grupo = next(g for g in self.grupos if g["id"] == grupo_id)
            
            if 'horarios' not in grupo:
                grupo['horarios'] = {}
            
            if turno not in grupo['horarios']:
                grupo['horarios'][turno] = []
            
            if horario not in grupo['horarios'][turno]:
                grupo['horarios'][turno].append(horario)
            
            # Limpiar el campo de texto
            dpg.set_value(f"nuevo_horario_{grupo_id}", "")
            
            # Actualizar la ventana
            self.mostrar_horario(grupo_id)
    
    def update(self):
        self.items.update()
        self.aplicar_filtros()
        self.actualizar_combos()
        pass 

        
   