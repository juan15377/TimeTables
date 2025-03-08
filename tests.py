import flet as ft

def main(page: ft.Page):
    # Configurar el tema oscuro
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "Insertar Materia y Código"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Función para manejar el envío del formulario
    def submit_form(e):
        if nombre_materia.value and codigo_materia.value:
            print(f"Materia: {nombre_materia.value}, Código: {codigo_materia.value}")
            page.snack_bar = ft.SnackBar(
                ft.Text("Datos enviados correctamente!", color=ft.colors.GREEN_200),
                bgcolor=ft.colors.GREEN_900,
            )
            page.snack_bar.open = True
            nombre_materia.value = ""
            codigo_materia.value = ""
            page.update()
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("Por favor, completa todos los campos.", color=ft.colors.RED_200),
                bgcolor=ft.colors.RED_900,
            )
            page.snack_bar.open = True
            page.update()

    # Campos de entrada con estilo personalizado
    nombre_materia = ft.TextField(
        label="Nombre de la Materia",
        width=300,
        border_radius=10,
        border_color=ft.colors.BLUE_200,
        focused_border_color=ft.colors.BLUE_400,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.BLACK12,
    )

    codigo_materia = ft.TextField(
        label="Código de la Materia",
        width=300,
        border_radius=10,
        border_color=ft.colors.BLUE_200,
        focused_border_color=ft.colors.BLUE_400,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.BLACK12,
    )

    # Botón de envío con estilo personalizado
    submit_button = ft.ElevatedButton(
        "Enviar",
        on_click=submit_form,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE_800,
            color=ft.colors.WHITE,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
    )

    # Diseño del componente
    form = ft.Container(
        content=ft.Column(
            [
                ft.Text("Registro de Materia", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_200),
                nombre_materia,
                codigo_materia,
                submit_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
        padding=30,
        border_radius=15,
        bgcolor=ft.colors.BLACK26,
        border=ft.border.all(2, ft.colors.BLUE_200),
    )

    # Añadir el componente a la página
    page.add(form)

ft.app(target=main)