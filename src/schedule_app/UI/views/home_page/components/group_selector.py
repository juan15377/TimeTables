import dearpygui.dearpygui as dpg
from typing import List, Tuple, Callable, Optional

class GroupSelector:
    def __init__(self, db, selection_callback: Callable):
        """
        Componente selector de grupos con filtros por carrera, semestre y subgrupo
        
        Args:
            db: Conexión a la base de datos
            selection_callback: Función que se llamará cuando se seleccione un grupo
        """
        self.db = db
        self.selection_callback = selection_callback
        
        # Datos de grupos
        self.all_groups = []  # Lista de todos los grupos (id, carrera, semestre, subgrupo, nombre_completo)
        self.filtered_groups = []  # Grupos filtrados actuales
        
        # Tags para los componentes UI
        self.career_filter_tag = "group_career_filter"
        self.semester_filter_tag = "group_semester_filter"
        self.subgroup_filter_tag = "group_subgroup_filter"
        self.search_input_tag = "group_search_input"
        self.groups_list_tag = "groups_selector_list"
        
        # Datos de filtros
        self.careers = []
        self.semesters = []
        self.subgroups = []

    def setup_ui(self, parent):
        """Configura la interfaz del selector de grupos"""
        # Cargar datos iniciales
        self._load_groups_data()
        self._extract_filter_options()
        
            
        # Filtros en una fila
        with dpg.group(horizontal=True):
            # Filtro por carrera
            dpg.add_text("Carrera:")
            dpg.add_combo(
                items=["Todas"] + self.careers,
                default_value="Todas",
                tag=self.career_filter_tag,
                width=150,
                callback=self._apply_filters
            )
                
                # Filtro por semestre
            dpg.add_text("Semestre:")
            dpg.add_combo(
                items=["Todos"] + self.semesters,
                default_value="Todos",  
                tag=self.semester_filter_tag,
                width=100,
                callback=self._apply_filters
            )
                
                # Filtro por subgrupo
            dpg.add_text("Subgrupo:")
            dpg.add_combo(
                items=["Todos"] + self.subgroups,
                default_value="Todos",
                tag=self.subgroup_filter_tag,
                width=100,
                callback=self._apply_filters
            )
            
            # Campo de búsqueda
        with dpg.group(horizontal=True):
            dpg.add_text("Buscar:")
            dpg.add_input_text(
                tag=self.search_input_tag,
                width=300,
                hint="Ingrese texto para buscar...",
                callback=self._apply_filters
            )
            dpg.add_button(
                label="Limpiar",
                callback=self._clear_filters
            )
            
            
            dpg.add_text("Grupo :")
            dpg.add_combo(
                items=self._format_groups_for_display(self.filtered_groups),
                tag=self.groups_list_tag,
                width=-1,     # Usar todo el ancho disponible
                callback=self._on_group_selected
            )
        return None 
        
        with dpg.group(parent=parent):
            # Título
            dpg.add_text("Buscador de Grupos", color=[255, 255, 0])
            dpg.add_separator()
            
            # Filtros en una fila
            with dpg.group(horizontal=True):
                # Filtro por carrera
                dpg.add_text("Carrera:")
                dpg.add_combo(
                    items=["Todas"] + self.careers,
                    default_value="Todas",
                    tag=self.career_filter_tag,
                    width=150,
                    callback=self._apply_filters
                )
                
                # Filtro por semestre
                dpg.add_text("Semestre:")
                dpg.add_combo(
                    items=["Todos"] + self.semesters,
                    default_value="Todos",  
                    tag=self.semester_filter_tag,
                    width=100,
                    callback=self._apply_filters
                )
                
                # Filtro por subgrupo
                dpg.add_text("Subgrupo:")
                dpg.add_combo(
                    items=["Todos"] + self.subgroups,
                    default_value="Todos",
                    tag=self.subgroup_filter_tag,
                    width=100,
                    callback=self._apply_filters
                )
            
            # Campo de búsqueda
            with dpg.group(horizontal=True):
                dpg.add_text("Buscar:")
                dpg.add_input_text(
                    tag=self.search_input_tag,
                    width=300,
                    hint="Ingrese texto para buscar...",
                    callback=self._apply_filters
                )
                dpg.add_button(
                    label="Limpiar",
                    callback=self._clear_filters
                )
            
            dpg.add_separator()
            
            # Lista de grupos
        dpg.add_text("Grupos encontrados:")
        dpg.add_combo(
            items=self._format_groups_for_display(self.filtered_groups),
            tag=self.groups_list_tag,
            width=-1,     # Usar todo el ancho disponible
            callback=self._on_group_selected
        )
    
    def _load_groups_data(self):
        """Carga todos los grupos desde la base de datos"""
        cursor = self.db.db_connection.cursor()
        cursor.execute("""
            SELECT ID, CAREER, SEMESTER, SUBGROUP, 
                   CAREER || ' - Sem ' || SEMESTER || ' - ' || SUBGROUP AS FULL_NAME
            FROM GROUPS
            ORDER BY CAREER, SEMESTER, SUBGROUP
        """)
        self.all_groups = cursor.fetchall()
        self.filtered_groups = self.all_groups.copy()
    
    def _extract_filter_options(self):
        """Extrae opciones únicas para los filtros"""
        # Extraer carreras únicas
        self.careers = sorted(list(set(group[1] for group in self.all_groups)))
        
        # Extraer semestres únicos
        self.semesters = sorted(list(set(str(group[2]) for group in self.all_groups)))
        
        # Extraer subgrupos únicos
        self.subgroups = sorted(list(set(group[3] for group in self.all_groups)))
    
    def _format_groups_for_display(self, groups):
        """Formatea los grupos para mostrarlos en la UI"""
        return [f"{full_name} (ID: {id_})" for id_, _, _, _, full_name in groups]
    
    def _apply_filters(self, sender=None, app_data=None, user_data=None):
        """Aplica todos los filtros actuales a la lista de grupos"""
        # Obtener valores de filtros
        career_filter = dpg.get_value(self.career_filter_tag)
        semester_filter = dpg.get_value(self.semester_filter_tag)
        subgroup_filter = dpg.get_value(self.subgroup_filter_tag)
        search_text = dpg.get_value(self.search_input_tag).lower()
        
        # Aplicar filtros
        filtered = self.all_groups.copy()
        
        # Filtro por carrera
        if career_filter != "Todas":
            filtered = [g for g in filtered if g[1] == career_filter]
        
        # Filtro por semestre
        if semester_filter != "Todos":
            filtered = [g for g in filtered if str(g[2]) == semester_filter]
        
        # Filtro por subgrupo
        if subgroup_filter != "Todos":
            filtered = [g for g in filtered if g[3] == subgroup_filter]
        
        # Filtro por texto de búsqueda
        if search_text:
            filtered = [g for g in filtered if search_text in g[4].lower()]
        
        # Actualizar grupos filtrados
        self.filtered_groups = filtered
        
        # Actualizar la lista en la UI
        dpg.configure_item(
            self.groups_list_tag, 
            items=self._format_groups_for_display(filtered)
        )
    
    def _clear_filters(self, sender=None, app_data=None, user_data=None):
        """Limpia todos los filtros"""
        # Resetear combos a valores predeterminados
        dpg.set_value(self.career_filter_tag, "Todas")
        dpg.set_value(self.semester_filter_tag, "Todos")
        dpg.set_value(self.subgroup_filter_tag, "Todos")
        dpg.set_value(self.search_input_tag, "")
        
        # Mostrar todos los grupos
        self.filtered_groups = self.all_groups.copy()
        dpg.configure_item(
            self.groups_list_tag, 
            items=self._format_groups_for_display(self.filtered_groups)
        )
    
    def _on_group_selected(self, sender, app_data, user_data):
        """Maneja la selección de un grupo de la lista"""
        if not app_data:
            return
            
        # Extraer el ID del grupo seleccionado
        try:
            selected_id = int(app_data.split("ID: ")[1].rstrip(")"))
            
            # Encontrar el grupo completo
            selected_group = next((g for g in self.filtered_groups if g[0] == selected_id), None)
            
            if selected_group:
                # Enviar señal con el grupo seleccionado
                self.selection_callback(selected_id, selected_group)
        except (IndexError, ValueError, AttributeError):
            print("Error al extraer ID del grupo seleccionado")
    
    def get_selected_group_id(self):
        """Devuelve el ID del grupo actualmente seleccionado"""
        selected_item = dpg.get_value(self.groups_list_tag)
        if not selected_item:
            return None
            
        try:
            selected_id = int(selected_item.split("ID: ")[1].rstrip(")"))
            return selected_id
        except (IndexError, ValueError, AttributeError):
            return None
    
    def update(self):
        """Actualiza los datos del componente"""
        # Recargar datos
        self._load_groups_data()
        self._extract_filter_options()
        
        # Actualizar listas de filtros
        dpg.configure_item(self.career_filter_tag, items=["Todas"] + self.careers)
        dpg.configure_item(self.semester_filter_tag, items=["Todos"] + self.semesters)
        dpg.configure_item(self.subgroup_filter_tag, items=["Todos"] + self.subgroups)
        
        # Reaplicar filtros
        self._apply_filters()
