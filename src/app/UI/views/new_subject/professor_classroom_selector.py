
import dearpygui.dearpygui  as dpg

class ProfessorClassroomSelected():
    
    def __init__(self, db):
        
        self.tag_professor_combo = "PROFESSOR_SELECTED_NEW_SUBJECT"
        self.tag_classroom_combo = "CLASSROOM_SELECTED_NEW_SUBJECT"
        
        self.tag_input_text_filter_professors = "PROFESSOR_FILTER_NEW_SUBJECT"
        self.tag_input_text_filter_classrooms = "CLASSROOM_FILTER_NEW_SUBJECT"
        
        self.db = db
        
    
    def setup_ui(self, parent):

        query_get_professors = """
        
        SELECT ID, NAME
        FROM PROFESSOR
        """
        
        query_get_classrooms = """
        
        SELECT ID, NAME
        FROM CLASSROOM
        """
        
        cursor = self.db.execute_query(
            query_get_professors
        )
        
        self.professor_items = [f"{name}  (id = {id})" for (id, name) in cursor]
        cursor.close()
        
        cursor = self.db.execute_query(
            query_get_classrooms
        )
        
        self.classroom_items = [f"{name} (id = {id})" for (id, name ) in cursor]
        cursor.close()
        
        def filter_items(sender, app_data, user_data):
            "filter professor and classrooms on input text change"
            coincidence = app_data 
            
            if sender == self.tag_input_text_filter_professors:
                selector_tag = self.tag_professor_combo
                all_items = self.professor_items 
            elif sender == self.tag_input_text_filter_classrooms:
                selector_tag = self.tag_classroom_combo
                all_items = self.classroom_items 
                
            filter_items = [item for item in all_items if coincidence in item] if coincidence != "" else all_items
            dpg.configure_item(selector_tag, 
                                items = filter_items)
                
            current_selection = dpg.get_value(selector_tag)
            dpg.configure_item(selector_tag, items = filter_items)
            
            
            if current_selection not in filter_items and len(filter_items) > 0:
                dpg.set_value(selector_tag, filter_items[0])
            elif not len(filter_items) > 0:
                dpg.set_value(selector_tag, "")
            
        
    
        with dpg.group(horizontal=True):
            
            with dpg.group(horizontal=False):
                dpg.add_input_text(
                    tag = self.tag_input_text_filter_professors,
                    callback= filter_items,
                    hint=f"Buscar profesor",

                )
                
                dpg.add_combo(
                    items=self.professor_items,
                    tag = self.tag_professor_combo,
                )
                

            
            with dpg.group(horizontal=False):
                dpg.add_input_text(
                    tag = self.tag_input_text_filter_classrooms,
                    callback= filter_items,

                )
                
                dpg.add_combo(
                    items = self.classroom_items,
                    tag = self.tag_classroom_combo
                )
                

        
        pass 
    
    def get_id_professor_selected(self):
        
        pass  
    
    def get_id_classroom_selected(self):
        pass  
            
            
from src.app.database import database_manager 
dpg.create_context()

object_ = ProfessorClassroomSelected(database_manager)
with dpg.window(label="Sistema de Horarios", tag="main_window", width=780, height=580):

    with dpg.group(tag = "HOLA"):
        object_.setup_ui("HOLA")

dpg.create_viewport(title="Sistema de Horarios", width=1000, height=800)
dpg.set_primary_window("main_window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()