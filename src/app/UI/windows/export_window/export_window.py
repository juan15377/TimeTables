import dearpygui.dearpygui as dpg
from .list_classrooms import ListaAulasApp, ListaProfesoresApp
from .list_groups import ListaGruposApp
from src.app.database import database_manager
from src.app.UI.components.windows_manager import Window, windows_manager
from src.app.UI.windows_tags import EXPORT_WINDOW_TAG

class ExportWindow(Window):
    def __init__(self, db):
        self.db = db
        self.tab_professors_tag = "list_professors_export"
        self.tab_classrooms_tag = "list_classrooms_export"
        self.tab_groups_tag = "list_groups_export"
        super().__init__(EXPORT_WINDOW_TAG)
        super().create()
        
    def _create_content(self):
        with dpg.group(horizontal=True):
            dpg.add_button(label="Exportar Horario Completo")
            dpg.add_button(label="Exportar Horario Completo en un solo archivo")
            dpg.add_spacing()
        
        dpg.add_separator()
        
        with dpg.tab_bar(tag="test_tab_bar"):
            # Tab 1
            with dpg.tab(label="Professor"):
                with dpg.group(tag=self.tab_professors_tag):
                    pass
            
            # Tab 2
            with dpg.tab(label="Grupo"):
                with dpg.group(tag=self.tab_groups_tag):
                    pass
            
            # Tab 3
            with dpg.tab(label="Aula"):
                with dpg.group(tag=self.tab_classrooms_tag):
                    pass
                
        
    
    def show(self):
        lp = ListaProfesoresApp(self.db)
        lg = ListaGruposApp(self.db)
        la = ListaAulasApp(self.db)
        
        dpg.delete_item(self.tab_professors_tag, children_only=True)
        dpg.delete_item(self.tab_classrooms_tag, children_only=True)
        dpg.delete_item(self.tab_groups_tag, children_only=True)
        
        # Set the parent directly instead of creating new groups
        lp.setup_ui(parent=self.tab_professors_tag)
        lg.setup_ui(parent=self.tab_groups_tag)
        la.setup_ui(parent=self.tab_classrooms_tag)
        super().show()
        