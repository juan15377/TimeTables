import flet as ft

def main(page: ft.Page):
    page.title = "Animación en Hover"

    # Crear un contenedor con color y tamaño inicial
    container = ft.Container(
        content=ft.Text("Pasa el mouse sobre mí", style=ft.TextStyle(size=20)),
        width=200,
        height=100,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.GREEN,
        border_radius=20,
        animate=ft.animation.scale(1.2, duration=500),  # Animación cuando pasa el mouse
    )

    # Aplicar la animación cuando el mouse pasa por encima del contenedor
    def on_hover(e):
        if e.data == "enter":
            container.animate = ft.animation.scale(1.5, duration=300)  # Aumentar tamaño
        else:
            container.animate = ft.animation.scale(1.2, duration=300)  # Reducir tamaño
        page.update()

    # Agregar el evento de hover al contenedor
    container.on_hover = on_hover

    # Agregar el contenedor a la página
    page.add(container)

ft.app(target=main)


