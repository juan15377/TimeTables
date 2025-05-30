from src.app.database import database_manager
import dearpygui.dearpygui as dpg
from src.app.UI.components.windows_manager import Window, windows_manager
from src.app.UI.windows_tags import IMPORT_DATABASE_WINDOW_TAG, MAIN_WINDOW_TAG
import dearpygui_extend as dpge


import os


class ImportDataBaseWindow(Window):
    
    def __init__(self, db):
        
        self.db = db 
        
        super().__init__(window_tag=IMPORT_DATABASE_WINDOW_TAG,
                         height=600, width=610,
                         no_resize=True,
                         label = "Importar Archivo")
        
        
        self.create()
        
    def _create_content(self):
        with dpg.group(horizontal=True):
            dpg.add_text("Ruta Base de Datos : ")
            dpg.add_text(tag = "select_directory_import_database")    
 
        def show_selected_file(sender, files, cancel_pressed):
            if not cancel_pressed:
                dpg.set_value('select_directory_import_database', files[0])
            
        dpge.add_file_browser(
            tag=None, 
            label=('Choose files', 'Select files or folders'), 
            width=600, 
            height=500, 
            pos=None, 
            default_path='~', 
            collapse_sequences=True, 
            collapse_sequences_checkbox=True, 
            sequence_padding='#', 
            show_hidden_files=True, 
            path_input_style=1, 
            add_filename_tooltip=False, 
            tooltip_min_length=100, 
            icon_size=1.0, 
            allow_multi_selection=False, 
            allow_drag=False, 
            allow_create_new_folder=True, 
            dirs_only=False, 
            show_as_window=False, 
            modal_window=True, 
            show_ok_cancel=True, 
            show_nav_icons=True, 
            user_data=None, 
            callback=show_selected_file
        )

        with dpg.group():
            def backup_database(sender, app_data, user_data):
                path = dpg.get_value("select_directory_import_database")
                name_file = dpg.get_value("name_import_database")
                
                file_path = os.path.join(path)
                
                print("FILE_PATH", file_path)
                
                try :
                    database_manager.import_database(file_path)
                    windows_manager.get_window(MAIN_WINDOW_TAG).update()
                    windows_manager.notification_system.show_notification("Importacion Finalizada")
                except:
                    windows_manager.notification_system.show_notification("Error al importar la base de datos", notification_type="error")
                
                
            with dpg.group(horizontal=True):
                dpg.add_button(label="Importar", callback= backup_database, height=30, width=100)
            

        


        return super()._create_content()
        
        pass