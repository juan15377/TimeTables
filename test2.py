import flet as ft
import random

def random_color():
    """Genera un color aleatorio en formato hexadecimal."""
    return f"#{''.join(random.choices('0123456789ABCDEF', k=6))}"

def main(page: ft.Page):
    page.add(ft.ListView(
        controls=[
            ft.Row(
                [ft.Container(width=3, height=5, bgcolor=random_color()) for _ in range(32)],
                spacing=0
            ) for _ in range(7)
        ],
        spacing=0
    ))

ft.app(target=main)
