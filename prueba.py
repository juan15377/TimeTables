import flet as ft

def main(page: ft.Page):
    # Configuración de la página
    page.title = "Horario Semanal"
    page.window_width = 1000
    page.window_height = 600
    page.padding = 20

    # Definir las horas del día (de 7:00 a 22:00 en saltos de 30 minutos)
    horas = [f"{h:02d}:{m:02d}" for h in range(7, 22) for m in [0, 30]]

    # Definir los días de la semana
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    # Definir algunas materias con colores y códigos
    materias = [
        {"nombre": "Matemáticas", "codigo": "MAT101", "color": "#FFCCCB"},  # Rojo claro
        {"nombre": "Física", "codigo": "FIS201", "color": "#ADD8E6"},       # Azul claro
        {"nombre": "Química", "codigo": "QUI301", "color": "#90EE90"},      # Verde claro
        {"nombre": "Historia", "codigo": "HIS401", "color": "#FFD700"},     # Amarillo
    ]

    # Crear las columnas de la tabla
    columnas = [ft.DataColumn(ft.Text(dia, weight="bold")) for dia in dias]

    # Crear las filas de la tabla
    filas = []
    for hora in horas:
        celdas = [ft.DataCell(ft.Text("")) for _ in dias]  # Celdas vacías inicialmente
        filas.append(ft.DataRow(cells=celdas))

    # Función para agregar una materia en un bloque de tiempo
    def agregar_materia(dia, hora_inicio, duracion, materia):
        """
        Agrega una materia en un bloque de tiempo continuo.
        
        Parámetros:
            dia: Índice del día (0 = Lunes, 1 = Martes, etc.).
            hora_inicio: Índice de la hora de inicio en la lista `horas`.
            duracion: Duración en intervalos de 30 minutos.
            materia: Diccionario con la información de la materia.
        """
        # Crear un contenedor que ocupe varias filas
        contenedor_multifila = ft.Container(
            content=ft.Column(
                [
                    ft.Text(materia["codigo"], weight="bold"),
                    ft.Text(materia["nombre"], size=12),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand = True
            ),
            bgcolor=materia["color"],
            border_radius=5,
            expand=True,  # Expande el contenedor para ocupar todo el espacio
        )

        # Asignar el contenedor a la primera celda del bloque
        filas[hora_inicio].cells[dia] = ft.DataCell(contenedor_multifila)

        # Vaciar las celdas restantes del bloque
        for i in range(hora_inicio + 1, hora_inicio + duracion):
            filas[i].cells[dia] = ft.DataCell(ft.Container())  # Celda vacía

    # Agregar materias al horario
    agregar_materia(0, 0, 3, materias[0])  # Matemáticas el Lunes de 7:00 a 8:30 (3 intervalos)
    agregar_materia(2, 6, 4, materias[1])  # Física el Miércoles de 10:00 a 11:30 (4 intervalos)
    agregar_materia(4, 14, 4, materias[2])  # Química el Viernes de 14:00 a 15:30 (4 intervalos)
    agregar_materia(5, 18, 4, materias[3])  # Historia el Sábado de 16:00 a 17:30 (4 intervalos)

    # Crear la tabla
    tabla = ft.DataTable(
        columns=[ft.DataColumn(ft.Text("Hora", weight="bold"))] + columnas,
        rows=[
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(hora, weight="bold"))] + fila.cells
            )
            for hora, fila in zip(horas, filas)
        ],
        border=ft.border.all(1, "black"),
        border_radius=10,
        horizontal_lines=ft.border.BorderSide(1, "gray"),
        vertical_lines=ft.border.BorderSide(1, "gray"),
    )

    # Añadir la tabla a un contenedor con scroll
    scroll_container = ft.ListView(
        controls=[tabla],
        expand=True,
    )

    # Añadir el contenedor a la página
    page.add(scroll_container)

# Ejecutar la aplicación
ft.app(target=main)