import flet as ft

def main(page: ft.Page):
    page.title = "Horario Mejorado"
    page.scroll = ft.ScrollMode.AUTO  # Habilita scroll en la página
    page.padding = 10
    page.theme_mode = ft.ThemeMode.LIGHT

    # Días de la semana
    days_of_week = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    timeslots = [
        "7:00 - 7:30 AM",
        "7:30 - 8:00 AM",
        "8:00 - 8:30 AM",
        "8:30 - 9:00 AM",
        "9:00 - 9:30 AM",
        "9:30 - 10:00 AM",
    ]

    # Contenedor para la cuadrícula
    grid = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=5,
    )

    # Encabezado de días
    days_row = ft.Row(
        controls=[
            ft.Container(
                content=ft.Text(day, weight="bold", color=ft.colors.WHITE),
                bgcolor=ft.colors.BLUE,
                alignment=ft.alignment.center,
                height=40,
                expand=1,
                border_radius=5,
            ) for day in days_of_week
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        spacing=5,
    )
    grid.controls.append(days_row)

    # Generar las filas de horarios
    for time in timeslots:
        time_row = ft.Row(
            controls=[
                # Celda de horario
                ft.Container(
                    content=ft.Text(time, color=ft.colors.BLACK),
                    bgcolor=ft.colors.LIGHT_BLUE_50,
                    alignment=ft.alignment.center,
                    height=40,
                    width=100,
                    border_radius=5,
                )
            ] + [
                # Botones para cada día
                ft.Container(
                    bgcolor=ft.colors.GREEN,
                    alignment=ft.alignment.center,
                    height=40,
                    expand=1,
                    border_radius=5,
                    on_click=lambda e, t=time, d=day: print(f"Clicked: {d} - {t}"),
                ) for day in days_of_week
            ],
            spacing=5,
        )
        grid.controls.append(time_row)

    # Agregar todo al contenedor principal con scroll
    page.add(
        ft.Container(
            content=grid,
            border=ft.border.all(1, ft.colors.GREY),
            padding=10,
            height=500,
            width=1000,
        )
    )

ft.app(target=main)
