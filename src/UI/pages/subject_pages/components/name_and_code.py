import flet as ft  



class NameCodeSubject(ft.Container):

    def __init__(self, name : str = "", code : str = ""):

        self.name = name
        self.code = code

        def change_name(e):
            self.name = e.control.value

        def change_code(e):
            self.code = e.control.value

        self.name_textfield = ft.TextField(
            value = self.name,
            label="Nombre",
            border=ft.InputBorder.UNDERLINE,
            filled=True,
            hint_text="Insertar Nombre Materia",
            on_change = change_name,
            max_length = 50,
            expand = True,
            cursor_color="white",
            border_color= ft.colors.AMBER,
            focused_color= ft.colors.WHITE,
        )

        self.code_textfield = ft.TextField(
            value = self.code,
            label="Codigo",
            border=ft.InputBorder.UNDERLINE,
            filled=True,
            hint_text = "Insertar Codigo Materia",
            on_change = change_code,
            max_length = 7,
            expand = True,
            width = 500,
            
        )

        layout = ft.Row(
            controls = [
                self.name_textfield,
                self.code_textfield,
            ],
            expand = True
        )

        super().__init__(
            content = layout,
            height = 80,
            expand = True
        )

    def get_name_and_code(self):
        return self.name, self.code
    
    def set_name_and_abrevation(self, new_name, new_code):
        self.name = new_name
        self.code = new_code
        self.name_textfield.value = new_name
        self.code_textfield.value = new_code

        self.code_textfield.update()
        self.name_textfield.update()

    def restart(self):
        self.set_name_and_abrevation("", "")
    
#
#def main(page : ft.Page):
#    na = NameCodeSubject("Nombre", "MATAC")
#    page.add(na)
#ft.app(main)