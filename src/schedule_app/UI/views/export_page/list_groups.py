import dearpygui.dearpygui as dpg
import random
from typing import List, Dict, Tuple, Optional

class ListaGruposApp:
    def __init__(self):
        dpg.create_context()
        
        self.grupos = []  # Lista de todos los grupos
        self.seleccion_grupos = {}  # Estado de selección de cada grupo
        self.grupos_con_indice = []  # Grupos con su índice original
        
        # Filtros
        self.carreras = []  # Lista de carreras únicas
        self.semestres = []  # Lista de semestres únicos
        self.subgrupos = []  # Lista de subgrupos únicos
        
        self.carrera_seleccionada = None
        self.semestre_seleccionado = None
        self.subgrupo_seleccionado = None
        
        self._inicializar_datos()
        #self.setup_ui()
        

    
    def _inicializar_datos(self):
        """Inicializa la lista de grupos y estructuras auxiliares."""
        # Datos de ejemplo para crear grupos
        carreras = ["Ingeniería", "Medicina", "Derecho", "Economía", "Arquitectura"]
        semestres = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        subgrupos = ["A", "B", "C", "D"]
        
        # Generar algunos grupos de ejemplo
        for carrera in carreras:
            for semestre in semestres:
                for subgrupo in subgrupos:
                    # No todos tienen todos los subgrupos (para hacerlo más realista)
                    if random.random() > 0.3:  
                        nombre_grupo = f"{carrera}-{semestre}-{subgrupo}"
                        self.grupos.append({
                            "carrera": carrera,
                            "semestre": semestre,
                            "subgrupo": subgrupo,
                            "nombre": nombre_grupo
                        })
        
        # Estructuras para gestión eficiente
        self.seleccion_grupos = {grupo["nombre"]: False for grupo in self.grupos}
        self.grupos_con_indice = [(grupo, i) for i, grupo in enumerate(self.grupos)]
        
        # Extraer listas únicas para los filtros
        self.carreras = sorted(list(set(grupo["carrera"] for grupo in self.grupos)))
        self.semestres = sorted(list(set(grupo["semestre"] for grupo in self.grupos)))
        self.subgrupos = sorted(list(set(grupo["subgrupo"] for grupo in self.grupos)))
    
    def setup_ui(self):
        """Configura la interfaz gráfica."""
        with dpg.group():
            # Filtros
            with dpg.group(horizontal=True):
                # Filtro de carrera
                dpg.add_text("Carrera:")
                dpg.add_combo(
                    items=["Todas"] + self.carreras,
                    default_value="Todas",
                    width=150,
                    callback=self.actualizar_filtro_carrera,
                    tag="filtro_carrera"
                )
                
                dpg.add_spacer(width=10)
                
                # Filtro de semestre
                dpg.add_text("Semestre:")
                dpg.add_combo(
                    items=["Todos"] + self.semestres,
                    default_value="Todos",
                    width=100,
                    callback=self.actualizar_filtro_semestre,
                    tag="filtro_semestre"
                )
                
                dpg.add_spacer(width=10)
                
                # Filtro de subgrupo
                dpg.add_text("Subgrupo:")
                dpg.add_combo(
                    items=["Todos"] + self.subgrupos,
                    default_value="Todos",
                    width=100,
                    callback=self.actualizar_filtro_subgrupo,
                    tag="filtro_subgrupo"
                )
            
            dpg.add_spacer(height=5)
            
            # Área de búsqueda por nombre
            with dpg.group(horizontal=True):
                dpg.add_text("Buscar:")
                dpg.add_input_text(
                    tag="busqueda_grupos", 
                    width=300, 
                    callback=self.aplicar_filtros
                )
            
            dpg.add_spacer(height=10)
            
            # Botones de selección
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Seleccionar Todos", 
                    callback=self.seleccionar_todos, 
                    width=150
                )
                dpg.add_button(
                    label="Deseleccionar Todos", 
                    callback=self.deseleccionar_todos, 
                    width=150
                )
                dpg.add_button(
                    label="Exportar Seleccionados", 
                    callback=self.exportar_seleccionados, 
                    width=150
                )
            
            dpg.add_spacer(height=10)
            
            # Lista de grupos
            with dpg.child_window(width=600, height=200, tag="lista_grupos"):
                pass  # Se llena dinámicamente
            
            dpg.add_spacer(height=10)
            
            # Botón y área de selección
            dpg.add_button(
                label="Mostrar Grupos Seleccionados", 
                callback=self.mostrar_seleccionados
            )
            dpg.add_text("Grupos seleccionados:", bullet=True)
            dpg.add_text(
                "Ningún grupo seleccionado", 
                tag="grupos_seleccionados", 
                wrap=700
            )
        
        # Inicializar lista
        self.aplicar_filtros(None, None)
    

    def actualizar_filtro_carrera(self, sender, app_data):
        """Actualiza el filtro de carrera y refresca la lista."""
        self.carrera_seleccionada = None if app_data == "Todas" else app_data
        self.aplicar_filtros(None, None)
    
    def actualizar_filtro_semestre(self, sender, app_data):
        """Actualiza el filtro de semestre y refresca la lista."""
        self.semestre_seleccionado = None if app_data == "Todos" else app_data
        self.aplicar_filtros(None, None)
    
    def actualizar_filtro_subgrupo(self, sender, app_data):
        """Actualiza el filtro de subgrupo y refresca la lista."""
        self.subgrupo_seleccionado = None if app_data == "Todos" else app_data
        self.aplicar_filtros(None, None)
    
    def aplicar_filtros(self, sender, app_data):
        """Aplica todos los filtros y la búsqueda por texto."""
        # Filtrado por carrera, semestre y subgrupo
        grupos_filtrados = []
        
        for grupo, idx in self.grupos_con_indice:
            # Aplicar filtros de carrera, semestre y subgrupo
            if (self.carrera_seleccionada is None or grupo["carrera"] == self.carrera_seleccionada) and \
               (self.semestre_seleccionado is None or grupo["semestre"] == self.semestre_seleccionado) and \
               (self.subgrupo_seleccionado is None or grupo["subgrupo"] == self.subgrupo_seleccionado):
                grupos_filtrados.append((grupo, idx))
        
        # Filtrado por texto de búsqueda
        termino = dpg.get_value("busqueda_grupos").lower() if dpg.does_item_exist("busqueda_grupos") else ""
        
        if not termino:
            grupos_ordenados = grupos_filtrados
        else:
            def calcular_puntuacion(item):
                grupo, idx = item
                nombre_lower = grupo["nombre"].lower()
                
                if nombre_lower.startswith(termino):
                    return (3, idx)
                elif termino in nombre_lower:
                    return (2, idx)
                elif any(p in nombre_lower for p in termino.split()):
                    return (1, idx)
                return (0, idx)
            
            grupos_ordenados = sorted(
                grupos_filtrados,
                key=calcular_puntuacion,
                reverse=True
            )
        
        self._actualizar_lista_ui(grupos_ordenados)
    def _actualizar_lista_ui(self, items_ordenados: List[Tuple[dict, int]]):
        """Actualiza la UI con la lista ordenada de grupos usando tablas."""
        if dpg.does_item_exist("lista_grupos"):
            dpg.delete_item("lista_grupos", children_only=True)
            
            # Crear tabla
            with dpg.table(header_row=True, policy=dpg.mvTable_SizingFixedFit, 
                        borders_innerH=True, borders_outerH=True, borders_innerV=True,
                        borders_outerV=True, parent="lista_grupos"):
                
                # Definir columnas
                dpg.add_table_column(label="")  # Para checkbox
                dpg.add_table_column(label="Carrera")
                dpg.add_table_column(label="Semestre")
                dpg.add_table_column(label="Subgrupo")
                dpg.add_table_column(label="Nombre Completo")
                
                # Mostrar datos
                items_mostrados = items_ordenados[:100]
                for grupo, _ in items_mostrados:
                    with dpg.table_row():
                        dpg.add_checkbox(
                            default_value=self.seleccion_grupos[grupo["nombre"]],
                            callback=lambda s, a, u: self._actualizar_seleccion(u),
                            user_data=grupo["nombre"]
                        )
                        dpg.add_text(grupo["carrera"])
                        dpg.add_text(grupo["semestre"])
                        dpg.add_text(grupo["subgrupo"])
                        dpg.add_text(grupo["nombre"])
            
            if len(items_ordenados) > 100:
                dpg.add_text(
                    f"Mostrando 100 de {len(items_ordenados)} grupos...",
                    parent="lista_grupos"
                )
    def _actualizar_seleccion(self, nombre_grupo: str):
        """Cambia el estado de selección de un grupo."""
        self.seleccion_grupos[nombre_grupo] = not self.seleccion_grupos[nombre_grupo]
    
    def seleccionar_todos(self):
        """Marca todos los grupos visibles como seleccionados."""
        # Aplicar filtros actuales para obtener grupos visibles
        self.aplicar_filtros(None, None)
        for grupo in self.grupos:
            self.seleccion_grupos[grupo["nombre"]] = True
        self.aplicar_filtros(None, None)  # Actualizar UI
    
    def deseleccionar_todos(self):
        """Desmarca todos los grupos."""
        for grupo in self.grupos:
            self.seleccion_grupos[grupo["nombre"]] = False
        self.aplicar_filtros(None, None)  # Actualizar UI
    
    def mostrar_seleccionados(self):
        """Muestra los grupos seleccionados."""
        seleccionados = [nombre for nombre, sel in self.seleccion_grupos.items() if sel]
        cantidad = len(seleccionados)
        
        if cantidad == 0:
            texto = "Ningún grupo seleccionado"
        elif cantidad <= 10:
            texto = ", ".join(seleccionados)
        else:
            texto = f"{cantidad} grupos seleccionados"
        
        if dpg.does_item_exist("grupos_seleccionados"):
            dpg.set_value("grupos_seleccionados", texto)
    
    def exportar_seleccionados(self):
        """Función para exportar los grupos seleccionados."""
        seleccionados = [nombre for nombre, sel in self.seleccion_grupos.items() if sel]
        cantidad = len(seleccionados)
        
        if cantidad == 0:
            print("No hay grupos seleccionados para exportar")
        else:
            print(f"Exportando {cantidad} grupos seleccionados")
            # Aquí podrías implementar la lógica de exportación real
            # Por ejemplo, guardar a CSV, Excel, etc.
            for nombre in seleccionados:
                print(f"- {nombre}")

