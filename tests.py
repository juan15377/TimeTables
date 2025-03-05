import flet as ft
import json  # Importamos json para parsear e.data
import time as tm 

def main(page: ft.Page):
    def on_scroll(e: ft.ControlEvent):
        """Muestra el porcentaje del scroll"""

        try:
            scroll_data = json.loads(e.data)  # Convertimos JSON string a diccionario
            print(scroll_data) #
            pos = scroll_data.get("p", 0)  # Posición actual del scroll
            max_scroll = scroll_data.get("maxse", 1)  # Máximo scroll posible

            if max_scroll > 0:
                scroll_percentage = round((pos / max_scroll) * 100, 2)  # Convertimos a porcentaje
                scroll_text.value = f"Scroll: {scroll_percentage}%"

                # Si estamos en el 90% del scroll, podemos cargar más datos
                if scroll_percentage >= 90:
                    load_more_items()

                page.update()

        except json.JSONDecodeError:
            print("Error al procesar el scroll:", e.data)  # Muestra el error en consola

    def load_more_items():
        """Función para cargar más elementos dinámicamente"""
        for i in range(len(list_view.controls), len(list_view.controls) + 10):
            list_view.controls.append(ft.Text(f"Ítem {i}"))
        page.update()

    list_view = ft.ListView(
        expand=True, spacing=10, padding=10, auto_scroll=False, 
        on_scroll=on_scroll, on_scroll_interval=100
    )

    # Agregamos 50 elementos iniciales
    for i in range(50):
        list_view.controls.append(ft.Text(f"Ítem {i}"))

    scroll_text = ft.Text("Scroll: 0%")  # Texto para mostrar el progreso
    page.add(list_view, scroll_text)
    tm.sleep(6)
    list_view.scroll_to("offset")

ft.app(target=main)
