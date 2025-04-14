import dearpygui.dearpygui as dpg
from src.schedule_app.UI.components.grid_subjects.grid_subjects import ScheduleGrid
from src.schedule_app.database import database_manager

dpg.create_context()


class SelectorBase:
    """Base class for selectors with common functionality"""
    def __init__(self, db, entity_type, callback=None):
        self.db = db
        self.entity_type = entity_type  # "PROFESSOR" or "CLASSROOM"
        self.items = []
        self.original_items = []  # Lista completa sin filtrar
        self.progress_bar_tag = f"{entity_type.lower()}_progress"
        self.filter_input_tag = f"{entity_type.lower()}_filter"
        self.selector_tag = f"{entity_type.lower()}_selector"
        self.callback = callback
        
    def setup_ui(self, parent):
        self._load_items()
        
        # Añadimos el campo de filtro con botón para limpiar
        with dpg.group(horizontal=True):
            dpg.add_text("Filtrar:")
            dpg.add_input_text(
                tag=self.filter_input_tag,
                width=300,
                hint=f"Buscar por nombre o ID...",
                callback=self._filter_items
            )
            dpg.add_button(
                label="Limpiar",
                callback=self._clear_filter
            )
            
            dpg.add_spacer()
                    
            dpg.add_text("Progresso :")
            dpg.add_progress_bar(
                default_value=0.0,
                width=150,
                tag=self.progress_bar_tag,
                overlay="0%"
            )
                
        with dpg.group(horizontal=True):
            dpg.add_text(f"{self.entity_type.title()} :")
            dpg.add_combo(
                items=self.items,
                default_value=self.items[0] if self.items else "",
                tag=self.selector_tag,
                width=600,
                height_mode=10,
                user_data=self.items[0] if self.items else "",
                callback=self._on_selection_change
            )

    def _load_items(self):
        """Load items from database"""
        cursor = self.db.db_connection.cursor()
        cursor.execute(f"""
        SELECT CONCAT(NAME, " ( id = ",ID, " )" )
        FROM {self.entity_type};
        """)
        self.items = list(map(lambda e: e[0], cursor.fetchall()))
        self.original_items = self.items.copy()
    
    def _clear_filter(self, sender, app_data, user_data):
        """Limpia el filtro y restaura la lista completa"""
        dpg.set_value(self.filter_input_tag, "")
        self.items = self.original_items.copy()
        dpg.configure_item(self.selector_tag, items=self.items)
        if self.items:
            dpg.set_value(self.selector_tag, self.items[0])
            
        # Update progress bar after selection change
        self.update_progress_bar()
    
    def _filter_items(self, sender, app_data, user_data):
        """Filtra la lista según el texto ingresado"""
        filter_text = app_data.lower()
        
        if not filter_text:
            # Si no hay texto de filtro, restaurar la lista completa
            self.items = self.original_items.copy()
        else:
            # Filtrar por nombre o ID
            self.items = [item for item in self.original_items if filter_text in item.lower()]
        
        # Actualizar el combo box con la lista filtrada
        current_selection = dpg.get_value(self.selector_tag)
        dpg.configure_item(self.selector_tag, items=self.items)
        
        # Si la selección actual ya no está en la lista filtrada y hay elementos,
        # establecer el primer elemento como seleccionado
        if current_selection not in self.items and self.items:
            dpg.set_value(self.selector_tag, self.items[0])
        # Si no hay elementos en la lista filtrada, limpiar la selección
        elif not self.items:
            dpg.set_value(self.selector_tag, "")
            
        # Update progress bar after selection change
        self.update_progress_bar()
    
    def get_id_selected(self):
        """Extract the ID from the selected item in the combo box"""
        selected_item = dpg.get_value(self.selector_tag)
        if not selected_item:
            return None
            
        # Parse the ID from the string format "NAME ( id = ID )"
        try:
            entity_id = int(selected_item.split("id = ")[1].split(" )")[0])
            return entity_id
        except (IndexError, ValueError, AttributeError):
            print(f"Error extracting {self.entity_type} ID from selection")
            return None
    
    def update(self):
        """Update the UI components with fresh data"""
        # Refresh the list
        cursor = self.db.db_connection.cursor()
        cursor.execute(f"""
        SELECT CONCAT(NAME, " ( id = ",ID, " )" )
        FROM {self.entity_type};
        """)
        new_items = list(map(lambda e: e[0], cursor.fetchall()))
        
        # Update the original items list
        if new_items != self.original_items:
            self.original_items = new_items
            
            # Reaplica el filtro actual
            filter_text = dpg.get_value(self.filter_input_tag).lower()
            if filter_text:
                self.items = [item for item in self.original_items if filter_text in item.lower()]
            else:
                self.items = self.original_items.copy()
            
            # Update combo box
            current_selection = dpg.get_value(self.selector_tag)
            dpg.configure_item(self.selector_tag, items=self.items)
            
            # If the current selection is no longer in the list, reset to first item
            if current_selection not in self.items and self.items:
                dpg.set_value(self.selector_tag, self.items[0])
            elif not self.items:
                dpg.set_value(self.selector_tag, "")
        
        # Update the progress bar
        self.update_progress_bar()
    
    def update_progress_bar(self):
        """Update the progress bar - to be implemented by subclasses"""
        pass
    
    def _on_selection_change(self, sender, app_data, user_data):
        """Callback when selection changes"""
        self.update_progress_bar()
        if self.callback:
            self.callback(sender, app_data, user_data)


class ProfessorSelector(SelectorBase):
    def __init__(self, db, callback=None):
        super().__init__(db, "PROFESSOR", callback)

    def update_progress_bar(self):
        """Update the progress bar based on professor data"""
        professor_id = self.get_id_selected()
        if professor_id is not None:
            cursor = self.db.db_connection.cursor()
            cursor.execute("""
            SELECT SUM(TOTAL_SLOTS)
            FROM SUBJECT 
            WHERE ID IN (SELECT ID_SUBJECT FROM PROFESSOR_SUBJECT WHERE ID_PROFESSOR = ?)
            """, (professor_id,))
            
            result = cursor.fetchone()
            total_slots = result[0] if result[0] is not None else 0
            
            cursor.execute("""
            SELECT SUM(LEN)
            FROM SUBJECT_SLOTS
            WHERE ID_SUBJECT IN (SELECT ID_SUBJECT FROM PROFESSOR_SUBJECT WHERE ID_PROFESSOR = ?)
            """, (professor_id,))
            
            result = cursor.fetchone()
            completed_slots = result[0] if result[0] is not None else 0
            
            # Avoid division by zero
            progress = completed_slots / total_slots if total_slots > 0 else 0
            
            # Update progress bar
            dpg.set_value(self.progress_bar_tag, progress)
            dpg.configure_item(self.progress_bar_tag, overlay=f"{int(progress * 100)}%")
        else:
            # If no professor selected, show 0%
            dpg.set_value(self.progress_bar_tag, 0.0)
            dpg.configure_item(self.progress_bar_tag, overlay="0%")


class ClassroomSelector(SelectorBase):
    def __init__(self, db, callback=None):
        super().__init__(db, "CLASSROOM", callback)

    def update_progress_bar(self):
        """Update the progress bar based on classroom data"""
        classroom_id = self.get_id_selected()
        if classroom_id is not None:
            cursor = self.db.db_connection.cursor()
            
            # Get total available slots for this classroom (total hours in the week)
            cursor.execute("""
            SELECT COUNT(*) * 5  -- Assuming 5 working days
            FROM TIME_SLOT;
            """)
            result = cursor.fetchone()
            total_available_slots = result[0] if result[0] is not None else 0
            
            # Get used slots (scheduled classes) for this classroom
            cursor.execute("""
            SELECT COUNT(*)
            FROM SUBJECT_SLOTS
            WHERE ID_CLASSROOM = ?
            """, (classroom_id,))
            
            result = cursor.fetchone()
            used_slots = result[0] if result[0] is not None else 0
            
            # Calculate usage percentage
            progress = used_slots / total_available_slots if total_available_slots > 0 else 0
            
            # Update progress bar
            dpg.set_value(self.progress_bar_tag, progress)
            dpg.configure_item(self.progress_bar_tag, overlay=f"{int(progress * 100)}%")
        else:
            # If no classroom selected, show 0%
            dpg.set_value(self.progress_bar_tag, 0.0)
            dpg.configure_item(self.progress_bar_tag, overlay="0%")

grilla = ScheduleGrid(database_manager, "PROFESSOR", 2)
prof = ProfessorSelector(database_manager, lambda e, r, f: grilla.set_id_mode(prof.get_id_selected()))
clas = ClassroomSelector(database_manager, lambda e, j, k: print("HOLA"))

def change_tab(sender, app_data):
    # Obtener el tag del tab bar
    tab_bar = "test_tab_bar"
    
    # Cambiar al tab 2 si el botón presionado es el 100, sino al tab 1
    if sender == 100:
        dpg.set_value(tab_bar, "test_tab_2")  # Cambia a Tab 2
    else:
        dpg.set_value(tab_bar, "test_tab_1")  # Cambia a Tab 1

with dpg.window(label="Window", tag="main_window"):
    # Tab bar (asegúrate de que los tags de los tabs sean strings únicos)
    with dpg.tab_bar(tag="test_tab_bar"):
        # Tab 1
        with dpg.tab(label="Professor", tag="test_tab_1"):
            prof.setup_ui(parent="main_window")
                    
        # Tab 2
        with dpg.tab(label="Grupo", tag="test_tab_2"):
            #grilla.setup_ui()
            pass            
        with dpg.tab(label="Aula", tag="test_tab_3"):
            clas.setup_ui(parent="main_window")
            
    grilla.setup_ui()

# Configuración del viewport
dpg.create_viewport(title="Switch entre Tabs", width=1000, height=800)
dpg.set_primary_window("main_window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()