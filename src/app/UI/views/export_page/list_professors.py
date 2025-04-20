import dearpygui.dearpygui as dpg
import random
from typing import List, Dict, Tuple

class ListaProfesoresApp:
    def __init__(self, db):
        # Ahora los profesores son diccionarios con id y nombre
        self.profesores: List[Dict[str, str]] = []
        self.seleccion_profesores: Dict[str, bool] = {}  # Clave: id del profesor
        self.profesores_con_indice: List[Tuple[Dict[str, str], int]] = []
        self.db = db 
        
        self._inicializar_datos()
        self.setup_ui()
    
    def _inicializar_datos(self):
        """Inicializa la lista de profesores y estructuras auxiliares."""
        # Ejemplo inicial con IDs
        cursor = self.db.execute_query("""
            SELECT *
            FROM PROFESSOR;
        """)
        
        profesores_iniciales = [
            {"id": id , "nombre" : name} for (id, name) in cursor.fetchall()
        ]
        
        self.profesores = profesores_iniciales.copy()
   
        # Estructuras para gestión eficiente
        self.seleccion_profesores = {profesor["id"]: False for profesor in self.profesores}
        self.profesores_con_indice = [(profesor, i) for i, profesor in enumerate(self.profesores)]
    
    def setup_ui(self):
        """Configura la interfaz gráfica."""

        with dpg.group():
            # Área de búsqueda
            with dpg.group(horizontal=True):
                dpg.add_text("Buscar:")
                dpg.add_input_text(
                    tag="busqueda", 
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
                    label="Exportar Seleccionados", 
                    callback=lambda: self.exportar_seleccionados(), 
                    width=150
                )
            
            dpg.add_spacer(height=10)
            
            # Lista de profesores con tabla
            with dpg.child_window(width=650, height=300, tag="lista_profesores"):
                pass  # Se llena dinámicamente con una tabla
            
            dpg.add_spacer(height=10)
            
            # Botón y área de selección
            dpg.add_button(
                label="Mostrar Profesores Seleccionados", 
                callback=lambda: self.mostrar_seleccionados()
            )
            dpg.add_text("Profesores seleccionados:", bullet=True)
            dpg.add_text(
                "Ningún profesor seleccionado", 
                tag="profesores_seleccionados", 
                wrap=600
            )
            
            # Botón para obtener IDs seleccionados
            dpg.add_button(
                label="Obtener IDs Seleccionados", 
                callback=lambda: self.mostrar_ids_seleccionados()
            )
            dpg.add_text("IDs seleccionados:", bullet=True)
            dpg.add_text(
                "Ningún ID seleccionado", 
                tag="ids_seleccionados", 
                wrap=600
            )
        
        # Inicializar lista
        self.ordenar_por_coincidencia(None, None)
        
    
    def ordenar_por_coincidencia(self, sender, app_data):
        """Ordena profesores según coincidencia con el término de búsqueda."""
        termino = dpg.get_value("busqueda").lower() if dpg.does_item_exist("busqueda") else ""
        
        if not termino:
            profesores_ordenados = self.profesores_con_indice.copy()
        else:
            def calcular_puntuacion(item):
                profesor, idx = item
                nombre_lower = profesor["nombre"].lower()
                id_lower = profesor["id"].lower()
                
                # Priorizar coincidencias tanto en nombre como en ID
                if nombre_lower.startswith(termino) or id_lower.startswith(termino):
                    return (3, idx)
                elif termino in nombre_lower or termino in id_lower:
                    return (2, idx)
                elif any(p in nombre_lower for p in termino.split()) or any(p in id_lower for p in termino.split()):
                    return (1, idx)
                return (0, idx)
            
            profesores_ordenados = sorted(
                self.profesores_con_indice,
                key=calcular_puntuacion,
                reverse=True
            )
        
        self._actualizar_lista_ui(profesores_ordenados)
    
    def _actualizar_lista_ui(self, items_ordenados: List[Tuple[Dict[str, str], int]]):
        """Actualiza la UI con la lista ordenada de profesores."""
        if dpg.does_item_exist("lista_profesores"):
            dpg.delete_item("lista_profesores", children_only=True)
            
            # Usar tabla para mostrar ID y nombre en columnas
            with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit,
                         borders_innerH=True, borders_outerH=True, borders_innerV=True,
                         borders_outerV=True, parent="lista_profesores"):
                
                # Definir columnas
                dpg.add_table_column(label="", width_fixed=True)  # Para checkbox
                dpg.add_table_column(label="ID")
                dpg.add_table_column(label="Nombre")
                
                # Mostrar datos
                items_mostrados = items_ordenados[:100]
                for profesor, _ in items_mostrados:
                    with dpg.table_row():
                        dpg.add_checkbox(
                            default_value=self.seleccion_profesores[profesor["id"]],
                            callback=lambda s, a, u: self._actualizar_seleccion(u),
                            user_data=profesor["id"]
                        )
                        dpg.add_text(profesor["id"])
                        dpg.add_text(profesor["nombre"])
            
            if len(items_ordenados) > 100:
                dpg.add_text(
                    f"Mostrando 100 de {len(items_ordenados)} profesores...",
                    parent="lista_profesores"
                )
    
    def _actualizar_seleccion(self, profesor_id: str):
        """Cambia el estado de selección de un profesor."""
        self.seleccion_profesores[profesor_id] = not self.seleccion_profesores[profesor_id]
    
    def seleccionar_todos(self):
        """Marca todos los profesores como seleccionados."""
        for profesor in self.profesores:
            self.seleccion_profesores[profesor["id"]] = True
        self.ordenar_por_coincidencia(None, None)
    
    def deseleccionar_todos(self):
        """Desmarca todos los profesores."""
        for profesor in self.profesores:
            self.seleccion_profesores[profesor["id"]] = False
        self.ordenar_por_coincidencia(None, None)
    
    def mostrar_seleccionados(self):
        """Muestra los profesores seleccionados."""
        seleccionados = []
        for profesor in self.profesores:
            if self.seleccion_profesores[profesor["id"]]:
                seleccionados.append(f"{profesor['id']} - {profesor['nombre']}")
        
        cantidad = len(seleccionados)
        
        if cantidad == 0:
            texto = "Ningún profesor seleccionado"
        elif cantidad <= 10:
            texto = ", ".join(seleccionados)
        else:
            texto = f"{cantidad} profesores seleccionados"
        
        if dpg.does_item_exist("profesores_seleccionados"):
            dpg.set_value("profesores_seleccionados", texto)
    
    def exportar_seleccionados(self):
        """Exporta los profesores seleccionados."""
        ids_seleccionados = self.obtener_ids_seleccionados()
        print(f"Exportando {len(ids_seleccionados)} profesores:")
        for id_profesor in ids_seleccionados:
            # Buscar el nombre del profesor por su id
            for profesor in self.profesores:
                if profesor["id"] == id_profesor:
                    print(f"ID: {id_profesor}, Nombre: {profesor['nombre']}")
                    break
    
    def obtener_ids_seleccionados(self):
        """Obtiene la lista de IDs de profesores seleccionados."""
        return [id_profesor for id_profesor, seleccionado in self.seleccion_profesores.items() if seleccionado]
    
    def mostrar_ids_seleccionados(self):
        """Muestra solo los IDs de los profesores seleccionados."""
        ids_seleccionados = self.obtener_ids_seleccionados()
        cantidad = len(ids_seleccionados)
        
        if cantidad == 0:
            texto = "Ningún ID seleccionado"
        elif cantidad <= 10:
            texto = ", ".join(ids_seleccionados)
        else:
            texto = f"{cantidad} IDs seleccionados: {', '.join(ids_seleccionados[:5])}..."
        
        if dpg.does_item_exist("ids_seleccionados"):
            dpg.set_value("ids_seleccionados", texto)



## Ejecución
#if __name__ == "__main__":
#    app = ListaProfesoresApp()
#    app.run()
#