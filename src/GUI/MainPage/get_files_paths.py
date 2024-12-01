import flet
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)
import flet as ft

import flet
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)

import pickle
import os

def save_object_to_pickle(obj, path):
    """
    Guarda un objeto en un archivo pickle en la ruta especificada.

    Parámetros:
    - obj: Objeto que se desea guardar.
    - path: Ruta completa del archivo, incluyendo el nombre y la extensión .pickle.
    """
    # Asegurarse de que la ruta al directorio exista
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Guardar el objeto usando pickle
    with open(path, "wb") as file:
        pickle.dump(obj, file)

    print(f"Objeto guardado exitosamente en {path}")

def save_data_base(page, bd):
    def save_file_result(e: FilePickerResultEvent):
        if e.path:
            save_object_to_pickle(bd, e.path)
            page.remove(save_file_dialog)
            print("Archivo guardado exitosamente")

    save_file_dialog = FilePicker(on_result=save_file_result)

    
    page.overlay.extend([save_file_dialog])

    page.add(save_file_dialog
    )
    
    save_file_dialog.save_file()


def load_data_base(page, db):
    
    def load_file_path(e: FilePickerResultEvent):
        if e.path:
            with open(e.path, "rb") as file:
                new_bd = pickle.load(file)
                db.professors = new_bd.professors
                db.classrooms = new_bd.classrooms
                db.groups = new_bd.groups
                db.subjects = new_bd.subjects
            page.remove(load_file_dialog)
                
    load_file_dialog = FilePicker(on_result=load_file_path)
    
    page.overlay.extend([load_file_dialog])
    
    page.add(load_file_dialog)
    
    load_file_dialog.load_file()



    
#on_result es una funcion que se ejecuta cuando el filepicker se cierra    

    
def main(page : ft.Page):
    
    def obtener_path(e):
        print(save_bd(page, 10))
    
    button_to_get = ft.TextButton(
        text="Pick files",
        on_click=obtener_path
    )
    
    page.add(button_to_get)


flet.app(target=main)