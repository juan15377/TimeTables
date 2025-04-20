import dearpygui.dearpygui as dpg
import random
from typing import List, Dict, Tuple

class ListaAulasApp:
    def __init__(self):
        self.aulas: List[str] = []
        self.seleccion_aulas: Dict[str, bool] = {}
        self.aulas_con_indice: List[Tuple[str, int]] = []
        self._inicializar_datos()
        self.setup_ui()

    def _inicializar_datos(self):
        """Inicializa la lista de aulas y estructuras auxiliares."""
        # Ejemplo inicial de aulas
        self.aulas = [
            "Aula 101 - Matemáticas",
            "Aula 202 - Física",
            "Aula 103 - Química",
            "Aula 305 - Biología",
            "Aula 104 - Informática",
            "Laboratorio 1 - Ciencias",
            "Laboratorio 2 - Tecnología",
            "Aula 203 - Historia",
            "Aula 301 - Literatura",
            "Aula 102 - Idiomas",
        ]
        # Generar datos aleatorios para pruebas
        tipos_aula = ["Aula", "Laboratorio", "Taller", "Sala"]
        materias = ["Matemáticas", "Física", "Química", "Biología", "Informática",
                   "Historia", "Literatura", "Idiomas", "Arte", "Música"]
        for _ in range(100):
            tipo = random.choice(tipos_aula)
            numero = random.randint(100, 399)
            materia = random.choice(materias)
            self.aulas.append(f"{tipo} {numero} - {materia}")
        
        # Estructuras para gestión eficiente
        self.seleccion_aulas = {aula: False for aula in self.aulas}
        self.aulas_con_indice = [(aula, i) for i, aula in enumerate(self.aulas)]

    def setup_ui(self):
        """Configura la interfaz gráfica."""
        with dpg.group():
            # Área de búsqueda
            with dpg.group(horizontal=True):
                dpg.add_text("Buscar:")
                dpg.add_input_text(
                    tag="busqueda_aulas",
                    width=300,
                    callback=lambda s, a: self.ordenar_por_coincidencia(s, a)
                )
            dpg.add_spacer(height=5)
            
            # Botones de selección
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Seleccionar Todas",
                    callback=lambda: self.seleccionar_todas(),
                    width=150
                )
                dpg.add_button(
                    label="Deseleccionar Todas",
                    callback=lambda: self.deseleccionar_todas(),
                    width=150
                )
                dpg.add_button(
                    label="Exportar",
                    callback=lambda e, a, u: print("HOLA"),
                    width=150
                )
            dpg.add_spacer(height=10)
            
            # Tabla de aulas
            with dpg.child_window(width=550, height=300, tag="tabla_container_classroom"):
                # Crear tabla
                with dpg.table(tag="tabla_aulas", header_row=True, borders_innerH=True, 
                              borders_outerH=True, borders_innerV=True, borders_outerV=True,
                              resizable=True, policy=dpg.mvTable_SizingStretchProp):
                    
                    # Definir columnas
                    dpg.add_table_column(label="Selección", width_fixed=True, init_width_or_weight=60)
                    dpg.add_table_column(label="ID")
                    dpg.add_table_column(label="Nombre")
            
            dpg.add_spacer(height=10)
            
            # Botón y área de selección
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Mostrar Aulas Seleccionadas",
                    callback=lambda: self.mostrar_seleccionadas()
                )
                dpg.add_button(
                    label="Mostrar IDs Seleccionados",
                    callback=lambda: self.mostrar_ids_seleccionados()
                )
            
            dpg.add_text("Aulas seleccionadas:", bullet=True)
            dpg.add_text(
                "Ningún aula seleccionada",
                tag="aulas_seleccionadas",
                wrap=500
            )
            
            dpg.add_text("IDs seleccionados:", bullet=True)
            dpg.add_text(
                "Ningún ID seleccionado",
                tag="ids_seleccionados_aulas",
                wrap=500
            )
            
        # Inicializar tabla
        self.ordenar_por_coincidencia(None, None)

    def run(self):
        """Ejecuta la aplicación."""
        pass

    def ordenar_por_coincidencia(self, sender, app_data):
        """Ordena aulas según coincidencia con el término de búsqueda."""
        termino = dpg.get_value("busqueda_aulas").lower() if dpg.does_item_exist("busqueda_aulas") else ""
        
        if not termino:
            aulas_ordenadas = self.aulas_con_indice.copy()
        else:
            def calcular_puntuacion(item):
                aula, idx = item
                aula_lower = aula.lower()
                if aula_lower.startswith(termino):
                    return (3, idx)
                elif termino in aula_lower:
                    return (2, idx)
                elif any(p in aula_lower for p in termino.split()):
                    return (1, idx)
                return (0, idx)
            
            aulas_ordenadas = sorted(
                self.aulas_con_indice,
                key=calcular_puntuacion,
                reverse=True
            )
        
        self._actualizar_tabla_ui(aulas_ordenadas)

    def _actualizar_tabla_ui(self, items_ordenados: List[Tuple[str, int]]):
        """Actualiza la UI con la tabla ordenada de aulas."""
        # Limpiar tabla existente
        if dpg.does_item_exist("tabla_aulas"):
            dpg.delete_item("tabla_aulas", children_only=True, slot=1)  # Borra solo las filas, no las columnas
        
        # Mostrar las primeras 100 aulas
        items_mostrados = items_ordenados[:100]
        
        # Añadir filas a la tabla
        for aula, idx in items_mostrados:
            with dpg.table_row(parent="tabla_aulas"):
                # Columna de selección
                dpg.add_checkbox(
                    default_value=self.seleccion_aulas[aula],
                    callback=lambda s, a, u: self._actualizar_seleccion(u),
                    user_data=aula
                )
                # Columna ID
                dpg.add_text(f"{idx}")
                # Columna Nombre
                dpg.add_text(aula)
        
        # Mostrar mensaje si hay más de 100 aulas
        if len(items_ordenados) > 100:
            with dpg.table_row(parent="tabla_aulas"):
                dpg.add_text("")
                dpg.add_text("")
                dpg.add_text(f"Mostrando 100 de {len(items_ordenados)} aulas...")

    def _actualizar_seleccion(self, aula: str):
        """Cambia el estado de selección de un aula."""
        self.seleccion_aulas[aula] = not self.seleccion_aulas[aula]

    def seleccionar_todas(self):
        """Marca todas las aulas como seleccionadas."""
        for aula in self.aulas:
            self.seleccion_aulas[aula] = True
        self.ordenar_por_coincidencia(None, None)

    def deseleccionar_todas(self):
        """Desmarca todas las aulas."""
        for aula in self.aulas:
            self.seleccion_aulas[aula] = False
        self.ordenar_por_coincidencia(None, None)

    def mostrar_seleccionadas(self):
        """Muestra las aulas seleccionadas."""
        seleccionadas = [a for a, sel in self.seleccion_aulas.items() if sel]
        cantidad = len(seleccionadas)
        
        if cantidad == 0:
            texto = "Ningún aula seleccionada"
        elif cantidad <= 10:
            texto = ", ".join(seleccionadas)
        else:
            texto = f"{cantidad} aulas seleccionadas"
        
        dpg.set_value("aulas_seleccionadas", texto)
    
    def obtener_ids_seleccionados(self):
        """Obtiene los IDs de las aulas seleccionadas."""
        ids_seleccionados = []
        for aula, idx in self.aulas_con_indice:
            if self.seleccion_aulas.get(aula, False):
                ids_seleccionados.append(idx)
        return ids_seleccionados
    
    def mostrar_ids_seleccionados(self):
        """Muestra los IDs de las aulas seleccionadas en la UI."""
        ids = self.obtener_ids_seleccionados()
        cantidad = len(ids)
        
        if cantidad == 0:
            texto = "Ningún ID seleccionado"
        elif cantidad <= 20:
            texto = ", ".join(map(str, ids))
        else:
            texto = f"{cantidad} IDs seleccionados: {', '.join(map(str, ids[:10]))}... (y {cantidad-10} más)"
        
        dpg.set_value("ids_seleccionados", texto)

# Para iniciar la aplicación
