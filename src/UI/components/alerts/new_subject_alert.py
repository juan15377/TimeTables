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

class Data:
    def __init__(self) -> None:
        self.counter = 0

class AlertNewSubject():
    """
    Alerta para mostrar cuando se crea una nueva materia en la base de datos
    """
    def __init__(self, page):
        d = Data()
        page.snack_bar = ft.SnackBar(
        content=ft.Text("New Subject Created"),
        action="Alright!",
        )
    
        
        def on_click():
            page.snack_bar = ft.SnackBar(ft.Text(f"New Subject Created"),
                                         bgcolor=ft.colors.GREEN_200)
            page.snack_bar.open = True
            d.counter += 1
            page.update()
        
        self.show = lambda : on_click()
        
