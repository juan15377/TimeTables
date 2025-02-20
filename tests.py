import flet as ft
import asyncio

def main(page: ft.Page):
    async def on_long_press(e):
        container.bgcolor = "red"  # Cambia el color al presionar
        container.update()
        await asyncio.sleep(0.3)  # Espera 200ms antes de volver al color original
        container.bgcolor = "blue"  # Vuelve al color original
        container.update()

    def handle_long_press(e):
        page.run_task(on_long_press, e)  # Llama a la función asincrónica de forma segura en Flet

    container = ft.Container(
        content=ft.Text("Mantén presionado"),
        width=200,
        height=100,
        bgcolor="blue",
        border_radius=10,
        alignment=ft.alignment.center,
        on_long_press=handle_long_press,  # Llama a la función de manejo
    )

    page.add(container)

ft.app(target=main)
