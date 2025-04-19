import dearpygui.dearpygui as dpg
from typing import Tuple, Optional

class SubjectColorEditor:

    """
    Component responsible for managing the color of subjects.

    This component allows the registration of callback, both following the standard Dear PyGui signature:
        callback(sender, app_data, user_data)

    Callbacks:
    - change_color_callback: Triggered when the selected color changes.
      - Sender = "color_picker_subject" 
      - app_data = color_selected of Sender (example : [.1, .1, .1, 1])
      - user_data = id of subject Selected (Example : 1)


    Parameters:
    - mode (str): One of ["PROFESSOR", "CLASSROOM", "GROUP"], indicating the context in which the component is used.
    - id_mode (int): The identifier corresponding to the selected mode.
    - db: Instance of the database manager used to handle subject-related data.
    """
    
    def __init__(self, id_mode, id_subject, db, change_color_callback, mode = "PROFESSOR",  default_color: Tuple[int, int, int] = (255, 255, 255)):

        
        self._current_color = default_color
        self._color_picker_tag = f"color_picker_subject"
        self._preview_tag = f"color_preview_{id(self)}"
        self._group_tag = f"color_group_{id(self)}"
        self._parent = None
        self.db = db
        self.mode = mode
        self.id_subject = id_subject
        self.id_mode = id_mode
        self.change_color_callback = change_color_callback

    def setup_ui(self, parent: Optional[int] = None):
        """Configura la UI de manera segura"""
        self._parent = parent
        
        # Verificar si el grupo ya existe
        if dpg.does_item_exist(self._group_tag):
            dpg.delete_item(self._group_tag)
        
        # Color Picker
        dpg.add_color_edit(
                default_value=self._current_color + (255,),
                tag=self._color_picker_tag,
                no_alpha=True,
                callback=self._on_color_changed,
                width=300,
                user_data=self.id_subject
        )

    def _draw_preview(self):
        """Dibuja el preview actual de manera segura"""
        if dpg.does_item_exist(self._preview_tag):
            dpg.delete_item(self._preview_tag, children_only=True)
            dpg.draw_rectangle(
                (0, 0), (30, 30),
                parent=self._preview_tag,
                fill=self._current_color,
                color=self._current_color
            )

    def _on_color_changed(self, sender, app_data, user_data):
        """Maneja cambios de color"""
        
        self._current_color = app_data[:3]
        self._draw_preview()
        
        self.change_color_callback(sender, app_data, user_data)

    def get_color(self) -> Tuple[int, int, int]:
        """Obtiene el color actual de forma confiable"""
        if dpg.does_item_exist(self._color_picker_tag):
            color = dpg.get_value(self._color_picker_tag)[:3]
            self._current_color = color
        return self._current_color

    def set_color(self, new_color: Tuple[int, int, int]):
        """Establece un nuevo color de manera segura"""
        self._current_color = new_color
        if dpg.does_item_exist(self._color_picker_tag):
            dpg.set_value(self._color_picker_tag, new_color + (255,))
        if dpg.does_item_exist(self._preview_tag):
            self._draw_preview()
            
            
    def set_id_subject(self, id_subject):
        print("CAMBIO de ID a ", id_subject)
        dpg.set_item_user_data(self._color_picker_tag, id_subject)
        self.id_subject = id_subject
        pass
    
