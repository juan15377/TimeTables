import flet as ft

def main(page: ft.Page):
    # Definir un tema personalizado
    custom_theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.BLUE_500,
            secondary=ft.colors.GREEN_500,
            background=ft.colors.BLACK38,
            surface=ft.colors.WHITE,
            error=ft.colors.RED_500,
            on_primary=ft.colors.WHITE,
            on_secondary=ft.colors.BLACK,
            on_background=ft.colors.BLACK,
            on_surface=ft.colors.BLACK,
            on_error=ft.colors.WHITE,
        ),
        use_material3=True  # Activar diseño Material 3
    )

    # Asignar el tema a la página
    page.theme = custom_theme
    page.title = "App con Tema Personalizado"

    # Crear widgets que usen el tema
    page.add(
        ft.Container(
            content=ft.Text("Texto usando el color primario", color=ft.colors.ON_PRIMARY),
            bgcolor=ft.colors.PRIMARY,
            padding=20,
            border_radius=10,
        ),
        ft.ElevatedButton("Botón secundario", bgcolor=ft.colors.SECONDARY, color=ft.colors.ON_SECONDARY),
        ft.Container(
            content=ft.Text("Fondo usando el color de superficie"),
            bgcolor=ft.colors.SURFACE,
            padding=20,
            border_radius=10,
        ),
    )

ft.app(target=main)

