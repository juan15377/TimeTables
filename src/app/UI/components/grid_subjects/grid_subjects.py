import dearpygui.dearpygui as dpg
import json
from typing import Dict, List, Tuple, Optional, Any
from .themes import create_blue_theme  # Importa la función, no el tema directo
from ..list_subjects.subject_selector import SubjectSelector
from src.app.database import database_manager
class ScheduleGrid:
    """
    Clase principal para gestionar una cuadrícula de horarios con materias personalizables.
    Permite añadir bloques de materias con posición, altura y color específicos.
    El ancho siempre es fijo (1 día).
    """
    
    def __init__(self, db, mode, mode_id):
        # Configuración
        self.width = 900
        self.height = 700
        self.title = 'Planificador de Horarios'
        self.db = db 
        self.mode = mode 
        self.mode_id = mode_id
        
        # Datos
        self.hours = [
            '7:00', '7:30', '8:00', '8:30', '9:00', '9:30', '10:00', '10:30',
            '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
            '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30',
            '19:00', '19:30', '20:00', '20:30', '21:00', '21:30'
        ]
        self.weekdays = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        
        # Dimensiones de celda
        self.cell_width = 120
        self.cell_height = 40
        
        # Sujetos predefinidos con colores
        
        # Bloques actuales (para rastrear las materias colocadas)
        self.blocks = []
        
        # Temas
        self.themes = {}
        
        self.categories = {}
        
        # Modo de edición
        self.edit_mode = "add"  # add, delete, move
        self.selected_block = None
        
        # Inicializar DPG
        
    def display_all_blocks(self):
        
        #extraigo todos los bloques asignados a esta grilla 
        cursor = self.db.db_connection.cursor()
        
        cursor.execute(f"""
            SELECT A.ID_SLOT, A.ID_SUBJECT, A.ROW_POSITION, A.COLUMN_POSITION, A.LEN, 
                B.CODE, C.RED, C.GREEN, C.BLUE
            FROM SUBJECT_SLOTS A
            LEFT JOIN SUBJECT B ON A.ID_SUBJECT = B.ID
            LEFT JOIN {self.mode}_COLORS C ON A.ID_SUBJECT = C.ID_SUBJECT
            WHERE A.ID_SUBJECT IN (
                SELECT ID_SUBJECT FROM {self.mode}_SUBJECT 
                WHERE ID_{self.mode} = {self.mode_id}
            )
        """)
        
        for slot in cursor:
            id_slot = slot[0]
            id_subject = slot[1]
            row_position = slot[2]
            column_position = slot[3]
            len_slot = slot[4]
            code = slot[5]
            red = slot[6]
            green = slot[7]
            blue = slot[8]
            
            self.add_subject_block(column_position-1, row_position-1, 1, len_slot, id_slot, id_subject, code, (red, green, blue), add_in_database = False)
        pass
        
        
    def setup_ui(self):
        global blue_combo_theme
        
        """Configurar la interfaz de usuario"""        
        # Crear temas
        self.create_themes()
        # Ventana principal
            
        dpg.add_separator()

        dpg.add_spacing()
        subject_selector  = SubjectSelector(1, database_manager, lambda e , t, c,: print("Hola"), lambda s , a, u,: self.update_color(u, a), mode = "PROFESSOR")
        self.subject_selector = subject_selector

        with dpg.group(horizontal=False, parent="main_content"):
                
            # Segunda fila de herramientas
            with dpg.group(horizontal=True):
                
                dpg.add_text("Modo:")
                dpg.add_radio_button(items=["Añadir", "Borrar", "Mover"], default_value="Añadir", 
                                        callback=self.set_edit_mode, horizontal=True)
                
                # Usar espaciador en lugar de separador vertical
                dpg.add_spacer(width=10)  
                dpg.add_text("Progresso Materia:")
                
                dpg.add_progress_bar(default_value=.5,
                                    width=100,
                                    overlay=f"{int(.5 * 100)}%")
                    
            subject_selector.setup_ui(parent="main_content") 

                # Solo permitimos configurar la altura
                #slots_selector.setup_widget()
                #self.slots_selector = slots_selector
                
            dpg.add_separator()
            dpg.add_spacing()
            

            #Contenedor de la cuadrícula
                
            with dpg.child_window(tag="grid_container", height=-30, parent="main_content"):
                self.build_grid()
                self.display_all_blocks()
                
                    

        
    def create_themes(self):
        """Crear todos los temas utilizados en la aplicación"""
        # Tema de botón predeterminado
        self.themes["default"] = dpg.add_theme()
        with dpg.theme_component(dpg.mvButton, parent=self.themes["default"]):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (120, 120, 120))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (160, 160, 160))
        
        # Tema para la columna de horas
        self.themes["hours"] = dpg.add_theme()
        with dpg.theme_component(dpg.mvButton, parent=self.themes["hours"]):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (200, 200, 200))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (220, 220, 220))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0))
        
        # Tema para celdas seleccionadas
        self.themes["selected"] = dpg.add_theme()
        with dpg.theme_component(dpg.mvButton, parent=self.themes["selected"]):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 120, 200))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (30, 150, 230))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))

    
    def create_subject_theme(self, color: Tuple[int, int, int]):
        """Crear un tema para una materia con el color especificado"""
        theme = dpg.add_theme()
        with dpg.theme_component(dpg.mvButton, parent=theme):
            # Colores (como ya tienes)
            dpg.add_theme_color(dpg.mvThemeCol_Button, color)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [min(c + 40, 255) for c in color])
            
            # Ajustar color de texto según brillo
            brightness = (0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2])/255
            text_color = (0, 0, 0) if brightness > 0.5 else (255, 255, 255)
            dpg.add_theme_color(dpg.mvThemeCol_Text, text_color)
            
            # Aumentar tamaño de fuente (agrega esto)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5)  # Padding interno
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)     # Bordes redondeados
            
        return theme
    
    def build_grid(self):
        """Construir la cuadrícula del horario"""
        with dpg.group(horizontal=True, parent="grid_container"):
            # Columna de horas
            with dpg.group():
                # Encabezado
                
                dpg.add_button(
                        label="Hora",
                        height=self.cell_height,
                        width = 70,
                        enabled=False,
                    )
                dpg.add_separator()
                
                # Celdas de hora
                for i, hour in enumerate(self.hours):
                    tag_hour = f"hora_{i}"
                    dpg.add_button(
                        label=hour,
                        width=70,
                        height=self.cell_height,
                        enabled=False,
                        tag=tag_hour
                    )
                    dpg.bind_item_theme(tag_hour, self.themes["hours"])
            
            # Columnas para los días
            for day_idx, day_name in enumerate(self.weekdays):
                with dpg.group():
                    # Encabezado
                    tag_day = f"day_{day_name}"
                    dpg.add_button(
                        label=day_name,
                        height=self.cell_height,
                        width = self.cell_width,
                        enabled=False,
                        tag=tag_day
                    )
                    #dpg.add_text(day_name, color=(0, 100, 200))
                    dpg.add_separator()
                    
                    # Celdas para cada día
                    for hour_idx in range(len(self.hours)):
                        cell_id = f"cell_{day_idx}_{hour_idx}"
                        dpg.add_button(
                            label="",
                            width=self.cell_width,
                            height=self.cell_height,
                            tag=cell_id,
                            callback=self.cell_clicked,
                            user_data=(day_idx, hour_idx)
                        )
                        dpg.bind_item_theme(cell_id, self.themes["default"])
    
    def cell_clicked(self, sender: str, app_data: Any, user_data: Tuple[int, int]):
        """
        Manejar el clic en una celda según el modo de edición actual
        """
        day_idx, hour_idx, id_block, id_subject = user_data
        
        
        if self.edit_mode == "add":
            # Ancho fijo siempre a 1
            width = 1
            # Obtener altura del bloque
            height = self.subject_selector.get_subject_slot()
            
                        
            # Verificar si el espacio está disponible
            if self.check_space_available(day_idx, hour_idx, width, height):
                # Obtener información de la materia
                subject_id = self.subject_selector.get_id()
                subject_name = self.subject_selector.get_code()
                color_values = self.subject_selector.get_subject_color()
                
                color = tuple(int(c) for c in color_values[:3])
                new_id_block = self.db.subjects.new_slot(subject_id, hour_idx + 1, day_idx + 1, height)
                if new_id_block == None:
                    return None
                #color = (100, 100, 100)
                
                # Añadir el bloque
                self.add_subject_block(day_idx, hour_idx, width, height, new_id_block, id_subject, subject_name, color)
            else:
                #self.update_status("Error: El espacio seleccionado no está disponible")
                pass
        
        elif self.edit_mode == "delete":
            # Buscar y eliminar bloques en esta posición
            self.delete_blocks_at(day_idx, hour_idx)
            # borrar en la base de datos
            self.db.subjects.remove_slot(id_block)
            self.subject_selector.update_bar_progress()
            self.subject_selector.update_subject_slots()
            
            print(self.categories.keys())
            print(self.categories[id_subject])
            self.categories[id_subject].remove(f"cell_{day_idx}_{hour_idx}")
            print(id_subject)
                    # Primero verificar si la clave existe en el diccionario
            #if id_subject in self.categories:
            #    # Si existe, añadir el elemento al conjunto
            #    self.categories[id_subject].add(f"cell_{day}_{hour}")
            #else:
            #    # Si no existe, crear un nuevo conjunto con ese elemento
            #    self.categories[id_subject] = {f"cell_{day}_{hour}"}        
            
        
        elif self.edit_mode == "move":
            # Seleccionar bloque para mover
            block = self.find_block_at(day_idx, hour_idx)
            if block:
                self.select_block(block)
            elif self.selected_block:
                # Mover el bloque seleccionado a la nueva posición
                # Ancho siempre es 1
                width = 1
                height = self.selected_block["height"]
                
                if self.check_space_available(day_idx, hour_idx, width, height, exclude_block=self.selected_block):
                    # Eliminar el bloque anterior
                    self.clear_block(self.selected_block)
                    
                    # Crear el nuevo bloque en la nueva posición
                    self.add_subject_block(
                        day_idx, hour_idx, width, height,
                        self.selected_block["subject"],
                        self.selected_block["color"],
                        self.selected_block.get("details", {})
                    )
                    self.selected_block = None
                    self.update_status("Bloque movido")
                else:
                    self.update_status("Error: No se puede mover a esa posición")
    
    def add_subject_block(self, day: int, hour: int, width: int, height: int, id_block : int, id_subject : int,
                        subject: str, color: Tuple[int, int, int], details: Dict = None, add_in_database = True):
        """
        Añadir un bloque de materia en la posición, tamaño y color especificados
        
        Args:
            day: Índice del día (0=Lunes, 6=Domingo)
            hour: Índice de la hora (0=7:00, 1=7:30, etc.)
            width: Ancho del bloque en número de días (siempre 1)
            height: Alto del bloque en número de slots de tiempo
            subject: Nombre de la materia
            color: Color en formato RGB (r, g, b)
            details: Detalles adicionales de la materia (profesor, notas, etc.)
        """
        # Asegurar que el ancho siempre sea 1
        if height == 0:
            return None
        
        width = 1
        
        if details is None:
            details = {}
            
        # Crear un nuevo tema para este bloque si no existe
        theme_key = f"subject_{id_subject}"
        self.themes[theme_key] = self.create_subject_theme(color)
        
        # Crear el bloque
        block = {
            "id_subject" : id_subject,
            "id" : id_block,
            "day": day,
            "hour": hour,
            "width": width,
            "height": height,
            "subject": subject,
            "color": color,
            "theme": theme_key,
            "details": details
        }
        

        # Guardar el bloque en la lista
        self.blocks.append(block)
        
        # Renderizar el bloque en la UI
        self.render_block(block)
        
        # Primero verificar si la clave existe en el diccionario
        print("EL ID_SUBJECT INSERCCION ", id_subject)
        if id_subject in self.categories.keys():
            # Si existe, añadir el elemento al conjunto
            self.categories[id_subject].add(f"cell_{day}_{hour}")
            f"Se anadio el bloque {id_block} en la materia {id_subject}"
        else:
            # Si no existe, crear un nuevo conjunto con ese elemento
            self.categories[id_subject] = {f"cell_{day}_{hour}"}        
        
        # guarda el cambio en la base de datos  
        self.subject_selector.update_subject_slots()
        self.subject_selector.update_bar_progress()
        
        #self.themes["default"] = dpg.add_theme()

    def render_block(self, block: Dict):
        """Renderizar un bloque de materia en la UI"""
        day, hour = block["day"], block["hour"]
        width, height = block["width"], block["height"]
        subject = block["subject"]
        theme_key = block["theme"]
        id_block = block["id"]
        id_subject= block["id_subject"]
        
        # Si el bloque abarca múltiples celdas, ocultar las celdas individuales
        # excepto la primera, que se redimensionará
        main_cell_id = f"cell_{day}_{hour}"
        
        # Calcular el tamaño total (ancho siempre es el ancho de una celda)
        total_width = self.cell_width
        total_height = self.cell_height * height +  (height -1)*6
        
        # Redimensionar la celda principal
        dpg.configure_item(main_cell_id, 
                          width=total_width,
                          height=total_height,
                          label=subject,
                          user_data = (day, hour, id_block, id_subject),
                          callback = self.cell_clicked)
        
        # Aplicar tema
        dpg.bind_item_theme(main_cell_id, self.themes[theme_key])
        
        # Ocultar las demás celdas que están dentro del bloque (solo verticalmente)
        for h in range(hour, hour + height):
            if h == hour:
                continue  # Saltar la celda principal
            
            if h < len(self.hours):
                cell_id = f"cell_{day}_{h}"
                if dpg.does_item_exist(cell_id):
                    dpg.configure_item(cell_id, show=False)
    
    def clear_block(self, block: Dict):
        """Eliminar un bloque de la UI y mostrar de nuevo las celdas individuales"""
        day, hour = block["day"], block["hour"]
        width, height = block["width"], block["height"]
        
        # Restaurar la celda principal
        main_cell_id = f"cell_{day}_{hour}"
        dpg.configure_item(main_cell_id, 
                          width=self.cell_width,
                          height=self.cell_height,
                          label="")
        self.create_themes()
        dpg.bind_item_theme(main_cell_id, self.themes["default"])
        
        # Mostrar de nuevo las demás celdas (solo verticalmente)
        for h in range(hour, hour + height):
            if h == hour:
                continue  # Saltar la celda principal
            
            if h < len(self.hours):
                cell_id = f"cell_{day}_{h}"
                if dpg.does_item_exist(cell_id):
                    dpg.configure_item(cell_id, show=True)
                    #dpg.bind_item_theme(cell_id, self.themes["default"])

    
    def check_space_available(self, day: int, hour: int, width: int, height: int, 
                             exclude_block: Dict = None) -> bool:
        """
        Verificar si el espacio está disponible para añadir un bloque
        
        Args:
            day: Índice del día inicial
            hour: Índice de la hora inicial
            width: Ancho del bloque en días (siempre 1)
            height: Alto del bloque en horas
            exclude_block: Bloque que se debe excluir de la verificación (para mover)
            
        Returns:
            bool: True si el espacio está disponible, False en caso contrario
        """
        # Asegurar que el ancho siempre sea 1
        width = 1
        
        # Verificar límites de la cuadrícula
        if day + width > len(self.weekdays) or hour + height > len(self.hours):
            return False
        
        # Verificar si hay bloques existentes en el espacio
        for h in range(hour, hour + height):
            # Buscar si hay un bloque que cubra esta celda
            for block in self.blocks:
                # Saltar el bloque excluido
                if exclude_block and block == exclude_block:
                    continue
                
                # Verificar si esta celda está dentro del bloque
                block_day, block_hour = block["day"], block["hour"]
                block_width, block_height = block["width"], block["height"]
                
                if (block_day == day and 
                    block_hour <= h < block_hour + block_height):
                    return False
        
        return True
    
    def find_block_at(self, day: int, hour: int) -> Optional[Dict]:
        """Encontrar un bloque en la posición dada"""
        for block in self.blocks:
            block_day, block_hour = block["day"], block["hour"]
            block_height = block["height"]
            
            if (block_day == day and 
                block_hour <= hour < block_hour + block_height):
                return block
        
        return None
    
    def delete_blocks_at(self, day: int, hour: int):
        """Eliminar bloques en la posición dada"""
        block = self.find_block_at(day, hour)
        if block:
            self.clear_block(block)
            self.blocks.remove(block)
            self.update_status(f"Eliminada materia {block['subject']}")
            
    
    def select_block(self, block: Dict):
        """Seleccionar un bloque para moverlo"""
        self.selected_block = block
        
        # Cambiar temporalmente el tema para mostrar que está seleccionado
        main_cell_id = f"cell_{block['day']}_{block['hour']}"
        dpg.bind_item_theme(main_cell_id, self.themes["selected"])
        
        self.update_status(f"Seleccionado bloque {block['subject']} para mover")
    
    def clear_all_blocks(self):
        """Eliminar todos los bloques"""
        for block in self.blocks[:]:  # Crear una copia para iterar
            self.clear_block(block)
        
        self.blocks = []
        self.update_status("Todos los bloques eliminados")
    
    def update_color_preview(self, sender, app_data):
        """Actualizar la vista previa del color"""
        color = app_data[:3]  # RGB sin el canal alpha
        
        # Actualizar el tema del botón de vista previa
        with dpg.theme() as preview_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, color)
        
        #dpg.bind_item_theme("color_preview", preview_theme)
    
    def set_edit_mode(self, sender, app_data):
        """Cambiar el modo de edición"""
        if app_data == "Añadir":
            self.edit_mode = "add"
        elif app_data == "Borrar":
            self.edit_mode = "delete"
        elif app_data == "Mover":
            self.edit_mode = "move"
        
        # Limpiar selección al cambiar de modo
        if self.selected_block:
            main_cell_id = f"cell_{self.selected_block['day']}_{self.selected_block['hour']}"
            theme_key = self.selected_block["theme"]
            dpg.bind_item_theme(main_cell_id, self.themes[theme_key])
            self.selected_block = None
        
        self.update_status(f"Modo cambiado a: {app_data}")
    
    def save_block_details(self):
        """Guardar los detalles editados de un bloque"""
        if self.selected_block:
            # Obtener valores del formulario
            name = dpg.get_value("edit_subject_name")
            professor = dpg.get_value("edit_professor")
            notes = dpg.get_value("edit_notes")
            
            # Actualizar detalles del bloque
            self.selected_block["details"] = {
                "professor": professor,
                "notes": notes
            }
            
            # Actualizar nombre de la materia si fue cambiado
            if name and name != self.selected_block["subject"]:
                self.selected_block["subject"] = name
                main_cell_id = f"cell_{self.selected_block['day']}_{self.selected_block['hour']}"
                dpg.set_item_label(main_cell_id, name)
            
            # Cerrar ventana de edición
            dpg.configure_item("edit_window", show=False)
            self.update_status("Detalles guardados")
    
    
    def update_status(self, message: str):
        """Actualizar el mensaje de la barra de estado"""
        #dpg.set_value("status_text", message) 

    def update_color(self, id_subject, new_color):
        #! New color is in format (red, green, blue, transparency)
        #! where between 0 an 1 
        red = new_color[0]
        green = new_color[1]
        blue = new_color[2]
        
        print(new_color)
        theme = self.create_subject_theme((red*255, green*255, blue*255)) # ! Format In range (0,255)
        
        print("ID SUBJECT A CAMBIAR", id_subject)
        for cell_tag in self.categories[id_subject]:
            dpg.bind_item_theme(cell_tag, theme)


    def set_id_mode(self, id_mode):
        self.mode_id = id_mode
        self.clear_all_blocks()
        self.subject_selector.set_id_mode(id_mode)
        self.categories = {}
        self.display_all_blocks()
        print("cambio de id")
        pass
    
    def set_mode(self, new_mode, mode_id):
        self.mode = new_mode
        self.set_id_mode(mode_id)
        pass