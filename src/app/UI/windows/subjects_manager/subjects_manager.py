from src.app.database import database_manager
import dearpygui.dearpygui as dpg
from src.app.UI.components.windows_manager import Window, windows_manager
from src.app.UI.windows_tags import SUBJECTS_MANAGER_WINDOW_TAG, NEW_SUBJECT_WINDOW_TAG



class SubjectsManager(Window):
    # Colores para la interfaz
    COLOR_BG_DARK = [33, 37, 43, 255]
    COLOR_BG_LIGHT = [42, 47, 53, 255]
    COLOR_HEADER = [52, 140, 215, 255]
    COLOR_TEXT = [240, 240, 240, 255]
    COLOR_ROW_EVEN = [45, 50, 56, 255]
    COLOR_ROW_ODD = [35, 40, 46, 255]
    COLOR_BUTTON_VIEW = [52, 131, 235, 255]
    COLOR_BUTTON_VIEW_HOVER = [66, 150, 250, 255]
    COLOR_BUTTON_DELETE = [235, 64, 52, 255]
    COLOR_BUTTON_DELETE_HOVER = [250, 80, 70, 255]
    COLOR_FILTER_BG = [38, 42, 48, 255]
    
    def __init__(self, db, mode_id = None, mode = "PROFESSOR"):
        
        if not mode in ["PROFESSOR", "GROUP", "CLASSROOM"]:
            return None  
        
        
        self.db = db 
        self.mode_id = mode_id
        self.mode = mode 

        
        self.update_subjects()
        
        # Datos filtrados (inicialmente todos)
        self.datos_filtrados = self.datos_tabla.copy()
        
        # Inicializar DPG
        self.crear_temas()
        
        super().__init__(
            window_tag = SUBJECTS_MANAGER_WINDOW_TAG,
            label = f"materia de {mode_id}",
            on_close= lambda s, a, u : print(10),
            width=860,
            height=680,
            no_resize=True
        )
        
        
        self.create()
        
    def _create_content(self):
        # Crear la ventana principal y viewport
        
        dpg.add_text("Sistema de Gestión de Materias Académicas")
        dpg.add_separator()
        
        # Sección de filtros
        with dpg.group(width = -1, height=-1):
            with dpg.child_window(tag="filtros_container", height=80, border=True):
                dpg.add_text("Filtros de Búsqueda")
                with dpg.group(horizontal=True):
                    # Filtro por código
                    dpg.add_text("Código:")
                    dpg.add_input_text(tag="filtro_codigo", width=100, callback=self.aplicar_filtros)
                    dpg.add_spacer(width=10)
                    
                    # Filtro por nombre
                    dpg.add_text("Nombre:")
                    dpg.add_input_text(tag="filtro_nombre_1", width=200, callback=self.aplicar_filtros)
                    dpg.add_spacer(width=10)
                    
                    # Filtro por créditos
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Limpiar Filtros", callback=self.limpiar_filtros)
                    dpg.add_button(label="Aplicar Filtros", callback=self.aplicar_filtros)
                
                dpg.add_separator()
                
                # Contenedor con scroll para la tabla
                dpg.add_child_window(tag="tabla_container", width=-1, height=400, horizontal_scrollbar=True)
                
                # Botón para agregar nuevas filas
                dpg.add_button(label="Agregar Nueva Materia", callback=self.agregar_fila)
                
                # Información de estadísticas
                with dpg.group(horizontal=True):
                    dpg.add_text("Total de materias: ")
                    dpg.add_text(str(len(self.datos_tabla)), tag="total_materias")
                    dpg.add_spacer(width=20)
                    dpg.add_text("Materias mostradas: ")
                    dpg.add_text(str(len(self.datos_filtrados)), tag="materias_mostradas")
            
        # Aplicar tema global
        #dpg.bind_item_theme("filtros_container", self.theme_filter)
        
        # Actualizar tabla inicial
        self.actualizar_tabla()

    def generate_label(self, mode, mode_id):
        if mode == "PROFESSOR":
            name = self.db.professors.get_name(mode_id)
            label = f"materias del professor {name} (ID = {mode_id})"
        elif mode == "CLASSROOM":
            name = self.db.classrooms.get_name(mode_id)
            label = f"materias del salon {name} (ID = {mode_id})"
        else:
            name = self.db.groups.get_name(mode_id)
            label = f"materia del grupo {name} (ID = {mode_id})"
        
        return label
    
        pass
    
    def show(self, **kwargs):
        mode = kwargs["mode"]
        
        mode_id = kwargs["mode_id"]
        
        label = self.generate_label(mode, mode_id)
        
        self.set_title(label)
        
        self.set_mode(mode,mode_id)
        
        super().show()
        
    def update_subjects(self):
        
        if self.mode_id is None:
            self.datos_tabla = []
            self.datos_filtrados = []
            return None 
        
        query = f"""
         SELECT S.ID, S.CODE, S.NAME, 
            CAST(SUM(coalesce(SS.LEN, 0)) AS REAL) / CAST(S.TOTAL_SLOTS AS REAL) AS PROGRESS
            FROM (
                SELECT *
                FROM SUBJECT S
                WHERE ID IN (
                            SELECT ID_SUBJECT
                            FROM {self.mode}_SUBJECT
                            WHERE ID_{self.mode} = {self.mode_id}
                )
            ) S
            LEFT JOIN SUBJECT_SLOTS  SS ON S.ID = SS.ID_SUBJECT
            GROUP BY S.ID;
        """
        
        cursor = self.db.execute_query(query)
        
        self.datos_tabla = [
            {"id" : id,
             "codigo" : code,
             "nombre" : name,
             "progress" : progress}
            for (id, code, name, progress) in cursor
        ]
        
        self.datos_filtrados = self.datos_tabla
        pass 
    
    def crear_temas(self):
        # Crear tema personalizado
        with dpg.theme() as self.global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, self.COLOR_BG_DARK)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.COLOR_BG_LIGHT)
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.COLOR_TEXT)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 5, 3)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 4)
        
        # Tema para botones de acción
        with dpg.theme() as self.theme_btn_ver:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, self.COLOR_BUTTON_VIEW)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.COLOR_BUTTON_VIEW_HOVER)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
        
        with dpg.theme() as self.theme_btn_eliminar:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, self.COLOR_BUTTON_DELETE)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.COLOR_BUTTON_DELETE_HOVER)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
        
        with dpg.theme() as self.theme_header:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text, [220, 220, 255, 255])
                
        with dpg.theme() as self.theme_filter:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.COLOR_FILTER_BG)
    
            # Tema para botones de eliminación
        with dpg.theme() as self.tema_eliminar:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [230, 100, 100, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [255, 130, 130, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [210, 80, 80, 255])
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3)
                
    def setup_ui(self):
        
        with dpg.group(parent=self.window_tag, width=800, height=600):
            dpg.add_text("Sistema de Gestión de Materias Académicas")
            dpg.add_separator()
            
            with dpg.child_window(tag="filtros_container", width=-1, height=80, border=True):
                dpg.add_text("Filtros de Búsqueda")
                with dpg.group(horizontal=True):
                    # Filtro por código
                    dpg.add_text("Código:")
                    dpg.add_input_text(tag="filtro_codigo", width=100, callback=self.aplicar_filtros)
                    dpg.add_spacer(width=10)
                    
                    # Filtro por nombre
                    dpg.add_text("Nombre:")
                    dpg.add_input_text(tag="filtro_nombre_1", width=200, callback=self.aplicar_filtros)
                    dpg.add_spacer(width=10)
                    
                    # Filtro por créditos

                with dpg.group(horizontal=True):
                    dpg.add_button(label="Limpiar Filtros", callback=self.limpiar_filtros)
                    dpg.add_button(label="Aplicar Filtros", callback=self.aplicar_filtros)
            
            dpg.add_separator()
            
            # Contenedor con scroll para la tabla
            dpg.add_child_window(tag="tabla_container", width=-1, height=400, horizontal_scrollbar=True)
            
            # Botón para agregar nuevas filas
            dpg.add_button(label="Agregar Nueva Materia", callback=self.agregar_fila)
            
            # Información de estadísticas
            with dpg.group(horizontal=True):
                dpg.add_text("Total de materias: ")
                dpg.add_text(str(len(self.datos_tabla)), tag="total_materias")
                dpg.add_spacer(width=20)
                dpg.add_text("Materias mostradas: ")
                dpg.add_text(str(len(self.datos_filtrados)), tag="materias_mostradas")
        
        # Aplicar tema global
        dpg.bind_theme(self.global_theme)
        dpg.bind_item_theme("filtros_container", self.theme_filter)
        
        # Actualizar tabla inicial
        self.actualizar_tabla()
    
    def actualizar_tabla(self):
        # Limpiar la tabla existente
        dpg.delete_item("tabla_container", children_only=True)
        
        # Actualizar contadores
        
        dpg.set_value("materias_mostradas", len(self.datos_filtrados))
        #dpg.set_value("total_materias", str(len(self.datos_tabla)))
        #dpg.set_value("materias_mostradas", str(len(self.datos_filtrados)))
        
        # Agregar encabezados de tabla
        with dpg.table(header_row=True, borders_innerH=True, borders_outerH=True,
                      borders_innerV=True, borders_outerV=True, tag="tabla_materias", 
                      parent="tabla_container"):
            
            # Definir columnas
            dpg.add_table_column(label="ID", width_fixed=True, width=50)
            dpg.add_table_column(label="Codigo", width_fixed=True, width=100)
            dpg.add_table_column(label="Nombre", width_stretch=True, init_width_or_weight=250)
            dpg.add_table_column(label="Creditos", width_fixed=True, width=150)
            dpg.add_table_column(label="Detalles", width_fixed=True, width=1250)
            dpg.add_table_column(label="Eliminar", width_fixed=True, width=1250)
            
            # Agregar filas con datos filtrados
            for i, dato in enumerate(self.datos_filtrados):
                with dpg.table_row():
                    dpg.add_text(f"{dato['id']}")
                    dpg.add_text(f"{dato['codigo']}")
                    dpg.add_text(f"{dato['nombre']}")
                    dpg.add_progress_bar(label = "hola", width=-1,  default_value=dato["progress"], overlay=f"{dato["progress"]*100}%")
                    
                    
                    # Columna de acciones
                    btn_ver = dpg.add_button(label="Ver", width=70, callback=lambda s, a, u: self.ver_detalles(u), user_data=dato)
                    btn_eliminar = dpg.add_button(label="Eliminar", width=70, callback=lambda s, a, u: self.eliminar_fila(u), user_data=dato['id'])
                    
                    dpg.bind_item_theme(btn_eliminar, self.tema_eliminar)
                    
                        # Aplicar temas a los botones
                        #dpg.bind_item_theme(btn_ver, self.theme_btn_ver)
                        #dpg.bind_item_theme(btn_eliminar, self.theme_btn_eliminar)
    
    def ver_detalles(self, materia):
        with dpg.window(label=f"Detalles de Materia", modal=True, 
                      width=350, height=200, pos=[100, 100], no_resize=True):
            dpg.add_text(f"ID: {materia['id']}")
            dpg.add_text(f"Código: {materia['codigo']}")
            dpg.add_text(f"Nombre: {materia['nombre']}")
            dpg.add_text(f"Créditos: {materia['creditos']}")
            dpg.add_separator()
            dpg.add_button(label="Cerrar", callback=lambda: dpg.delete_item(dpg.last_container()))
    
    def eliminar_fila(self, id_subject):
        # Ventana de confirmación
        with dpg.window(label="Confirmar eliminación", modal=True, width=300, height=150, pos=[120, 120], no_resize=True, tag = "accept_delete_subject"):
            dpg.add_text(f"¿Está seguro que desea eliminar la materia ID: {id_subject}?")
            
            with dpg.group(horizontal=True):
                dpg.add_button(label="Cancelar", width=100, callback=lambda: dpg.delete_item("accept_delete_subject"))
                
                def confirmar_eliminar():
                    # Filtrar la materia a eliminar
                    self.db.subjects.remove(id_subject)
                    # Actualizar también los datos filtrados
                    self.update_subjects()
                    self.aplicar_filtros()
                    dpg.delete_item("accept_delete_subject")
                    windows_manager.notification_system.show_notification(f"Se ah Eliminado la materia con ID = {id_subject}", 3, "success")

                    
                dpg.add_button(label="Eliminar", width=100, callback=confirmar_eliminar)
    
    
    def agregar_fila(self):
        global windows_manager
    
        windows_manager.show_window(NEW_SUBJECT_WINDOW_TAG)
        

    def aplicar_filtros(self, sender=None, app_data=None, user_data=None):
        # Obtener valores de filtros
        filtro_codigo = dpg.get_value("filtro_codigo").upper() if dpg.get_value("filtro_codigo") else ""
        filtro_nombre = dpg.get_value("filtro_nombre").upper() if dpg.get_value("filtro_nombre") else ""
        
        # Aplicar filtros
        self.datos_filtrados = []
        for materia in self.datos_tabla:
            cumple_filtro = True
            
            # Filtrar por código
            if filtro_codigo and filtro_codigo not in materia['codigo'].upper():
                cumple_filtro = False
                
            # Filtrar por nombre
            if filtro_nombre and filtro_nombre not in materia['nombre'].upper():
                cumple_filtro = False
                
            # Filtrar por créditos
            cumple_filtro = True
                
            if cumple_filtro:
                self.datos_filtrados.append(materia)
        
        # Actualizar tabla con datos filtrados
        self.actualizar_tabla()
    
    def limpiar_filtros(self):
        # Resetear valores de filtros
        dpg.set_value("filtro_codigo", "")
        dpg.set_value("filtro_nombre", "")
        dpg.set_value("filtro_creditos", "Todos")
        
        # Mostrar todos los datos
        self.datos_filtrados = self.datos_tabla.copy()
        self.actualizar_tabla()
        
    def set_mode(self, mode, mode_id):
        self.mode = mode 
        self.mode_id = mode_id
        
        self.update_subjects()
        self.actualizar_tabla()
        
    def update(self):
        if self.is_visible():
            self.set_mode(self.mode, self.mode_id)
        