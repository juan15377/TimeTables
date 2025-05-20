import dearpygui.dearpygui as dpg
from typing import List, Tuple, Callable, Optional
from src.app.UI.components.items_groups_manager import ItemsGroupsManager, get_id


class CreateSubjectGroupsSelector:
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
        self.career_filter_tag = "group_career_filter_create_subject"
        self.semester_filter_tag = "group_semester_filter_create_subject"
        self.subgroup_filter_tag = "group_subgroup_filter_create_subject"
        self.search_input_tag = "group_search_input_create_subject"
        self.groups_list_tag = "groups_selector_list_create_subject"
        
        self.groups = []
        

    def setup_ui(self):
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
            
        dpg.add_button(label = "añadir", callback= self.add_group)
        
            # Lista de grupos con mejor espaciado
        with dpg.child_window(height=200, tag="lista_grupos_create_subject", border=True):
             # Limpiar la tabla existente
    
    # Agregar encabezados de tabla
            with dpg.table(header_row=True, borders_innerH=True, borders_outerH=True,
                        borders_innerV=True, borders_outerV=True, tag="table_groups_create_subject", 
                        parent="tabla_container"):
                
                # Definir columnas
                dpg.add_table_column(label="ID", width_fixed=True, width=50)
                dpg.add_table_column(label="Carrera", width_fixed=True, width=100)
                dpg.add_table_column(label="Semestre", width_stretch=True, init_width_or_weight=250)
                dpg.add_table_column(label="Subgrupo", width_fixed=True, width=80)
                dpg.add_table_column(label="Eliminar", width_fixed=True, width=170)
        
       
            pass  # Se llenará con actualizar_lista_grupos
            
    def add_group(self, sender, app_data, user_data):
        group_id = get_id(dpg.get_value(self.groups_list_tag))
        
        if group_id is None or group_id in self.groups:
            return None 
        
        
        self.groups.append(group_id)
        
        self.update_groups()
        
        pass 
    
    def update_groups(self):
        dpg.delete_item("table_groups_create_subject")
        
        def delete_group(sender, app_data, group_id):
            self.groups.remove(group_id)
            self.update_groups()
            pass

        with dpg.table(header_row=True, borders_innerH=True, borders_outerH=True,
                    borders_innerV=True, borders_outerV=True, tag="table_groups_create_subject", 
                    parent="lista_grupos_create_subject"):
            
            # Definir columnas

            dpg.add_table_column(label="ID", width_fixed=True, width=50)
            dpg.add_table_column(label="Carrera", width_fixed=True, width=100)
            dpg.add_table_column(label="Semestre", width_stretch=True, init_width_or_weight=250)
            dpg.add_table_column(label="Subgrupo", width_fixed=True, width=80)
            dpg.add_table_column(label="Eliminar", width_fixed=True, width=300)
        
            # Agregar filas con datos
            for group in self.get_info_groups():
                # Alternar colores para filas pares e impares para mejor legibilidad
                
                with dpg.table_row():
                    dpg.add_text(f"{group['id']}")
                    dpg.add_text(f"{group['career']}")
                    dpg.add_text(f"{group['semester']}")
                    dpg.add_text(f"{group['subgroup']}")
                    dpg.add_button(label = "X", width=-1, callback= delete_group, user_data=group["id"])
                    

        pass
            
    def get_info_groups(self):
        """Carga todos los grupos desde la base de datos"""
        placeholders = "(" + ",".join(["?" for group in self.groups]) +  ")"
        query = f"""
            SELECT G.ID, C.NAME, S.NAME, SG.NAME
            FROM GROUPS G
            JOIN CAREER C ON G.CAREER = C.ID 
            JOIN SEMESTER S ON G.SEMESTER = S.ID
            JOIN SUBGROUP SG ON G.SUBGROUP = SG.ID
            WHERE G.ID IN {placeholders}
        """
        
        cursor = self.db.execute_query(query, self.groups)
        
        return [
            {
            "id" : id,
            "career" : career,
            "semester" : semester,
            "subgroup" : subgroup
            }
            for (id, career, semester, subgroup) in cursor
        ]
        

        
    def get_name_group(self, group_id):
        """Carga todos los grupos desde la base de datos"""
        query = f"""
            SELECT G.ID, C.NAME, S.NAME, SG.NAME
            FROM GROUPS G
            JOIN CAREER C ON G.CAREER = C.ID 
            JOIN SEMESTER S ON G.SEMESTER = S.ID
            JOIN SUBGROUP SG ON G.SUBGROUP = SG.ID
            WHERE G.ID = ?
        """
        
        cursor = self.db.execute_query(query,(group_id,))
        
        cursor = cursor.fetchone()
        
        name = cursor[1] +  "|" + cursor[2] + "|" + cursor[3] + "|" + f"(id = {cursor[0]} ) "
        return name 
    
        pass 
    
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
    
    def get_groups_ids(self):
        return self.groups
    
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

    def get_ids_groups(self):
        pass  
    
    def set_ids_groups(self):
        pass 


