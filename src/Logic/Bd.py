
import sys


from .Subjects import Subjects
from .Professor_Classroom_Group import Professors, Classrooms, Groups

import sys 

from .schedule_printer import *

import pickle

import os
import subprocess

def save_latex_to_file_and_compile(latex_content, file_path):
    """
    Guarda el contenido LaTeX en un archivo .tex con la ruta especificada,
    genera un PDF y elimina los archivos temporales generados durante la compilación.
    
    Args:
        latex_content (str): Contenido del documento LaTeX.
        file_path (str): Ruta completa para guardar el archivo .tex, 
                         incluyendo el nombre base (sin extensión .tex o .pdf).
    """
    # Verificar y crear el directorio si no existe
    save_path = os.path.dirname(file_path)
    os.makedirs(save_path, exist_ok=True)

    # Agregar la extensión .tex al archivo si no está incluida
    if not file_path.endswith(".tex"):
        file_path += ".tex"

    # Extraer el nombre base del archivo (sin ruta ni extensión)
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Guardar el contenido LaTeX en el archivo .tex
    with open(file_path, "w") as f:
        f.write(latex_content)

    # Cambiar al directorio de salida antes de compilar el PDF
    original_directory = os.getcwd()
    os.chdir(save_path)

    try:
        # Ejecutar pdflatex para compilar el archivo .tex a PDF
        result = subprocess.run(['pdflatex', file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = subprocess.run(['pdflatex', file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Verificar si la compilación fue exitosa
    finally:
        # Eliminar archivos temporales generados por pdflatex
        latex_files = [f'{file_name}.aux', f'{file_name}.log', f'{file_name}.out', f'{file_name}.toc', f'{file_name}.fls', f'{file_name}.synctex.gz']
        for file in latex_files:
            file_path_temp = os.path.join(save_path, file)
            if os.path.exists(file_path_temp):
                os.remove(file_path_temp)

        os.chdir(original_directory)  # Restaurar el directorio original



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


def save_data_base(page, bd):
    def save_file_result(e: FilePickerResultEvent):
        if e.path:
            save_object_to_pickle(bd, e.path)
            page.remove(save_file_dialog)

    save_file_dialog = FilePicker(on_result=save_file_result)

    
    page.overlay.extend([save_file_dialog])

    page.add(save_file_dialog
    )
    
    save_file_dialog.pick_files()


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
    
    load_file_dialog.pick_files()
    



def generate_pdf_latex(page, bd):
    def save_file_result(e: FilePickerResultEvent):
        if e.path:
            schedule_latex = ScheduleLatex(bd)
            latex_content = schedule_latex.compile_to_latex()
            save_latex_to_file_and_compile(latex_content, e.path)
            page.remove(save_file_dialog)

    save_file_dialog = FilePicker(on_result=save_file_result)

    
    page.overlay.extend([save_file_dialog])

    page.add(save_file_dialog
    )
    
    save_file_dialog.save_file()

class BD():

    def __init__(self) -> None:
        self.professors = Professors(self)
        self.classrooms = Classrooms(self)
        self.groups = Groups(self)
        self.subjects = Subjects(self)
        pass
    
    def generate_pdf(self, path_save):
        schedule_latex = ScheduleLatex(self)
        latex_content = schedule_latex.compile_to_latex()
        save_latex_to_file_and_compile(latex_content, path_save)

        
    def load_db(self, path_new_db):
        with open(path_new_db, "rb") as file:
            new_bd = pickle.load(file)
            self.professors = new_bd.professors
            self.classrooms = new_bd.classrooms
            self.groups = new_bd.groups
            self.subjects = new_bd.subjects
            self.subjects.BD = self
        
        
    
    def save_db(self, path_save_db):
        save_object_to_pickle(self, path_save_db)

    def update_bd(self):
        pass
    
    
    def get_status_completed(self):
        sum_hours_total = 0
        sum_hours_restart = 0
        
        for subject in self.subjects.get():
            sum_hours_total += subject.hours_distribution.total
            sum_hours_remaining += subject.hours_distribution.remaining
        
        return 1 - sum_hours_remaining / sum_hours_total if sum_hours_total != 0 else 1 
    

    

