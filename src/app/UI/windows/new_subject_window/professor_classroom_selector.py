import dearpygui.dearpygui as dpg

class ProfessorClassroomSelected():
    def __init__(self, db):
        self.tag_professor_combo = "PROFESSOR_SELECTED_NEW_SUBJECT"
        self.tag_classroom_combo = "CLASSROOM_SELECTED_NEW_SUBJECT"
        self.tag_input_text_filter_professors = "PROFESSOR_FILTER_NEW_SUBJECT"
        self.tag_input_text_filter_classrooms = "CLASSROOM_FILTER_NEW_SUBJECT"
        self.db = db
        self.professor_items = []
        self.classroom_items = []
        self.professor_id_map = {}  # Maps display string to professor ID
        self.classroom_id_map = {}  # Maps display string to classroom ID

    def setup_ui(self, parent):
        # Query to get professors
        query_get_professors = """
        SELECT ID, NAME
        FROM PROFESSOR
        """
        
        # Query to get classrooms
        query_get_classrooms = """
        SELECT ID, NAME
        FROM CLASSROOM
        """
        
        # Fetch professors
        cursor = self.db.execute_query(query_get_professors)
        self.professor_items = []
        self.professor_id_map = {}
        for id, name in cursor:
            display_string = f"{name} (id = {id})"
            self.professor_items.append(display_string)
            self.professor_id_map[display_string] = id
        cursor.close()
        
        # Fetch classrooms
        cursor = self.db.execute_query(query_get_classrooms)
        self.classroom_items = []
        self.classroom_id_map = {}
        for id, name in cursor:
            display_string = f"{name} (id = {id})"
            self.classroom_items.append(display_string)
            self.classroom_id_map[display_string] = id
        cursor.close()
        
        # Create UI layout
        with dpg.group(horizontal=True, parent=parent):
            with dpg.group(horizontal=False):
                dpg.add_text("Profesor:")
                dpg.add_input_text(
                    tag=self.tag_input_text_filter_professors,
                    callback=lambda sender, app_data: self.filter_items(sender, app_data, None),
                    hint="Buscar profesor",
                    width=250
                )
                dpg.add_combo(
                    items=self.professor_items,
                    tag=self.tag_professor_combo,
                    width=250
                )
            
            dpg.add_spacer(width=20)
            
            with dpg.group(horizontal=False):
                dpg.add_text("Aula:")
                dpg.add_input_text(
                    tag=self.tag_input_text_filter_classrooms,
                    callback=lambda sender, app_data: self.filter_items(sender, app_data, None),
                    hint="Buscar aula",
                    width=250
                )
                dpg.add_combo(
                    items=self.classroom_items,
                    tag=self.tag_classroom_combo,
                    width=250
                )

    def filter_items(self, sender, app_data, user_data):
        """Filter professor and classrooms on input text change"""
        coincidence = app_data.lower()  # Case-insensitive search
        
        if sender == self.tag_input_text_filter_professors:
            selector_tag = self.tag_professor_combo
            all_items = self.professor_items
        elif sender == self.tag_input_text_filter_classrooms:
            selector_tag = self.tag_classroom_combo
            all_items = self.classroom_items
        else:
            return
            
        filter_items = [item for item in all_items if coincidence in item.lower()] if coincidence != "" else all_items
        
        # Save current selection before updating items
        current_selection = dpg.get_value(selector_tag)
        
        # Update items in the combo box
        dpg.configure_item(selector_tag, items=filter_items)
        
        # Handle selection after filtering
        if current_selection not in filter_items:
            if len(filter_items) > 0:
                dpg.set_value(selector_tag, filter_items[0])
            else:
                dpg.set_value(selector_tag, "")

    def get_id_professor_selected(self):
        """Extract the ID of the selected professor from the combo box"""
        selected_professor = dpg.get_value(self.tag_professor_combo)
        if not selected_professor:
            return None
        
        # Get ID from the mapping
        return self.professor_id_map.get(selected_professor)

    def get_id_classroom_selected(self):
        """Extract the ID of the selected classroom from the combo box"""
        selected_classroom = dpg.get_value(self.tag_classroom_combo)
        if not selected_classroom:
            return None
            
        # Get ID from the mapping
        return self.classroom_id_map.get(selected_classroom)


# Example usage
if __name__ == "__main__":
    from src.app.database import database_manager
    
    dpg.create_context()
    
    object_ = ProfessorClassroomSelected(database_manager)
    
    with dpg.window(label="Sistema de Horarios", tag="main_window", width=780, height=580):
        with dpg.group(tag="selection_group"):
            object_.setup_ui("selection_group")
            
        # Example button that uses the selected IDs
        def on_button_click():
            prof_id = object_.get_id_professor_selected()
            classroom_id = object_.get_id_classroom_selected()
            print(f"Selected Professor ID: {prof_id}")
            print(f"Selected Classroom ID: {classroom_id}")
            
        dpg.add_spacer(height=20)
        dpg.add_button(label="Get Selected IDs", callback=on_button_click)
    
    dpg.create_viewport(title="Sistema de Horarios", width=1000, height=800)
    dpg.set_primary_window("main_window", True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()