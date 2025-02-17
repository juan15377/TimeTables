import flet as ft

def main(page: ft.Page):
    page.title = "Cuadrícula de Horarios"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Definir los días de la semana
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    # Definir las horas del día
    horas_dia = [f"{h:02d}:00" for h in range(8, 22)]

    # Crear la cuadrícula
    grid = ft.GridView(
        expand=1,
        runs_count=len(dias_semana),
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=10,
        run_spacing=10,
    )

    # Añadir los días de la semana como encabezados
    for dia in dias_semana:
        grid.controls.append(
            ft.Container(
                content=ft.Text(dia, size=16, weight=ft.FontWeight.BOLD),
                alignment=ft.alignment.center,
                bgcolor=ft.colors.BLUE_200,
                padding=10,
                border_radius=5,
            )
        )

    # Añadir las horas y celdas vacías
    for hora in horas_dia:
        grid.controls.append(
            ft.Container(
                content=ft.Text(hora, size=14),
                alignment=ft.alignment.center,
                bgcolor=ft.colors.GREY_200,
                padding=10,
                border_radius=5,
            )
        )
        for _ in range(len(dias_semana) - 1):
            grid.controls.append(
                ft.Container(
                    content=ft.Text("", size=14),
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.WHITE,
                    padding=10,
                    border_radius=5,
                    border=ft.border.all(1, ft.colors.GREY_300),
                )
            )

    page.add(grid)

ft.app(target=main)