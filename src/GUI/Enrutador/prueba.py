import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors


def load_professor_page(profesor):
    
    pass

def load_classroom_page(classroom):
    pass 


def load_subjects_page(subject):
    pass


#/main/juan_de_jesus/calculo/



class Enruter_page():
    
    def __init__(self) -> None:
        pass


def main(page: Page):
    page.title = 'Ejemplo de Rutas'

    def route_change(route):
        page.views.clear()

        # Default view (home page)
        if page.route == '/':
            page.views.append(
                View(
                    '/',
                    [
                        AppBar(title=Text('App Flet'), bgcolor=colors.SURFACE_VARIANT),
                        ElevatedButton('Visitar la tienda', on_click=lambda _: page.go('/tienda')),
                        ElevatedButton('Visitar las materias', on_click=lambda _: page.go('/materias'))
                    ]
                )
            )

        # Tienda view
        elif page.route == '/tienda':
            page.views.append(
                View(
                    '/tienda',
                    [
                        AppBar(title=Text('Tienda'), bgcolor=colors.SURFACE_VARIANT),
                        ElevatedButton('Inicio', on_click=lambda _: page.go('/')),
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    "Range slider with divisions and labels",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Container(height=30)
                            ],
                        )
                    ]
                )
            )

        # Materias view
        elif page.route == '/materias':
            page.views.append(
                View(
                    '/materias',
                    [
                        AppBar(title=Text('Materias'), bgcolor=colors.SURFACE_VARIANT),
                        ElevatedButton('Inicio', on_click=lambda _: page.go('/')),
                        ElevatedButton('detalles', on_click=lambda _: page.go('/materias/detalles')),
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    "Puta_cola",  # This text can be changed
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Container(height=30)
                            ],
                        )
                    ]
                )
            )
            
        elif page.route == '/materias/detalles':
            page.views.append(
                View(
                    '/',
                    [
                        AppBar(title=Text('Juan_de_jesus/calculo'), bgcolor=colors.SURFACE_VARIANT),
                        ElevatedButton('materias', on_click=lambda _: page.go('/materias')),
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    "Puta_cola",  # This text can be changed
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Container(height=30)
                            ],
                        )
                    ]
                )
            )
        
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)

