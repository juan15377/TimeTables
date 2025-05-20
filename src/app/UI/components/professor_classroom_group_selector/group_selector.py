import dearpygui.dearpygui as dpg
from typing import List, Tuple, Callable, Optional
from src.app.UI.components.items_groups_manager import ItemsGroupsManager, get_id


class GroupSelector:
    def __init__(self, db, selection_callback: Callable, default_id):
        """
        Componente selector de grupos con filtros por carrera, semestre y subgrupo
        
        Args:
            db: Conexión a la base de datos
            selection_callback: Función que se llamará cuando se seleccione un grupo
        """
        self.db = db
        self.selection_callback = selection_callback
        self.items = ItemsGroupsManager(db) 
        
        
        # Datos de grupos
        self.all_groups = []  # Lista de todos los grupos (id, carrera, semestre, subgrupo, nombre_completo)
        self.filtered_groups = []  # Grupos filtrados actuales
        
        # Tags para los componentes UI
        self.career_filter_tag = "group_career_filter_grid"
        self.semester_filter_tag = "group_semester_filter_grid"
        self.subgroup_filter_tag = "group_subgroup_filter_grid"
        self.search_input_tag = "group_search_input_grid"
        self.groups_list_tag = "groups_selector_list_grid"
        

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
                items=[""] + sorted(self.items.get_careers()),
                default_value="",
                tag=self.career_filter_tag,
                width=250,
                callback=self._apply_filters
            )
                
                # Filtro por semestre
            dpg.add_text("Semestre:")
            dpg.add_combo(
                items=[""] + sorted(self.items.get_semesters()),
                default_value="",  
                tag=self.semester_filter_tag,
                width=250,
                callback=self._apply_filters
            )
                
                # Filtro por subgrupo
            dpg.add_text("Subgrupo:")
            dpg.add_combo(
                items=[""] + sorted(self.items.get_subgroups()),
                default_value="",
                tag=self.subgroup_filter_tag,
                width=250,
                callback=self._apply_filters
            )
            
            # Campo de búsqueda
        with dpg.group(horizontal=True):
            dpg.add_text("Buscar:")
            dpg.add_input_text(
                tag=self.search_input_tag,
                width=200,
                hint="Ingrese texto para buscar...",
                callback=self._apply_filters
            )
            dpg.add_button(
                label="Limpiar",
                callback=self._clear_filters
            )
            
            
            dpg.add_text("Grupo :")
            dpg.add_combo(
                items=[""] + sorted(self.filtered_groups),
                tag=self.groups_list_tag,
                width=-1,     # Usar todo el ancho disponible
                callback=self._on_group_selected
            )
        return None 
        
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
        query = """
            SELECT ID, CAREER, SEMESTER, SUBGROUP, 
                   CAREER || ' - Sem ' || SEMESTER || ' - ' || SUBGROUP AS FULL_NAME
            FROM GROUPS
            ORDER BY CAREER, SEMESTER, SUBGROUP
        """
        
        cursor = self.db.execute_query(query)

        self.all_groups = [group["nombre"] for group in self.items.get_filtered_groups()]
        cursor.close() 
        
        self.filtered_groups = self.all_groups
    
    def _extract_filter_options(self):
        pass 
    def _format_groups_for_display(self, groups):
        """Formatea los grupos para mostrarlos en la UI"""
        return [f"{full_name} (ID: {id_})" for id_, _, _, _, full_name in groups]
    
    def _apply_filters(self, sender=None, app_data=None, user_data=None):
        """Aplica todos los filtros actuales a la lista de grupos"""
        # Obtener valores de filtros
        career_filter = get_id(dpg.get_value(self.career_filter_tag))
        semester_filter = get_id(dpg.get_value(self.semester_filter_tag))
        subgroup_filter = get_id(dpg.get_value(self.subgroup_filter_tag))
        search_text = get_id(dpg.get_value(self.search_input_tag).lower())
        
        # Aplicar filtros
        filtered = self.items.get_filtered_groups(search_text,
                                                  career_filter,
                                                  semester_filter,
                                                  subgroup_filter)
        

        # Actualizar grupos filtrados
        self.filtered_groups = filtered
        
        # Actualizar la lista en la UI
        dpg.configure_item(
            self.groups_list_tag, 
            items=[group["nombre"] for group in self.filtered_groups]
        )
    
    def _clear_filters(self, sender=None, app_data=None, user_data=None):
        """Limpia todos los filtros"""
        # Resetear combos a valores predeterminados
        dpg.set_value(self.career_filter_tag, "")
        dpg.set_value(self.semester_filter_tag, "")
        dpg.set_value(self.subgroup_filter_tag, "")
        dpg.set_value(self.search_input_tag, "")
        
        # Mostrar todos los grupos
        self.filtered_groups = self.all_groups.copy()
        dpg.configure_item(
            self.groups_list_tag, 
            items=self.all_groups
        )
    
    def _on_group_selected(self, sender, app_data, user_data):
        """Maneja la selección de un grupo de la lista"""
        if not app_data:
            return
            
        # Extraer el ID del grupo seleccionado
        try:
            selected_id = get_id(dpg.get_value(self.groups_list_tag))
            print("ID Seleccionado ", selected_id)
            # Encontrar el grupo completo
            
            # Enviar señal con el grupo seleccionado
            self.selection_callback(selected_id, selected_id, 1)
        except (IndexError, ValueError, AttributeError):
            print("Error al extraer ID del grupo seleccionado")
    
    def get_id_selected(self):
        """Devuelve el ID del grupo actualmente seleccionado"""
        selected_item = get_id(dpg.get_value(self.groups_list_tag))
        if not selected_item:
            return None
        return selected_item 

    
    def update(self):
        """Actualiza los datos del componente"""
        # Recargar datos
        self._load_groups_data()
        self._extract_filter_options()
        
        # Actualizar listas de filtros
        dpg.configure_item(self.career_filter_tag, items=[""] + sorted(self.items.get_careers()))
        dpg.configure_item(self.semester_filter_tag, items=[""] + sorted(self.items.get_semesters()))
        dpg.configure_item(self.subgroup_filter_tag, items=[""] + sorted(self.items.get_subgroups()))
        
        # Reaplicar filtros
        self._apply_filters()
