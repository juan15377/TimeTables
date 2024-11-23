import flet as ft  


class name_and_abrevation(ft.Container):

    def __init__(self, name : str = "", abrevation : str = ""):

        self.name = name
        self.abrevation = abrevation

        def change_name(e):
            self.name = e.control.value

        def change_abrevation(e):
            self.abrevation = e.control.value

        name_textfield = ft.TextField(
            value = self.name,
            label="Nombre",
            border=ft.InputBorder.UNDERLINE,
            filled=True,
            hint_text="Enter text here",
            on_change = change_name,
            max_length = 50
        )

        abrevation_textfield = ft.TextField(
            value = self.abrevation,
            label="Abreviatura",
            border=ft.InputBorder.UNDERLINE,
            filled=True,
            hint_text = "Enter text here",
            on_change = change_abrevation,
            max_length = 5
        )

        layout = ft.Row(
            controls = [
                name_textfield,
                abrevation_textfield,
            ]
        )

        super().__init__(
            content = layout,
            width = 400,
            height = 120,
            padding = 10,
        )

    def get_name_and_abrevation(self):
        return self.name, self.abrevation
    
    def set_name_and_abrevation(self, name, abrevation):
        self.name = name
        self.abrevation = abrevation
        self.name_textfield.value = name
        self.abrevation_textfield.value = abrevation

        self.abrevation_textfield.update()
        self.name_textfield.update()


def main(page : ft.Page):
    na = name_and_abrevation("Nombre", "MATAC")
    page.add(na)

ft.app(main)