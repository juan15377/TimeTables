import flet as ft
class NameEditor(ft.Container):
    
    def __init__(self, name):
        
        self.name = name
        
        def change_name(e):
            self.name = e.control.value
            
        self.name_textfield = ft.TextField(
            value = self.name,
            label="Nombre",
            border=ft.InputBorder.UNDERLINE,
            filled=True,
            hint_text="Insertar Nombre",
            on_change = change_name,
            max_length = 50,
            expand = True
        )
        
        layout = ft.Row(
            controls = [
                self.name_textfield,
            ],
            expand = True
        )
        
        super().__init__(
            content = layout,
            height = 80,
            expand = True
        )