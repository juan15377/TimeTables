import flet as ft

def main(page: ft.Page):
    def on_change(e):
        page.controls.clear()
        page.controls.append(ft.Text(f"Página seleccionada: {e.control.selected_index}"))
        page.update()

    nav = ft.NavigationBar(
        selected_index=0,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME, label="Inicio"),
            ft.NavigationDestination(icon=ft.icons.SEARCH, label="Buscar"),
            ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Configuración"),
        ],
        on_change=on_change,
    )

    page.add(nav)

ft.app(target=main)
