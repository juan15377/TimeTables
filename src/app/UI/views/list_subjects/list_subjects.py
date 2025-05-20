from src.app.database import database_manager
from src.app.UI.views.new_subject.new_subject import SubjectRegistrationWindow
import dearpygui.dearpygui as dpg
from src.app.UI.components.windows_manager import Window, windows_manager



class GestorMaterias(Window):
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
            window_tag = "list_subjects_window",
            label = f"materia de {mode_id}",
            on_close= lambda s, a, u : print(10)
        )
        
        #self.create()
        
        
    def update_subjects(self):
        
        if self.mode_id is None:
            self.datos_tabla = []
            self.datos_filtrados = []
            return None 
        
        cursor = self.db.execute_query(f"""
        SELECT A.ID, A.CODE, A.NAME, B.PROGRESS
        FROM SUBJECT A
		JOIN(
		
		SELECT A.ID, CAST(B.COMPLETED_SLOTS AS REAL) / CAST(A.TOTAL_SLOTS AS REAL) AS PROGRESS
		FROM SUBJECT A 
		JOIN (
			SELECT A.ID, coalesce(B.LEN, 0) AS COMPLETED_SLOTS
			FROM SUBJECT A
			LEFT JOIN SUBJECT_SLOTS B ON A.ID = B.ID_SUBJECT
			GROUP BY A.ID
			) B ON A.ID = B.ID

		
		) B ON A.ID = B.ID
		WHERE A.ID IN (
				SELECT ID_SUBJECT
				FROM {self.mode}_SUBJECT
				WHERE ID_{self.mode} = {self.mode_id}
			);
        
        """)
        
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
                
        # Tema para área de filtro
        with dpg.theme() as self.theme_filter:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.COLOR_FILTER_BG)
    
    def setup_ui(self):
        # Crear la ventana principal y viewport
        
        with dpg.group(parent=self.window_tag, width=800, height=600):
            dpg.add_text("Sistema de Gestión de Materias Académicas")
            dpg.add_separator()
            
            # Sección de filtros
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
        #dpg.set_value("total_materias", str(len(self.datos_tabla)))
        #dpg.set_value("materias_mostradas", str(len(self.datos_filtrados)))
        
        # Agregar encabezados de tabla
        with dpg.table(header_row=True, borders_innerH=True, borders_outerH=True,
                      borders_innerV=True, borders_outerV=True, tag="tabla_materias", 
                      parent="tabla_container"):
            
            # Definir columnas
            dpg.add_table_column(label="ID", width_fixed=True, width=50)
            dpg.add_table_column(label="CÓDIGO", width_fixed=True, width=100)
            dpg.add_table_column(label="NOMBRE", width_stretch=True, init_width_or_weight=250)
            dpg.add_table_column(label="CRÉDITOS", width_fixed=True, width=150)
            dpg.add_table_column(label="ACCIONES", width_fixed=True, width=1250)
            
            # Agregar filas con datos filtrados
            for i, dato in enumerate(self.datos_filtrados):
                with dpg.table_row():
                    dpg.add_text(f"{dato['id']}")
                    dpg.add_text(f"{dato['codigo']}")
                    dpg.add_text(f"{dato['nombre']}")
                    dpg.add_progress_bar(label = "hola", width=-1,  default_value=dato["progress"], overlay=f"{dato["progress"]*100}%")
                    
                    # Columna de acciones
                    with dpg.group(horizontal=True):
                        btn_ver = dpg.add_button(label="Ver", width=70, callback=lambda s, a, u: self.ver_detalles(u), user_data=dato)
                        dpg.add_spacer(width=5)
                        btn_eliminar = dpg.add_button(label="Eliminar", width=70, callback=lambda s, a, u: self.eliminar_fila(u), user_data=dato['id'])
                        
                        # Aplicar temas a los botones
                        dpg.bind_item_theme(btn_ver, self.theme_btn_ver)
                        dpg.bind_item_theme(btn_eliminar, self.theme_btn_eliminar)
    
    def ver_detalles(self, materia):
        with dpg.window(label=f"Detalles de Materia", modal=True, 
                      width=350, height=200, pos=[100, 100], no_resize=True):
            dpg.add_text(f"ID: {materia['id']}")
            dpg.add_text(f"Código: {materia['codigo']}")
            dpg.add_text(f"Nombre: {materia['nombre']}")
            dpg.add_text(f"Créditos: {materia['creditos']}")
            dpg.add_separator()
            dpg.add_button(label="Cerrar", callback=lambda: dpg.delete_item(dpg.last_container()))
    
    def eliminar_fila(self, id_materia):
        # Ventana de confirmación
        with dpg.window(label="Confirmar eliminación", modal=True, width=300, height=150, pos=[120, 120], no_resize=True):
            dpg.add_text(f"¿Está seguro que desea eliminar la materia ID: {id_materia}?")
            
            with dpg.group(horizontal=True):
                dpg.add_button(label="Cancelar", width=100, callback=lambda: dpg.delete_item(dpg.last_container()))
                
                def confirmar_eliminar():
                    # Filtrar la materia a eliminar
                    self.datos_tabla = [m for m in self.datos_tabla if m['id'] != id_materia]
                    # Actualizar también los datos filtrados
                    self.aplicar_filtros()
                    dpg.delete_item(dpg.last_container())
                    
                dpg.add_button(label="Eliminar", width=100, callback=confirmar_eliminar)
    
    def agregar_fila(self):
        global windows_manager
    
        windows_manager.show_window("new_subject_window")
        

    def aplicar_filtros(self, sender=None, app_data=None, user_data=None):
        # Obtener valores de filtros
        filtro_codigo = dpg.get_value("filtro_codigo").upper() if dpg.get_value("filtro_codigo") else ""
        filtro_nombre = dpg.get_value("filtro_nombre").upper() if dpg.get_value("filtro_nombre") else ""
        filtro_creditos = dpg.get_value("filtro_creditos")
        
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
            if filtro_creditos != "Todos" and int(filtro_creditos) != materia['creditos']:
                cumple_filtro = False
                
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
        self.mode = mode, 
        self.mode_id 
        
        self.update_subjects()
        self.actualizar_tabla()
        
    
    def run(self):
        # Configuración final y lanzamiento
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("ventana_principal", True)
        dpg.start_dearpygui()
        dpg.destroy_context()

