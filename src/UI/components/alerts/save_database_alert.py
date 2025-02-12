import flet as ft 

class Data:
    def __init__(self) -> None:
        self.counter = 0


class DatabaseSaveAlert():
    """
    Alerta para mostrar cuando se guardan cambios en la base de datos.
    """
    def __init__(self, page, save_path):
        d = Data()
        page.snack_bar = ft.SnackBar(
        content=ft.Text("New Subject Created"),
        action="Alright!",
        )
    
        
        def on_click():
            page.snack_bar = ft.SnackBar(ft.Text(f"save changes in {save_path}"),
                                         bgcolor=ft.colors.GREEN_200)
            page.snack_bar.open = True
            d.counter += 1
            page.update()
        
        self.show = lambda : on_click()

