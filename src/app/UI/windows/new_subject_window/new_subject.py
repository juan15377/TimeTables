import dearpygui.dearpygui as dpg
from .list_groups import CreateSubjectGroupsSelector
from src.app.database import database_manager

from src.app.UI.components.items_groups_manager import get_id
from src.app.UI.components.windows_manager import Window

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
        
        super().__init__(
            window_tag="new_subject_window",
            label = "Nueva Materia",
            on_close= lambda s, a, u : print(10),
            height=550,
            width=990,
            no_resize=True
        ) 
        
        self.create()
        
    def _create_content(self):
        
        dpg.add_text("Registrar Nueva Materia", color=(255, 255, 0))
        dpg.add_separator()
        with dpg.group():
            with dpg.group(horizontal=True):
                dpg.add_input_text(label="Código", tag=self.input_code_tag, width=120)
                dpg.add_input_text(label="Nombre", tag=self.input_name_tag, width=400)
                
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
                            tag="modal_create_filtro_profesores",
                            width=300,
                            callback=lambda s, a, u: print(10)
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
                            tag="modal_create_filtro_aulas",
                            width=300,
                            callback=lambda s, a, u: print(10)
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
            dpg.add_text("Administración de Grupos", color=[255, 255, 0])
            self.create_subject_list_groups.setup_ui()
            dpg.add_button(label="Guardar Materia", callback=lambda: self.register_new_subject())


        
        
        

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
        
        
        # ? Filtro que se debe hacer para saber si los argumentos son validos 
        
        self.db.subjects.new(
        name,
        code,
        professor_id,
        classroom_id,
        group_ids,
        min_slots,
        max_slots,
        total_slots,
        mode_space
        )
        
        
        
        
        pass 
    def toggle_aula_selector(self, value):
        if value == "Online":
            dpg.disable_item("modal_create_combo_aulas")
            dpg.disable_item("modal_create_filtro_aulas")
        else:
            dpg.enable_item("modal_create_combo_aulas")
            dpg.enable_item("modal_create_filtro_aulas")

    def save_subject(self):
        codigo = dpg.get_value("input_codigo")
        nombre = dpg.get_value("input_nombre")

        if not codigo or not nombre:
            dpg.set_value("status", "Error: Todos los campos son obligatorios")
            return

        dpg.set_value("status", f"Materia guardada: {codigo} - {nombre}")
        dpg.set_value("input_codigo", "")
        dpg.set_value("input_nombre", "")
