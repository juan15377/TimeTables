import flet as ft

def main(page: ft.Page):
    page.title = "Lista de Items con Añadir y Eliminar"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Lista de items
    items = ["Item 1", "Item 2", "Item 3"]

    # Función para eliminar un item
    def delete_item(e):
        item = e.control.data
        items.remove(item)
        list_view.controls.remove(e.control)
        page.update()

    # Función para añadir un item
    def add_item(e):
        new_item = new_item_textfield.value
        if new_item:
            items.append(new_item)
            list_view.controls.append(
                ft.ListTile(
                    title=ft.Text(new_item),
                    trailing=ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=delete_item,
                        data=new_item,
                    ),
                )
            )
            new_item_textfield.value = ""
            page.update()

    # ListView para mostrar los items
    list_view = ft.ListView(
        controls=[
            ft.ListTile(
                title=ft.Text(item),
                trailing=ft.IconButton(
                    icon=ft.icons.DELETE,
                    on_click=delete_item,
                    data=item,
                ),
            )
            for item in items
        ],
        expand=True,
    )

    # TextField para añadir nuevos items
    new_item_textfield = ft.TextField(hint_text="Añadir un nuevo item", expand=True)

    # Botón para añadir el item
    add_button = ft.ElevatedButton("Añadir", on_click=add_item)

    # Layout principal
    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        new_item_textfield,
                        add_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                list_view,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(target=main)