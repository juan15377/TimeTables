import flet as ft

def main(page: ft.Page):
    def scroll_to_index(index):
        listview.scroll_to_index(index, alignment="start")
        page.update()

    def calculate_visible():
        # Supongamos que conocemos la altura de cada elemento
        visible_start = current_index
        visible_end = min(visible_start + num_visible_items - 1, len(items) - 1)
        visible_items_text.value = f"Visibles: {items[visible_start:visible_end + 1]}"
        page.update()

    def on_scroll(event):
        nonlocal current_index
        # Simular cambio de índice de desplazamiento
        current_index = min(len(items) - 1, max(0, current_index + 1))
        calculate_visible()

    items = [f"Elemento {i}" for i in range(100)]
    current_index = 0
    item_height = 50  # Altura de cada elemento en píxeles (estimada)
    listview_height = 300  # Altura visible del ListView
    num_visible_items = listview_height // item_height

    # Crear un ListView con eventos de scroll simulados
    listview = ft.ListView(
        height=listview_height,
        spacing=10,
        controls=[
            ft.Container(ft.Text(item), height=item_height, bgcolor=ft.colors.LIGHT_BLUE)
            for item in items
        ],
    )

    visible_items_text = ft.Text("Visibles: Ninguno")
    page.add(listview, visible_items_text)

    # Simular scroll y cálculo de elementos visibles
    page.add(ft.TextButton("Simular scroll", on_click=on_scroll))

ft.app(target=main)
