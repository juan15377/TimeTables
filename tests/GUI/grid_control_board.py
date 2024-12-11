from src.GUI.MainPage.TMaterias import initialize_control_board
import flet as ft 

def row_expansive():
    
    def container_expansive():
        return ft.Container(
            content = ft.Text("Juan de jesus"),
            bgcolor = ft.colors.RED,
            expand = True,

        )
    
    def column_expansive():
        return ft.ListView(
            controls = [container_expansive() for i in range(10)],
            expand = True,
            spacing=3
        )
    
    column = ft.Row(
        controls = [column_expansive() for i in range(7)],
    )
    
    return initialize_control_board()[1]

def main(page: ft.Page):
    page.add(row_expansive())



# Ejecutar la aplicación
ft.app(target=main)

