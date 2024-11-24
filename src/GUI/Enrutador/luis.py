import flet as ft
from PIL import Image
import cv2
import numpy as np
from io import BytesIO

class ImageCropper:
    def __init__(self, page):
        self.page = page
        self.image = None
        self.display_image = None
        self.rectangles = []
        self.start_x = self.start_y = None
        self.zoom_scale = 1.0

        # Layout principal
        self.canvas = ft.canvas(width=800, height=600, bgcolor=ft.colors.GREY)
        self.canvas.on_pointer_down = self.start_crop
        self.canvas.on_pointer_move = self.draw_rectangle
        self.canvas.on_pointer_up = self.save_rectangle
        self.canvas.on_wheel = self.zoom

        # Botones
        self.load_button = ft.ElevatedButton("Cargar Imagen", on_click=self.load_image)
        self.save_button = ft.ElevatedButton("Guardar Recortes", on_click=self.save_crops)

        self.page.add(ft.Column([
            self.canvas,
            ft.Row([self.load_button, self.save_button], alignment=ft.MainAxisAlignment.CENTER),
        ]))

    def load_image(self, e):
        file_picker = ft.FilePicker(on_result=self.file_picker_result)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(file_type=ft.FilePickerFileType.IMAGE)

    def file_picker_result(self, e):
        if not e.files:
            return

        file_path = e.files[0].path
        self.image = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
        self.zoom_scale = 1.0
        self.display_image_at_scale()

    def display_image_at_scale(self):
        if self.image is not None:
            # Redimensionar imagen según zoom
            height, width, _ = self.image.shape
            new_width = int(width * self.zoom_scale)
            new_height = int(height * self.zoom_scale)
            resized_image = cv2.resize(self.image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

            # Convertir la imagen a formato compatible con Flet
            pil_image = Image.fromarray(resized_image)
            img_buffer = BytesIO()
            pil_image.save(img_buffer, format="PNG")
            img_data = img_buffer.getvalue()

            self.canvas.controls.clear()
            self.canvas.controls.append(
                ft.Image(src_base64=img_data, width=800, height=600, fit=ft.ImageFit.CONTAIN)
            )
            self.page.update()

    def start_crop(self, e):
        if self.image is not None:
            self.start_x = e.local_x / self.zoom_scale
            self.start_y = e.local_y / self.zoom_scale

    def draw_rectangle(self, e):
        if self.image is not None and self.start_x is not None:
            self.canvas.controls.clear()
            self.display_image_at_scale()
            rect = ft.Rectangle(
                left=self.start_x * self.zoom_scale,
                top=self.start_y * self.zoom_scale,
                right=e.local_x,
                bottom=e.local_y,
                color=ft.colors.RED,
                stroke_width=2
            )
            self.canvas.controls.append(rect)
            self.page.update()

    def save_rectangle(self, e):
        if self.image is not None and self.start_x is not None:
            x1, y1 = int(self.start_x), int(self.start_y)
            x2, y2 = int(e.local_x / self.zoom_scale), int(e.local_y / self.zoom_scale)
            self.rectangles.append((x1, y1, x2, y2))
            self.start_x = self.start_y = None

    def save_crops(self, e):
        if not self.rectangles:
            self.page.snack_bar = ft.SnackBar(ft.Text("No hay recortes seleccionados."))
            self.page.snack_bar.open = True
            self.page.update()
            return

        for i, (x1, y1, x2, y2) in enumerate(self.rectangles):
            crop = self.image[y1:y2, x1:x2]
            cv2.imwrite(f"recorte_{i+1}.jpg", cv2.cvtColor(crop, cv2.COLOR_RGB2BGR))

        self.page.snack_bar = ft.SnackBar(ft.Text("Recortes guardados."))
        self.page.snack_bar.open = True
        self.page.update()

# Inicializar la aplicación
if __name__ == "__main__":
    ft.app(target=ImageCropper)
