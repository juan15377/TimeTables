import flet as ft

def main(page: ft.Page):
    def button_clicked(e):
        t.value = f"Dropdown value is:  {dd.value}"
        page.update()
    pb = ft.ProgressBar(width=400)
    pb.value = 0.5
    contenedor_nombre = ft.Row(controls = 
                                [ft.Text("Juan de Jesus Venegas Flores"),
                                 pb,
                                 ])

    t = ft.Text()
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    dd = ft.Dropdown(
        width=100,
        options=[
            contenedor_nombre,
            ft.dropdown.Option(contenedor_nombre),
            ft.dropdown.Option("Green"),
            ft.dropdown.Option("Blue"),
        ],
    )
    page.add(dd, b, t)

#ft.app(target=main)
import flet as ft

def main_(page):

    def close_anchor(e):
        text = f"Juan de Jesus"
        print(f"closing view from {text}")
        anchor.close_view(text)

    def handle_change(e):
        print(f"handle_change e.data: {e.data}")

    def handle_submit(e):
        print(f"handle_submit e.data: {e.data}")

    def handle_tap(e):
        print(f"handle_tap")

    pb = ft.ProgressBar(width=400)
    pb.value = 0.5
    contenedor_nombre = ft.Row(controls = 
                                [ft.Text("Juan de Jesus Venegas Flores"),
                                 pb,
                                 ])

    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Search colors...",
        view_hint_text="Choose a color from the suggestions...",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        controls=[
            ft.ListTile(title=contenedor_nombre, on_click=close_anchor, data=i)
            for i in range(10)
        ],
    )

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.OutlinedButton(
                    "Open Search View",
                    on_click=lambda _: anchor.open_view(),
                ),
            ],
        ),
        anchor,
    )


ft.app(target=main_)