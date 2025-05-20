from src.app.database import database_manager
import dearpygui.dearpygui as dpg
from src.app.UI.components.windows_manager import Window, windows_manager
from src.app.UI.windows_tags import SAVE_FILE_WINDOW_TAG
import dearpygui_extend as dpge


import os


class SaveFileWindow(Window):
    
    def __init__(self, db):
        
        self.db = db
        
        super().__init__(window_tag=SAVE_FILE_WINDOW_TAG,
                         height=580,
                         width=600,
                         no_resize=True)
        
        
        self.create()
        
    def _create_content(self):
        with dpg.group(horizontal=True):
            dpg.add_text(default_value= "Ruta : ")
            dpg.add_text(tag = "select_directory_save_database")
            
        with dpg.group(horizontal=True):
            dpg.add_text("Nombre Base de Datos")
            dpg.add_input_text(tag = "name_save_database")
        
 
        def show_selected_file(sender, files, cancel_pressed):
            if not cancel_pressed:
                dpg.set_value('select_directory_save_database', files[0])
            
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
            dirs_only=True, 
            show_as_window=False, 
            modal_window=True, 
            show_ok_cancel=True, 
            show_nav_icons=True, 
            user_data=None, 
            callback=show_selected_file
        )

        with dpg.group():
            def backup_database(sender, app_data, user_data):
                path = dpg.get_value("select_directory_save_database")
                name_file = dpg.get_value("name_save_database")
                
                file_path = os.path.join(path, name_file + ".db")
                
                print("FILE_PATH", file_path)
                database_manager.backup(file_path)
                
            with dpg.group(horizontal=True):
                dpg.add_button(label="Backup", callback= backup_database, height=30, width=100)
            


        return super()._create_content()
        
        pass