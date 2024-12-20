import flet as ft


def main(page: ft.Page):
    def handle_change(e: ft.ControlEvent):
        print(f"change on panel with index {e.data}")

    def handle_delete(e: ft.ControlEvent):
        panel.controls.remove(e.control.data)
        page.update()

    panel = ft.ExpansionPanelList(
        expand_icon_color=ft.colors.AMBER,
        elevation=8,
        divider_color=ft.colors.AMBER,
        on_change=handle_change,
        controls=[
            ft.Text("HOLA"),
            ft.Text("HOLA"),
            ft.Text("HOLA"),
            ft.Text("HOLA"),
            ft.Text("HOLA"),
            ft.ListView(
                controls = [
                    ft.Text("Hola"),
                    ft.Text("Mundo"),
                    ft.Text("Esto"),
                    ft.Text("Es"),
                    ft.Text("Una"),
                    ft.Text("Prueba"),
                ]
            )
        ]
    )

    colors = [
        ft.colors.GREEN_500,
        ft.colors.BLUE_800,
        ft.colors.RED_800,
    ]

    page.add(panel)


ft.app(main)