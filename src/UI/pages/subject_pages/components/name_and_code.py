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
            label="Nombre de la materia",
            border_radius=10,
            border_color=ft.colors.BLUE_200,
            focused_border_color=ft.colors.BLUE_400,
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLACK12,
            on_change= change_name
        )

        
        self.code_textfield = ft.TextField(
        value = self.code,
        label="Codigo de la Materia",
        border_radius=10,
        border_color=ft.colors.BLUE_200,
        focused_border_color=ft.colors.BLUE_400,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.BLACK12,
        on_change= change_code
        )

        layout = ft.Column(
            controls = [
                self.name_textfield,
                self.code_textfield,
            ],
            expand = False,
        )

        layout = ft.Container(
            content=ft.Column(
                [
                    self.name_textfield,
                    self.code_textfield,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            bgcolor=ft.colors.BLACK26,
        )
        super().__init__(
            content = layout,
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