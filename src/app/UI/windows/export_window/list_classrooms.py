import dearpygui.dearpygui as dpg
import random
from typing import List, Dict, Tuple, Callable, Any, Optional

class ListaGenericaApp:
    """Clase base para manejo de listas seleccionables (aulas, profesores, grupos)"""
    
    def __init__(self, db, entity_name="element"):
        self.db = db
        self.entity_name = entity_name  # Nombre de la entidad (aula, profesor, grupo)
        self.items: List[str] = []
        self.seleccion_items: Dict[str, bool] = {}
        self.items_con_indice: List[Tuple[str, int]] = []
        self.search_tag = f"busqueda_{self.entity_name}"
        self.table_tag = f"tabla_{self.entity_name}"
        self.selected_items_tag = f"{self.entity_name}_seleccionados"
        self.selected_ids_tag = f"ids_seleccionados_{self.entity_name}"
        self.table_container_tag = f"tabla_container_{self.entity_name}"

    def _inicializar_datos(self):
        """Inicializa los datos y estructuras auxiliares.
        Este método debe ser sobrescrito por las clases hijas."""
        pass

    def setup_ui(self, parent):
        """Configura la interfaz gráfica."""
        with dpg.group(parent=parent):
            # Área de búsqueda
            with dpg.group(horizontal=True):
                dpg.add_text("Buscar:")
                dpg.add_input_text(
                    tag=self.search_tag,
                    width=300,
                    callback=lambda s, a: self.ordenar_por_coincidencia(s, a)
                )
            dpg.add_spacer(height=5)
            
            # Botones de selección
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Seleccionar Todos",
                    callback=lambda: self.seleccionar_todos(),
                    width=150
                )
                dpg.add_button(
                    label="Deseleccionar Todos",
                    callback=lambda: self.deseleccionar_todos(),
                    width=150
                )
                dpg.add_button(
                    label="Exportar",
                    callback=self.exportar,
                    width=150
                )
            dpg.add_spacer(height=10)
            
            # Tabla 
            with dpg.child_window(width=550, height=300, tag=self.table_container_tag):
                # Crear tabla
                with dpg.table(tag=self.table_tag, header_row=True, borders_innerH=True, 
                              borders_outerH=True, borders_innerV=True, borders_outerV=True,
                              resizable=True, policy=dpg.mvTable_SizingStretchProp):
                    
                    # Definir columnas base - pueden ser sobrescritas
                    self.setup_table_columns()
            
            dpg.add_spacer(height=10)
            
            # Botón y área de selección
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label=f"Mostrar {self.entity_name.capitalize()} Seleccionados",
                    callback=lambda: self.mostrar_seleccionados()
                )
                dpg.add_button(
                    label="Mostrar IDs Seleccionados",
                    callback=lambda: self.mostrar_ids_seleccionados()
                )
            
            dpg.add_text(f"{self.entity_name.capitalize()} seleccionados:", bullet=True)
            dpg.add_text(
                f"Ningún {self.entity_name} seleccionado",
                tag=self.selected_items_tag,
                wrap=500
            )
            
            dpg.add_text("IDs seleccionados:", bullet=True)
            dpg.add_text(
                "Ningún ID seleccionado",
                tag=self.selected_ids_tag,
                wrap=500
            )
            
        # Inicializar tabla
        self._inicializar_datos()  # Asegurar que tenemos datos antes de ordenar
        self.ordenar_por_coincidencia(None, None)

    def setup_table_columns(self):
        """Configura las columnas de la tabla. Puede ser sobrescrita."""
        dpg.add_table_column(label="Selección", width_fixed=True, init_width_or_weight=60)
        dpg.add_table_column(label="ID")
        dpg.add_table_column(label="Nombre")

    def ordenar_por_coincidencia(self, sender, app_data):
        """Ordena items según coincidencia con el término de búsqueda."""
        termino = dpg.get_value(self.search_tag).lower() if dpg.does_item_exist(self.search_tag) else ""
        
        if not termino:
            items_ordenados = self.items.copy()
        else:
            def calcular_puntuacion(item):
                name = item["name"]
                id = item["id"]
                
                name_lower = name.lower()
                if name_lower.startswith(termino):
                    return (3, id)
                elif termino in name_lower:
                    return (2, id)
                elif any(p in name_lower for p in termino.split()):
                    return (1, id)
                return (0, id)
            
            items_ordenados = sorted(
                self.items,
                key=calcular_puntuacion,
                reverse=True
            )
        
        self._actualizar_tabla_ui(items_ordenados)

    def _actualizar_tabla_ui(self, items_ordenados: List[Tuple[str, int]]):
        """Actualiza la UI con la tabla ordenada de items."""
        # Limpiar tabla existente
        if dpg.does_item_exist(self.table_tag):
            dpg.delete_item(self.table_tag, children_only=True, slot=1)  # Borra solo las filas, no las columnas
        
        # Mostrar las primeras 100 items
        items_mostrados = items_ordenados[:100]
        
        # Añadir filas a la tabla
        for item in items_mostrados:
            with dpg.table_row(parent=self.table_tag):
                # Columna de selección
                dpg.add_checkbox(
                    default_value=self.seleccion_items.get(item["id"], False),
                    callback=lambda s, a, u: self._actualizar_seleccion(u),
                    user_data = item
                )
                # Columna ID
                dpg.add_text(f"{item["id"]}")
                dpg.add_text(f"{item["name"]}")
                # Columna Nombre - puede ser sobrescrita
                #self.render_item_row(item["name"], item["id"])
        
        # Mostrar mensaje si hay más de 100 items
        if len(items_ordenados) > 100:
            with dpg.table_row(parent=self.table_tag):
                dpg.add_text("")
                dpg.add_text("")
                dpg.add_text(f"Mostrando 100 de {len(items_ordenados)} {self.entity_name}...")

    def render_item_row(self, item: str, idx: int):
        """Renderiza las celdas específicas para un item (excluyendo checkbox y ID).
        Puede ser sobrescrita por clases hijas para mostrar más columnas."""
        dpg.add_text(item)

    def _actualizar_seleccion(self, item):
        """Cambia el estado de selección de un item."""
        print(self.seleccion_items)
        is_selected = self.seleccion_items[item["id"]]
        self.seleccion_items[item["id"]] = not is_selected
            
    def seleccionar_todos(self):
        """Marca todos los items como seleccionados."""
        for item in self.items:
            self.seleccion_items[item["id"]] = True
        self.ordenar_por_coincidencia(None, None)

    def deseleccionar_todos(self):
        """Desmarca todos los items."""
        for item in self.items:
            self.seleccion_items[item["id"]] = False
        self.ordenar_por_coincidencia(None, None)

    def mostrar_seleccionados(self):
        """Muestra los items seleccionados."""
        seleccionados = [a for a, sel in self.seleccion_items.items() if sel]
        cantidad = len(seleccionados)
        
        if cantidad == 0:
            texto = f"Ningún {self.entity_name} seleccionado"
        elif cantidad <= 10:
            texto = ", ".join(seleccionados)
        else:
            texto = f"{cantidad} {self.entity_name} seleccionados"
        
        dpg.set_value(self.selected_items_tag, texto)
    
    
    def obtener_ids_seleccionados(self):
        """Obtiene los IDs de los items seleccionados."""
        ids_seleccionados = [item["id"] for item in self.items if self.seleccion_items[item["id"]]]
        return ids_seleccionados
    
    
    def mostrar_ids_seleccionados(self):
        """Muestra los IDs de los items seleccionados en la UI."""
        ids = self.obtener_ids_seleccionados()
        cantidad = len(ids)
        print(ids)       
        return None 
     
        if cantidad == 0:
            texto = "Ningún ID seleccionado"
        elif cantidad <= 20:
            texto = ", ".join(map(str, ids))
        else:
            texto = f"{cantidad} IDs seleccionados: {', '.join(map(str, ids[:10]))}... (y {cantidad-10} más)"
        
        dpg.set_value(self.selected_ids_tag, texto)
    
    def exportar(self, sender=None, app_data=None, user_data=None):
        """Método para exportar los datos seleccionados. Debe ser implementado por clases hijas."""
        print(f"Exportando {self.entity_name}...")
        
        
import random

class ListaAulasApp(ListaGenericaApp):
    """Clase especializada para el manejo de aulas"""
    
    def __init__(self, db):
        super().__init__(db, entity_name="aula")
        self._inicializar_datos()

    def _inicializar_datos(self):
        """Inicializa la lista de aulas y estructuras auxiliares."""
        # Ejemplo inicial de aulas
        
        cursor = self.db.execute_query("""
            SELECT ID, NAME 
            FROM CLASSROOM                               
        """)
        
        
        
        self.items = [
            {"name" : name,
             "id" : id} 
            for (id, name) in cursor
        ]
        
        self.seleccion_items = {item["id"]: False for item in self.items}


    def setup_table_columns(self):
        """Configura las columnas específicas para aulas."""
        # Heredamos las columnas base
        super().setup_table_columns()
        # Podríamos añadir columnas específicas, por ejemplo:
        # dpg.add_table_column(label="Capacidad")
        # dpg.add_table_column(label="Tipo")

    def render_item_row(self, item: str, idx: int):
        """Renderiza una fila específica para aulas."""
        # En este caso simple, solo mostramos el nombre del aula
        dpg.add_text(item)
        
        # Si queremos mostrar más información, podríamos hacer un parse del nombre
        # o tener una estructura de datos más compleja para cada aula
        
    def exportar(self, sender=None, app_data=None, user_data=None):
        """Exporta los horarios de las aulas seleccionadas."""
        ids_seleccionados = self.obtener_ids_seleccionados()
        print(f"Exportando horarios de {len(ids_seleccionados)} aulas...")
        # Aquí iría la lógica para exportar los horarios de las aulas



class ListaProfesoresApp(ListaGenericaApp):
    """Clase especializada para el manejo de profesores"""
    
    def __init__(self, db):
        super().__init__(db, entity_name="profesor")
        self.profesores_info = {}  # Diccionario para almacenar información adicional
        self._inicializar_datos()

    def _inicializar_datos(self):
        """Inicializa la lista de profesores y estructuras auxiliares."""
        # Ejemplo inicial de profesores (nombre y departamento)
        cursor = self.db.execute_query("""
            SELECT ID, NAME
            FROM PROFESSOR                               
        """)
        
        # Almacenar la información completa
        
        self.items = [
            {"name" : name,
             "id" : id} 
            for (id, name) in cursor
        ]
        
        self.seleccion_items = {item["id"]: False for item in self.items}

    def setup_table_columns(self):
        """Configura las columnas específicas para aulas."""
        # Heredamos las columnas base
        super().setup_table_columns()
        # Podríamos añadir columnas específicas, por ejemplo:
        # dpg.add_table_column(label="Capacidad")
        # dpg.add_table_column(label="Tipo")

    def render_item_row(self, item: str, idx: int):
        """Renderiza una fila específica para aulas."""
        # En este caso simple, solo mostramos el nombre del aula
        dpg.add_text(item)
        
        # Si queremos mostrar más información, podríamos hacer un parse del nombre
        # o tener una estructura de datos más compleja para cada aula
        
    def exportar(self, sender=None, app_data=None, user_data=None):
        """Exporta los horarios de las aulas seleccionadas."""
        ids_seleccionados = self.obtener_ids_seleccionados()
        print(f"Exportando horarios de {len(ids_seleccionados)} aulas...")
        # Aquí iría la lógica para exportar los horarios de las aulas

