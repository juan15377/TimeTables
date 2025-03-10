import flet as ft

def main(page: ft.Page):
    page.title = "Tabla con Nombres en Varias Líneas"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Datos de la tabla
    nombres_largos = [
        {"nombre": "Juan Pérez González", "edad": 25},
        {"nombre": "María de los Ángeles López Martínez", "edad": 30},
        {"nombre": "Carlos Alberto Sánchez Ramírez", "edad": 22},
        {"nombre": "Ana Sofía García Rodríguez de la Cruz", "edad": 28},
    ]

    # Crear la tabla con ajuste de texto en varias líneas
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Edad", weight=ft.FontWeight.BOLD)),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    # Ajustar el texto en varias líneas
                    ft.DataCell(ft.Text(nombre["nombre"], width=200)),  # Ancho máximo para el texto
                    ft.DataCell(ft.Text(str(nombre["edad"]))),
                ]
            )
            for nombre in nombres_largos
        ],
        column_spacing=20,  # Espacio entre columnas
        width=600,  # Ancho total de la tabla
    )

    # Añadir la tabla a la página
    page.add(tabla)

ft.app(target=main)