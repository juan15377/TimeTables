import flet as ft

class Alert():
    
    def __init__(self, alert : str, page):
        self.page = page
        self.alert = alert
        
        def show_alert():
            # Configurar el contenido del diálogo
            alert = ft.AlertDialog(
                title=ft.Text("¡Error!"),
                content=ft.Text(self.alert),
                actions=[
                    ft.TextButton("Aceptar", on_click= lambda e : self.close_alert()),
                    ft.TextButton("Cancelar", on_click= lambda e : self.close_alert()),
                ],
            )
            # Mostrar el diálogo
            page.dialog = alert
            alert.open = True
            page.update()

            def cerrar_alerta(e):
                # Cerrar el diálogo
                page.dialog.open = False
                page.update()

        self.show_alert = show_alert

    def show(self):
        self.show_alert()
        
    def close_alert(self):
        self.page.dialog.open = False
        self.page.update()