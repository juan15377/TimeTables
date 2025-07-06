import dearpygui.dearpygui as dpg
from .list_groups import CreateSubjectGroupsSelector
from src.app.database import database_manager

from src.app.UI.components.items_groups_manager import get_id
from src.app.UI.components.windows_manager import Window, windows_manager
from src.app.UI.windows_tags import NEW_SUBJECT_WINDOW_TAG, SUBJECTS_MANAGER_WINDOW_TAG


import re
import unicodedata

def normalizar(palabra):
    # Quita acentos y convierte a ASCII
    return ''.join(
        c for c in unicodedata.normalize('NFD', palabra)
        if unicodedata.category(c) != 'Mn'
    )

def generar_codigo_materia(nombre_materia):
    palabras_omitidas = {"de", "la", "el", "y", "en", "del", "los", "las", "por", "para", "a", "al"}

    # Tokenizar y normalizar palabras
    palabras = re.findall(r'\w+', nombre_materia.lower())
    palabras = [normalizar(p) for p in palabras]

    # Extraer número final si existe
    sufijo = '0'
    if palabras and palabras[-1].isdigit():
        sufijo = palabras.pop()

    # Filtrar palabras útiles
    significativas = [p for p in palabras if p not in palabras_omitidas]

    # Construir código de 4 letras
    codigo = ''
    for palabra in significativas:
        if len(codigo) < 4:
            codigo += palabra[0].upper()

    # Si faltan letras, seguir tomando más letras de las mismas palabras
    if len(codigo) < 4:
        for palabra in significativas:
            for letra in palabra[1:]:
                if len(codigo) < 4:
                    codigo += letra.upper()
                else:
                    break

    # Rellenar si aún faltan letras
    codigo = (codigo + 'XXXX')[:4]

    return codigo + sufijo


class SubjectRegistrationWindow(Window):
    
    __reference = None
    
    def __new__(cls, *args, **kwargs):
        if cls.__reference is None:
            cls.__reference = super().__new__(cls)
            return cls.__reference 
        else:
            return cls.__reference 
    
    
    def __init__(self, db):
        
        self.db = db 
        
        cursor = self.db.execute_query("""
            SELECT ID, NAME
            FROM PROFESSOR            
        """)
        
        
        self.profesores = [
            F"{name} (id = {id})" for (id, name) in cursor
        ]
        cursor.close()
        
        cursor = self.db.execute_query("""
            SELECT ID, NAME
            FROM CLASSROOM           
        """)
        
        self.aulas = [
            F"{name} (id = {id})" for (id, name) in cursor
        ]
        cursor.close()
        

        self.create_subject_list_groups = CreateSubjectGroupsSelector(
            database_manager,
            lambda s, a, u: print("cambio"),
            1
        )
        
        self.input_name_tag = "input_name_subject"
        self.input_code_tag = "input_code_subject"
        self.modal_create_subject_classroom_tag = "modal_create_combo_aulas" 
        self.modal_create_subject_professor_tag = "modal_create_combo_profesores"
        self.input_min_slots_tag = "modal_create_min_slots"
        self.input_max_slots_tag = "modal_create_max_slots"
        self.input_total_slots_tag = "modal_create_total_slots"
        self.modal_create_mode_space = "modal_create_mode_space" # ! online or presencial
        
        #! filters 
        
        self.input_filter_professor = "modal_create_new_subject_filter_professors"
        self.input_filter_classroom = "modal_create_new_subject_filter_classroom"
        
        super().__init__(
            window_tag="new_subject_window",
            label = "Nueva Materia",
            on_close= lambda s, a, u : print(10),
            height=560,
            width=990,
            no_resize=True
        ) 
        
        self.create()
    
    def show(self):
        
        self.update()
        
        super().show()
        
        pass 
    
    
    def update_items(self):
        
        
        cursor = self.db.execute_query("""
            SELECT ID, NAME
            FROM PROFESSOR            
        """)
        
        
        self.profesores = [
            F"{name} (id = {id})" for (id, name) in cursor
        ]
        cursor.close()
        
        cursor = self.db.execute_query("""
            SELECT ID, NAME
            FROM CLASSROOM           
        """)
        
        self.aulas = [
            F"{name} (id = {id})" for (id, name) in cursor
        ]
        cursor.close()
        
        self.create_subject_list_groups.update()
        
        
        pass 
        
        
    def update_combos(self):
        
        dpg.configure_item(self.modal_create_subject_professor_tag, items = self.profesores)
        dpg.configure_item(self.modal_create_subject_classroom_tag, items = self.aulas)
    
    def update(self):
        
        self.update_items()
        self.update_combos()
        
        
    def _create_content(self):
        
        
        def generate_tag():
            name = dpg.get_value(self.input_name_tag)
            generate_code = generar_codigo_materia(name)
            dpg.set_value(self.input_code_tag, generate_code)

        dpg.add_separator()
        with dpg.group():
            with dpg.group(horizontal=True):
                dpg.add_input_text(label="Código", tag=self.input_code_tag, width=120)
                dpg.add_input_text(label="Nombre", tag=self.input_name_tag, width=400)
                
                dpg.add_button(label ="generar_codigo", tag = "generate_tag", callback= lambda s, a, u: generate_tag())
                
            with dpg.group(horizontal=True):
                dpg.add_input_int(label="Mín. Slots", tag=self.input_min_slots_tag, width=120, min_value=1, min_clamped=True, default_value=5)
                dpg.add_input_int(label="Máx. Slots", tag=self.input_max_slots_tag, width=120, min_value=1, min_clamped=True, default_value=30)
                dpg.add_input_int(label="Total Slots", tag=self.input_total_slots_tag, width=120, min_value=1, min_clamped=True, default_value=15)
            with dpg.group(horizontal=True):
                dpg.add_text("Modalidad:")
                dpg.add_radio_button(
                    items=["Presencial", "Online"],
                    tag=self.modal_create_mode_space,
                    default_value="Presencial",
                    horizontal=True,
                    callback=lambda s, a, u: self.toggle_aula_selector(a)
                )
            
                
            with dpg.group(horizontal=True):
                with dpg.group():
                    dpg.add_text("Profesor:")
                    with dpg.group(horizontal=True):
                        dpg.add_input_text(
                            hint="Buscar profesor...",
                            tag=self.input_filter_professor,
                            width=300,
                            callback=self.filter_items
                        )
                        dpg.add_button(
                            label="Buscar",
                            callback=lambda s, a, u: print(11),
                            width=80
                        )
                    dpg.add_combo(
                        items=self.profesores,
                        tag=self.modal_create_subject_professor_tag,
                        width=400
                    )
                with dpg.group():
                    dpg.add_text("Aula:")
                    with dpg.group(horizontal=True):
                        dpg.add_input_text(
                            hint="Buscar aula...",
                            tag=self.input_filter_classroom,
                            width=300,
                            callback=self.filter_items
                        )
                        dpg.add_button(
                            label="Buscar",
                            callback=lambda s, a, u: print(10),
                            width=80
                        )
                    dpg.add_combo(
                        items=self.aulas,
                        tag=self.modal_create_subject_classroom_tag,
                        width=400
                    )
            dpg.add_separator()
            self.create_subject_list_groups.setup_ui()
            dpg.add_button(label="Guardar Materia", callback=lambda: self.register_new_subject())


        
    def filter_items(self, sender, coincidence, user_data):
        """Filtra la lista según el texto ingresado"""
        filter_text = coincidence.lower()
        
        if sender == self.input_filter_professor:
            all_items = self.profesores
            selector_tag = self.modal_create_subject_professor_tag
        else:
            all_items = self.aulas
            selector_tag = self.modal_create_subject_classroom_tag
        
        
        if not filter_text:
            # Si no hay texto de filtro, restaurar la lista completa
            filter_items = all_items
        else:
            # Filtrar por nombre o I
            filter_items = [item for item in all_items if filter_text in item.lower()]
        
        current_selection = dpg.get_value(selector_tag)
        dpg.configure_item(selector_tag, items=filter_items)
        
        # Si la selección actual ya no está en la lista filtrada y hay elementos,
        # establecer el primer elemento como seleccionado
        if current_selection not in filter_items and filter_items:
            dpg.set_value(selector_tag, filter_items[0])
        # Si no hay elementos en la lista filtrada, limpiar la selección
        elif not all_items:
            dpg.set_value(selector_tag, current_selection)
            
        # Update progress bar after selection change
        pass

        

    def register_new_subject(self):
        name = dpg.get_value(self.input_name_tag)
        code = dpg.get_value(self.input_code_tag)
        

        min_slots = dpg.get_value(self.input_min_slots_tag)
        max_slots = dpg.get_value(self.input_max_slots_tag)
        total_slots = dpg.get_value(self.input_total_slots_tag)
        
        professor_id = get_id(dpg.get_value(self.modal_create_subject_professor_tag))
        classroom_id = get_id(dpg.get_value(self.modal_create_subject_classroom_tag))
        
        mode_space = dpg.get_value(self.modal_create_mode_space)
        
        group_ids = self.create_subject_list_groups.get_groups_ids()
        
        
        online = False if mode_space == "Presencial" else True
        
        # ? Filtro que se debe hacer para saber si los argumentos son validos 
        
        
        if professor_id is None:
            windows_manager.notification_system.show_notification("Error: No se ah Seleccionado ningun Profesor", 3, "error")
            return None
        
        if min_slots > max_slots :
            windows_manager.notification_system.show_notification("Error: Max Slots  > Min Slots", 3, "error")
            return None
    
        if group_ids is None or group_ids == []:
            windows_manager.notification_system.show_notification("Error: La lista de grupos esta vacia ", 3, "error")
            return None
            
        self.db.subjects.new(
        name,
        code,
        professor_id,
        classroom_id,
        group_ids,
        min_slots,
        max_slots,
        total_slots,
        online
        )
            
        
        dpg.set_value(self.input_name_tag, "")
        dpg.set_value(self.input_code_tag, "")
        
        windows_manager.notification_system.show_notification("Materia Agregada correctamente", 3, "success")

        windows_manager.get_window(SUBJECTS_MANAGER_WINDOW_TAG).update()
        
        
        pass 
    def toggle_aula_selector(self, value):
        if value == "Online":
            dpg.disable_item(self.modal_create_subject_classroom_tag)
            dpg.disable_item(self.input_filter_classroom)
        else:
            dpg.enable_item(self.modal_create_subject_classroom_tag)
            dpg.enable_item(self.input_filter_classroom)

    def save_subject(self):
        codigo = dpg.get_value("input_codigo")
        nombre = dpg.get_value("input_nombre")

        if not codigo or not nombre:
            dpg.set_value("status", "Error: Todos los campos son obligatorios")
            return

        dpg.set_value("status", f"Materia guardada: {codigo} - {nombre}")
        dpg.set_value("input_codigo", "")
        dpg.set_value("input_nombre", "")
