import flet as ft

name = "AppBar Example"


def example():

    pagelet = ft.Pagelet(
        appbar=ft.AppBar(
            leading=ft.IconButton(icon = ft.icons.ARROW_BACK, 
                                  on_click = lambda x: print("para atras")),
            leading_width=50,
            title=ft.Text(""),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Item 1"),
                        ft.PopupMenuItem(),  # divider
                        ft.PopupMenuItem(
                            text="Checked item",
                            checked=False,
                        ),
                    ]
                ),
            ],
        ),
        content=ft.Container(),
    )

    return pagelet

def main(page:ft.page):
    page.add(example())


ft.app(main)