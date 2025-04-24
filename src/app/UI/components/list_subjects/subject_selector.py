from src.app.UI.components.color_picker import SubjectColorEditor
import dearpygui.dearpygui as dpg
from src.app.database import database_manager
from src.app.UI.components.slider_slots.slider_slots import DiscreteValueSelector

dpg.create_context()

# ✅ Crear la ventana principal antes de usarla como parent
#with dpg.window(tag="main_window"):
#    pass




SUBJECT_SELECTOR_TAGS = {
    "progress_bar_subject" : "progress_bar_subject",
    "subject_selector" : "subject_selector",
}

class SubjectSelector:
    """
    Component responsible for managing the subjects assigned to a professor, classroom, or group.

    This component allows the registration of two optional callbacks, both following the standard Dear PyGui signature:
        callback(sender, app_data, user_data)

    Callbacks:
    - on_subject_change: Triggered when the selected subject changes.
      - Sender = "subject_selector" 
      - app_data = value selected of Sender (example  : "Matematicas Actuariales MATACT ID = 1)
      - user_data = id of subject Selected (Example : 1)
    - on_color_change: Triggered when the color of a specific subject is modified.
      -  Sender = "subject_color_editor" 
      -  app_data = color selected (example [0.1, 0.1, 0.1, 1])
      -  user_data = id of subject selected (example 1)

    Parameters:
    - mode (str): One of ["PROFESSOR", "CLASSROOM", "GROUP"], indicating the context in which the component is used.
    - id_mode (int): The identifier corresponding to the selected mode.
    - db: Instance of the database manager used to handle subject-related data.
    """
    def __init__(self, id_mode, db, subject_changed_callback, color_change_callback, mode = "PROFESSOR"):
        self.subject_changed_callback = subject_changed_callback
        self.db = db
        self.mode = mode
        self.id_mode = id_mode
        self.color_change_callback = color_change_callback
        
        if self.mode == "PROFESSOR":
            self.ids_subjects = self.db.professors.get_subjects(self.id_mode)
        elif self.mode == "CLASSROOM":
            self.ids_subjects = self.db.classrooms.get_subjects(self.id_mode)
        else:
            self.ids_subjects = self.db.groups.get_subjects(self.id_mode)
            
        self.subjects_data = []  # <- Aquí guardaremos tuples (id, name, code)
        self.mode = mode
        
        
    def update_subjects_display(self):
        "actualiza las posibles materias que se pueden seleccionar"
        
        cursor = self.db.db_connection.cursor()
        
        list_subjects = "(" + ",".join(str(id_) for id_ in self.ids_subjects) + ")"
        cursor.execute(f"""
            SELECT ID, NAME, CODE
            FROM SUBJECT
            WHERE ID IN {list_subjects}
        """)
        
        self.subjects_data = cursor.fetchall() 

        subjects_display = [f"{name} {code} ID = {id_}" for id_, name, code in self.subjects_data]
        
        dpg.configure_item("subject_selector", items=subjects_display)
        dpg.set_value("subject_selector", subjects_display[0] if subjects_display else "")
        # llamamos al callback manualmente
        self.subject_changed_callback("subject_selector", subjects_display[0] if subjects_display else "", self.get_id() )
        self.color_editor.set_id_subject(self.get_id())

        pass
        
    def set_id_mode(self, new_id_mode):
        "change the id_mode preserving mode"
        self.id_mode = new_id_mode
        
        #actualizamos las materias dependiendo del modo 
        if self.mode == "PROFESSOR":
            self.ids_subjects = self.db.professors.get_subjects(self.id_mode)
        elif self.mode == "CLASSROOM":
            self.ids_subjects = self.db.classrooms.get_subjects(self.id_mode)
        else:
            self.ids_subjects = self.db.groups.get_subjects(self.id_mode)
            
        # actualizamos las materias sobre las cuales podemos seleccionar
        self.update_subjects_display()
        
        # cambiamos el color 
        color = self.get_subject_color()
        self.color_editor.set_color(color)
        
        #cambiamos la seleccion de slots
        self.update_subject_slots()
        self.update_bar_progress()
        
    def update_mode(self, new_mode, id_mode = None):
        "cnhages the mode and id_mode"
        self.mode = new_mode 
        self.set_id_mode(id_mode)
        

    def setup_ui(self, parent):
        "build a widget in interface"
        with dpg.group(parent = parent, horizontal=True):
            dpg.add_text("Materia :")
            
            dpg.add_combo(
                items=[""],
                default_value="",
                tag="subject_selector",
                width=530,
                callback=self.on_change_subject_selected,
                user_data=1,
            )
            # despues de crear el objecto lo actualizamos
            
            self.slots_selector = DiscreteValueSelector([0], "slots_subject")
            
            color = self.get_subject_color()
            dpg.add_text("  Color:")
            self.color_editor = SubjectColorEditor(self.id_mode, self.get_id(), database_manager, self.on_change_color_subject, default_color=color)
            self.color_editor.setup_ui()
            
            self.update_subjects_display()


        with dpg.group(horizontal=True):
            dpg.add_spacer(width=10)
            dpg.add_text("Progresso Materia:")
            
            progress = self.get_progress_subject()

            dpg.add_progress_bar(default_value=progress,
                                 width=100,
                                 overlay=f"{int(progress * 100)}%",
                                 tag = "subject_progress")
            dpg.add_text("Tamaño Slot:")

            self.slots_selector.setup_widget()
            self.update_subject_slots()

    def update_subject_slots(self):
        "after update subject selected update the allowed slots"
        id_subject_selected = self.get_id()
        
        allowed_slots = self.db.subjects.get_allowed_slots(id_subject_selected)
        
        self.slots_selector.set_allowed_values(allowed_slots)
        pass

    def get_selected_subject_index(self):
        selected = dpg.get_value("subject_selector")
        for i, (id_, name, code) in enumerate(self.subjects_data):
            if selected == f"{name} {code} ID = {id_}":
                return i
        return None

    def get_id(self):
        idx = self.get_selected_subject_index()
        return self.subjects_data[idx][0] if idx is not None else None

    def get_name(self):
        idx = self.get_selected_subject_index()
        return self.subjects_data[idx][1] if idx is not None else None

    def get_code(self):
        idx = self.get_selected_subject_index()
        return self.subjects_data[idx][2] if idx is not None else None

    def get_subject_slot(self):
        # seleccionar dependiendo del color del padre que proviene 
        return self.slots_selector.get_value()
    
    def get_subject_color(self):
        
        id_subject = self.get_id()
                
        if self.mode == "PROFESSOR":
            color = self.db.professors.get_subject_color(id_subject)
        elif self.mode == "PROFESSOR":
            color = self.db.classrooms.get_subject_color(id_subject)
        else:
            color = self.db.groups.get_subject_color(id_subject)
        if color == None:
            color = (0, 0, 0)
        return color
        pass

    def on_change_subject_selected(self, sender, app_data, user_data, force = True):
        self.subject_changed_callback(sender, app_data, user_data)
        
        
        self.update_subject_slots()
        self.update_bar_progress()
        
        if self.mode == "PROFESSOR":
            color = self.db.professors.get_subject_color(self.get_id())
        elif self.mode == "CLASSROOM":
            color = self.db.classrooms.get_subject_color(self.get_id())
        else:
            color = self.db.groups.get_subject_color(self.get_id())
            
        self.color_editor.set_id_subject(self.get_id())
        self.color_editor.set_color(color)
        
        pass

    def on_change_color_subject(self, sender, app_data, user_data):
        self.color_change_callback(sender, app_data, user_data)
        
        # cambiar el color en la base de datos
        
        id_subject = self.get_id()
        id_mode = self.id_mode
        
        print("ID_SUBJECT = ", id_subject)
        
        color = self.color_editor.get_color() # extrae el color del color picker
        red = color[0]
        green = color[1]
        blue = color[2]

                
        if self.mode == "PROFESSOR":
            self.db.professors.set_subject_color(id_mode, id_subject, red, green, blue)
        elif self.mode == "CLASSROOM":
            self.db.classrooms.set_subject_color(id_mode, id_subject, red, green, blue)
        else:
            self.db.groups.set_subject_color(id_mode, id_subject, red, green, blue)
    
    def get_progress_subject(self):
        
        cursor = self.db.db_connection.cursor()
        
        if self.get_id() == None:
            # ! el valor por defecto cuando un professor no tiene ninguna materia
            return 1
        
        cursor.execute(f"""
            SELECT TOTAL_SLOTS
            FROM SUBJECT 
            WHERE ID = {self.get_id()}
        """)
        
        total_slots = cursor.fetchone()[0]
        
        cursor.execute(f"""
            SELECT SUM(LEN)
            FROM SUBJECT_SLOTS
            WHERE ID_SUBJECT =  {self.get_id()}     
        """)
        
        completed_slots = cursor.fetchone()[0]
        
        if completed_slots == None:
            completed_slots = 0
        progress = completed_slots / total_slots if not total_slots  == 0 else 1
        return progress

    def update_bar_progress(self):
        
        progress = self.get_progress_subject()
        dpg.set_value("subject_progress", progress)
        dpg.configure_item("subject_progress", overlay=f"{int(progress * 100)}%")
        pass