import flet as ft
from src.models.database import PCG

import flet as ft

import flet as ft

class MiniAvailableMatrix(ft.UserControl):
    def __init__(self, pcg):
        super().__init__()
        self.pcg = pcg
        self.initial_availability_matrix = pcg.initial_availability_matrix()
        self.availability_matrix = pcg.availability_matrix

    def build(self):
        pixel_size = 3  # Ancho de cada "píxel"
        row_size = 5    # Alto de cada "píxel"
        shapes = []

        for j in range(7):  # Filas
            for i in range(30):  # Columnas
                color = self.get_color(i, j)
                shapes.append(ft.canvas.Rect(
                    x=i * pixel_size,
                    y=j * row_size,
                    width=pixel_size,
                    height=row_size,
                    paint=ft.Paint(
                        style=ft.PaintingStyle.FILL,
                        color=color
                    )
                ))

        return ft.canvas.Canvas(
            shapes=shapes,
            width=30 * pixel_size,
            height=7 * row_size
        )

    def get_color(self, i, j):
        """Determina el color del píxel según las matrices de disponibilidad."""
        if self.initial_availability_matrix[i, j]:
            return "green" if self.availability_matrix[i, j] else "blue"
        return "red"

    def update(self):
        self.pcg = pcg
        self.initial_avilability_matrix = pcg.initial_availability_matrix()
        self.availability_matrix = pcg.availability_matrix
        
        def color(i, j):
            if self.initial_avilability_matrix[i, j]:
                if self.availability_matrix[i, j]:
                    return "green"
                return "blue"
            return "red"
            pass
            
        content = ft.ListView(
        controls=[
            ft.Row(
                [ft.Container(width=3, height=5, bgcolor=color(i, j)) for i in range(30)],
                spacing=0
            ) for j in range(7)
        ],
        spacing=0
        )
        

        
        for i in range(7):
            for j in range(30):
                self.controls[i].controls[j].bgcolor = self.color(i, j)
        self.controls[1].update()
        pass