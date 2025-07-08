import dearpygui.dearpygui as dpg
import random
import time
from typing import List, Dict, Callable, Optional, Any
from src.app.UI.components.schedule_availability.schedule_availability import HorarioDisponibilidadApp

from src.app.UI.components.windows_manager import windows_manager
from src.app.UI.windows_tags import SUBJECTS_MANAGER_WINDOW_TAG, SCHEDULE_AVAILABILITY_WINDOW_TAG


class GestorEntidad:
    """Clase base para gestionar entidades (profesores, aulas, etc.)"""
    
    def __init__(self, nombre_entidad: str, campos: List[str], db , generador_datos=None):
        """
        Inicializa un gestor de entidades
        
        Args:
            nombre_entidad: Nombre en singular de la entidad (ej: "Profesor", "Aula")
            campos: Lista de campos que tiene la entidad
            generador_datos: Función opcional para generar datos de ejemplo
        """
        
        self.nombre_entidad = nombre_entidad
        self.nombre_plural = f"{nombre_entidad}es" if nombre_entidad.endswith('r') else f"{nombre_entidad}s"
        self.campos = campos
        self.items = []
        self.ultima_busqueda = ""
        self.items_filtrados = []
        self.cache_busqueda = {}
        self.item_seleccionado = None
        self.db = db
        self.generar_datos = generador_datos
        
        
        # Generar datos de ejemplo si se proporcionó un generador
        if generador_datos:
            self.items = generador_datos()
            self.items_filtrados = self.items.copy()
            self.nuevo_id = max(p["id"] for p in self.items) + 1 if self.items else 1
        else:
            self.nuevo_id = 1
            
        # Crear temas
        self.crear_temas()
        pass
        
    def crear_temas(self):
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
        
    def get_tag(self, suffix: str) -> str:
        """Genera un tag único para los elementos de la UI"""
        return f"{self.nombre_entidad.lower()}_{suffix}"
    
    def actualizar_lista(self, force: bool = False) -> None:
        """Actualiza la lista con paginación y caching"""

        # Obtener los valores actuales
        filtro = dpg.get_value(self.get_tag("filtro")).lower()
        pagina = dpg.get_value(self.get_tag("pagina_actual"))
        por_pagina = dpg.get_value(self.get_tag("items_por_pagina"))
        
        # Si cambia el filtro o se fuerza la actualización, limpiar caché y buscar nuevamente
        if force or filtro != self.ultima_busqueda:
            start_time = time.time()
            
            # El campo de filtro depende de la entidad (por defecto usamos el primer campo)
            campo_filtro = self.campos[0] if self.campos else "nombre"
            self.items_filtrados = [p for p in self.items if filtro in str(p.get(campo_filtro, "")).lower()]
            
            self.cache_busqueda[filtro] = self.items_filtrados
            self.ultima_busqueda = filtro
            
            # Resetear la página al cambiar el filtro
            pagina = 1
            dpg.set_value(self.get_tag("pagina_actual"), pagina)
        else:
            self.items_filtrados = self.cache_busqueda.get(filtro, self.items_filtrados)
        
        # Actualizar paginación
        total_paginas = max(1, (len(self.items_filtrados) + por_pagina - 1) // por_pagina)
        dpg.configure_item(self.get_tag("total_paginas"), label=f"de {total_paginas}")
        dpg.configure_item(self.get_tag("pagina_actual"), max_value=total_paginas)
        
        # Calcular inicio y fin para paginación
        inicio = (pagina - 1) * por_pagina
        fin = min(inicio + por_pagina, len(self.items_filtrados))
        
        # Limpiar y reconstruir la lista
        lista_tag = self.get_tag("lista")
        dpg.delete_item(lista_tag, children_only=True)
        
        # Renderizar los elementos filtrados
        self.renderizar_items(lista_tag, self.items_filtrados[inicio:fin])
        
        # Actualizar contador
        dpg.configure_item(self.get_tag("contador_total"), label=f"Total {self.nombre_plural}: {len(self.items)}")
    
    def renderizar_items(self, parent_tag: str, items: List[Dict]) -> None:
        """Renderiza los items en la interfaz"""
        # Limpiar la tabla existente
        dpg.delete_item(f"tabla_container_{self.nombre_entidad}", children_only=True)
        
        with dpg.table(header_row=True, borders_innerH=True, borders_outerH=True,
                      borders_innerV=True, borders_outerV=True, tag=f"tabla_items_{self.nombre_entidad}", 
                      parent=f"tabla_container_{self.nombre_entidad}"):
            
            # Definir columnas
            dpg.add_table_column(label="ID", width_fixed=True, width=100)
            dpg.add_table_column(label="NOMBRE",width_stretch=True, init_width_or_weight=250)
            dpg.add_table_column(label="PROGRESO", width_fixed=True,init_width_or_weight=100)
            dpg.add_table_column(label="Materias", width_fixed=True, init_width_or_weight=120)
            dpg.add_table_column(label="Horario", width_fixed=True, init_width_or_weight=120)
            dpg.add_table_column(label="Eliminar", width_fixed=True, width=100)
            
            # Agregar filas con datos filtrados
            for item in items:
                with dpg.table_row():
                    dpg.add_text(f"{item["id"]}")
                    campo_principal = self.campos[0] if self.campos else "nombre"
                    dpg.add_text(f"{item["name"]}")
                    progress = item["progress"]
                    progress_bar = dpg.add_progress_bar(
                        default_value=progress,
                        overlay = f"{int(progress * 100)}%",
                        width=-1
                    )
                    
                    for idx, accion in enumerate(self.get_acciones_item()):
                        btn = dpg.add_button(
                            label=accion["label"],
                            user_data=(item["id"], accion["callback"]),
                            callback=lambda s, a, u : u[1](u[0]), #! u = (id, accion), se ejecuta accion(id)
                            width=-1,
                            height=20
                        )
                        
                        # Aplicar tema según el índice
                        if idx == 0:
                            dpg.bind_item_theme(btn, self.tema_detalle1)
                        elif idx == 1:
                            dpg.bind_item_theme(btn, self.tema_detalle2)
                    
                    btn_eliminar = dpg.add_button(
                        label="×",
                        user_data=item["id"],
                        callback=lambda s, a, u: self.confirmar_eliminar(u),
                        width=-1,
                        height=20
                    )
                    

                    dpg.bind_item_theme(btn_eliminar, self.tema_eliminar)                  
                    
    
    def get_acciones_item(self) -> List[Dict]:
        """
        Devuelve la lista de acciones para cada item
        Override en subclases para personalizar
        """
        return [
            {"label": "Detalle", "callback": self.mostrar_detalle1},
            {"label": "Editar", "callback": self.mostrar_detalle2},
        ]
    
    def seleccionar_item(self, item_id: int) -> None:
        """Selecciona un item para operaciones posteriores"""
        self.item_seleccionado = next((p for p in self.items if p["id"] == item_id), None)
        info_tag = self.get_tag("info_item")
        campo_principal = self.campos[0] if self.campos else "nombre"
        
        if self.item_seleccionado:
            dpg.set_value(
                info_tag, 
                f"Seleccionado: {self.item_seleccionado.get(campo_principal, '')} (ID: {self.item_seleccionado['id']})"
            )
    
    def mostrar_detalle1(self, item_id: int) -> None:
        """Muestra la ventana de detalle 1 para el item seleccionado"""
        item = next((p for p in self.items if p["id"] == item_id), None)
        if not item:
            return
            
        ventana_tag = f"{self.nombre_entidad.lower()}_detalle1"
        
        # Verificar si ya existe una ventana abierta y cerrarla
        if dpg.does_item_exist(ventana_tag):
            dpg.delete_item(ventana_tag)
        
        campo_principal = self.campos[0] if self.campos else "nombre"
        with dpg.window(modal=True, show=True, tag=ventana_tag, 
                       label=f"Detalle 1 de {item.get(campo_principal, '')}", 
                       width=500, height=400, pos=[200, 200]):
            dpg.add_text(f"Esta ventana muestra detalles del {self.nombre_entidad}.")
            dpg.add_spacer(height=10)
            
            with dpg.child_window(height=200, border=True):
                dpg.add_text(f"{self.nombre_entidad}: {item.get(campo_principal, '')} (ID: {item['id']})")
                dpg.add_text(f"Funcionalidad de detalle 1 a implementar para {self.nombre_entidad}.")
            
            dpg.add_spacer(height=20)
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Cerrar",
                    callback=lambda: dpg.delete_item(ventana_tag),
                    width=150
                )
    
    def mostrar_detalle2(self, item_id: int) -> None:
        """Muestra la ventana de detalle 2 para el item seleccionado"""
        item = next((p for p in self.items if p["id"] == item_id), None)
        if not item:
            return
            
        ventana_tag = f"{self.nombre_entidad.lower()}_detalle2"
        
        # Verificar si ya existe una ventana abierta y cerrarla
        if dpg.does_item_exist(ventana_tag):
            dpg.delete_item(ventana_tag)
        
        campo_principal = self.campos[0] if self.campos else "nombre"
        with dpg.window(modal=True, show=True, tag=ventana_tag, 
                       label=f"Detalle 2 de {item.get(campo_principal, '')}", 
                       width=500, height=400, pos=[200, 200]):
            dpg.add_text(f"Esta ventana muestra el detalle 2 del {self.nombre_entidad}.")
            dpg.add_spacer(height=10)
            
            with dpg.child_window(height=200, border=True):
                dpg.add_text(f"{self.nombre_entidad}: {item.get(campo_principal, '')} (ID: {item['id']})")
                dpg.add_text(f"Funcionalidad de detalle 2 a implementar para {self.nombre_entidad}.")
            
            dpg.add_spacer(height=20)
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Cerrar",
                    callback=lambda: dpg.delete_item(ventana_tag),
                    width=150
                )
    
    def agregar_item(self) -> None:
        """Agrega un nuevo item a la lista"""
        # Obtener el valor del campo principal
        campo_principal = self.campos[0] if self.campos else "nombre"
        valor = dpg.get_value(self.get_tag("nuevo_item")).strip() # nombre
        if not valor:
            return
        
        if self.nombre_entidad == "PROFESSOR":
            self.db.professors.new(valor)
        elif self.nombre_entidad == "CLASSROOM":
            self.db.classrooms.new(valor)
        
        # Agregar y actualizar
        self.items = self.generar_datos()
        
        # Limpiar input y actualizar lista
        dpg.set_value(self.get_tag("nuevo_item"), "")
        self.cache_busqueda.clear()
        self.actualizar_lista(force=True)
        
        info_tag = self.get_tag("info_item")
    
    def confirmar_eliminar(self, item_id: int) -> None:
        """Muestra confirmación antes de eliminar"""
        item = next((p for p in self.items if p["id"] == item_id), None)
        if not item:
            return
            
        campo_principal = self.campos[0] if self.campos else "nombre"
        modal_tag = f"{self.nombre_entidad.lower()}_modal_confirm"
        
        with dpg.window(modal=True, show=True, tag=modal_tag, label="Confirmación", width=400, height=150, pos=[250, 300]):
            dpg.add_text(f"¿Está seguro que desea eliminar {self.nombre_entidad.lower()} '{item.get(campo_principal, '')}'?")
            dpg.add_spacer(height=20)
            with dpg.group(horizontal=True):
                btn_confirm = dpg.add_button(
                    label="Confirmar",
                    callback=lambda: self.eliminar_item(item_id, modal_tag),
                    width=150
                )
                dpg.bind_item_theme(btn_confirm, self.tema_eliminar)
                
                btn_cancel = dpg.add_button(
                    label="Cancelar",
                    callback=lambda: dpg.delete_item(modal_tag),
                    width=150
                )
    
    def eliminar_item(self, item_id: int, modal_tag: str) -> None:
        """Elimina un item de la lista"""
        # Filtrar el item a eliminar
        
        if self.nombre_entidad == "PROFESSOR":
            self.db.professors.remove(item_id)
        else :
            self.db.classrooms.remove(item_id)
        
            
        self.items = self.generar_datos()


        # Actualizar selección si es necesario
        if self.item_seleccionado and self.item_seleccionado["id"] == item_id:
            self.item_seleccionado = None
            info_tag = self.get_tag("info_item")
            dpg.set_value(info_tag, f"Ningún {self.nombre_entidad.lower()} seleccionado")
        
        # Limpiar caché y actualizar lista
        self.cache_busqueda.clear()
        dpg.delete_item(modal_tag)
        self.actualizar_lista(force=True)
    
    def cambiar_pagina(self) -> None:
        """Actualiza la lista al cambiar de página"""
        self.actualizar_lista()
    
    def setup_ui(self, parent_tag: str) -> None:
        """Crea la interfaz de usuario para gestionar la entidad"""
        with dpg.group(horizontal=False, parent=parent_tag):
            # Sección de búsqueda
            with dpg.child_window(height=90, label="Búsqueda"):
                with dpg.group(horizontal=True):
                    dpg.add_text(f"Buscar {self.nombre_entidad.lower()}")
                    dpg.add_input_text(
                        tag=self.get_tag("filtro"),
                        width=-120,
                        callback=lambda: self.actualizar_lista(force=True)
                    )
                    
                    btn_limpiar = dpg.add_button(
                        label="Limpiar filtro",
                        callback=lambda: [
                            dpg.set_value(self.get_tag("filtro"), ""), 
                            self.actualizar_lista(force=True)
                        ]
                    )
                
                dpg.add_separator()
                
                with dpg.group(horizontal=True):
                    # Texto descriptivo según la entidad
                    label_text = f"Nombre "
                    
                    dpg.add_text(label_text)
                    
                    dpg.add_input_text(
                        tag=self.get_tag("nuevo_item"),
                        width=-100,
                        on_enter=True,
                        callback=self.agregar_item
                    )
                    btn_agregar = dpg.add_button(
                        label="Agregar",
                        callback=self.agregar_item,
                        width=-1
                    )
                    dpg.bind_item_theme(btn_agregar, self.tema_accion)
            
            # Paginación
            with dpg.child_window(height=65, label="Paginación"):
                with dpg.group(horizontal=True):
                    dpg.add_text("Página:")
                    dpg.add_input_int(
                        tag=self.get_tag("pagina_actual"),
                        default_value=1,
                        min_value=1,
                        min_clamped=True,
                        width=80,
                        step=1,
                        callback=lambda: self.cambiar_pagina()
                    )
                    dpg.add_text("", tag=self.get_tag("total_paginas"))
                    dpg.add_spacer(width=20)
                    dpg.add_text("Items por página:")
                    dpg.add_input_int(
                        tag=self.get_tag("items_por_pagina"),
                        default_value=50,
                        min_value=10,
                        max_value=200,
                        min_clamped=True,
                        max_clamped=True,
                        width=80,
                        step=10,
                        callback=lambda: [
                            dpg.set_value(self.get_tag("pagina_actual"), 1), 
                            self.actualizar_lista(force=True)
                        ]
                    )
                    dpg.add_spacer(width=20)
                    # Añadir contador total
                    dpg.add_text(f"Total {self.nombre_plural}: 0", tag=self.get_tag("contador_total"))
            
            # Lista de items
            with dpg.child_window(label=f"Lista de {self.nombre_plural}", height=-1, border=True, tag = f"tabla_container_{self.nombre_entidad}"):
                with dpg.child_window(tag=self.get_tag("lista"), height=-1, border=False):
                    pass
        
        # Inicializar lista
        self.actualizar_lista(force=True)

    def update(self):
        self.items = self.generar_datos()

        self.actualizar_lista(force=True)
        

class ProfessorsManager(GestorEntidad):
    """Gestor específico para profesores"""
    
    def __init__(self, db):
        # Generar datos de ejemplo
        def generar_datos():
            # Nombres y apellidos aleatorios
            
            query = custom_query("PROFESSOR")

            cursor = self.db.execute_query(query)
            
            # Generar profesores aleatorios
            return [{
                "id": id,
                "name": name,
                "progress" : progress
            } for (id, name, progress) in cursor]
        
        super().__init__("PROFESSOR", ["name"], db, generar_datos)

    
    def get_acciones_item(self) -> List[Dict]:
        """Define acciones específicas para profesores"""
        return [
            {"label": "Materias", "callback": self.mostrar_materias},
            {"label": "Horario", "callback": self.mostrar_disponibilidad},
        ]
    
    
    def mostrar_materias(self, prof_id: int) -> None:
        """Muestra la ventana de materias para el profesor seleccionado"""
        profesor = next((p for p in self.items if p["id"] == prof_id), None)
        if not profesor:
            return
        
        windows_manager.show_window(window_tag= SUBJECTS_MANAGER_WINDOW_TAG, mode = "PROFESSOR", mode_id = prof_id)
        

    def mostrar_disponibilidad(self, prof_id: int) -> None:
        """Muestra la ventana de disponibilidad para el profesor seleccionado"""
        professor = next((p for p in self.items if p["id"] == prof_id), None)
        if not professor:
            return
        
        windows_manager.show_window(SCHEDULE_AVAILABILITY_WINDOW_TAG, mode = "PROFESSOR", mode_id = prof_id)
        
 
def custom_query(mode):
    if not mode in ["PROFESSOR", "CLASSROOM"]:
        return None 
    return f"""	
    SELECT 
        p.ID AS ID,
        p.NAME,
        COALESCE(
            CAST(ps_completed.COMPLETED_SLOTS AS FLOAT) / 
            NULLIF(ps_total.TOTAL_SLOTS, 0), 
            1.0
        ) AS PROGRESS
    FROM 
        {mode} p
    LEFT JOIN (
        SELECT 
            ps.ID_{mode},
            SUM(s.TOTAL_SLOTS) AS TOTAL_SLOTS
        FROM 
            {mode}_SUBJECT ps
        JOIN 
            SUBJECT s ON ps.ID_SUBJECT = s.ID
        GROUP BY 
            ps.ID_{mode}
    ) ps_total ON p.ID = ps_total.ID_{mode}
    LEFT JOIN (
        SELECT 
            ps.ID_{mode},
            SUM(ss.LEN) AS COMPLETED_SLOTS
        FROM 
            {mode}_SUBJECT ps
        JOIN 
            SUBJECT_SLOTS ss ON ps.ID_SUBJECT = ss.ID_SUBJECT
        GROUP BY 
            ps.ID_{mode}
    ) ps_completed ON p.ID = ps_completed.ID_{mode};
            """


class ClassroomsManager(GestorEntidad):
    """Gestor específico para profesores"""
    
    def __init__(self, db):
        # Generar datos de ejemplo
        def generar_datos():
            
        
            query = custom_query("CLASSROOM")
            cursor = db.execute_query(query)

            # Generar profesore
            return [{
                "id": id,
                "name": name,
                "progress" : progress
            } for (id, name, progress) in cursor]
            
        
        super().__init__("CLASSROOM", ["name"], db, generar_datos)
    
    def get_acciones_item(self) -> List[Dict]:
        """Define acciones específicas para profesores"""
        return [
            {"label": "Materias", "callback": self.mostrar_materias},
            {"label": "Horario", "callback": self.mostrar_disponibilidad},
        ]
    
    def mostrar_materias(self, clas_id: int) -> None:
        """Muestra la ventana de materias para el profesor seleccionado"""
        classroom = next((p for p in self.items if p["id"] == clas_id), None)
        if not classroom:
            return

        windows_manager.show_window(SUBJECTS_MANAGER_WINDOW_TAG, mode = "CLASSROOM", mode_id = clas_id)

    def mostrar_disponibilidad(self, clas_id: int) -> None:
        """Muestra la ventana de disponibilidad para el profesor seleccionado"""
        classroom = next((p for p in self.items if p["id"] == clas_id), None)
        if not classroom:
            return

        windows_manager.show_window(SCHEDULE_AVAILABILITY_WINDOW_TAG, mode = "CLASSROOM", mode_id = clas_id)
