
import sys


from .Subjects import Subjects
from .Professor_Classroom_Group import Professors, Classrooms, Groups

import sys 

from .schedule_printer import *

import pickle


import pickle
import os

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
        if result.returncode == 0:
            print(f"PDF generado exitosamente en: {os.path.join(save_path, f'{file_name}.pdf')}")
        else:
            print("Hubo un error durante la compilación de LaTeX:")
            print(result.stderr.decode())  # Mostrar el error si la compilación falla
    finally:
        # Eliminar archivos temporales generados por pdflatex
        latex_files = [f'{file_name}.aux', f'{file_name}.log', f'{file_name}.out', f'{file_name}.toc', f'{file_name}.fls', f'{file_name}.synctex.gz']
        for file in latex_files:
            file_path_temp = os.path.join(save_path, file)
            if os.path.exists(file_path_temp):
                os.remove(file_path_temp)
                print(f"Archivo temporal eliminado: {file_path_temp}")

        os.chdir(original_directory)  # Restaurar el directorio original

    print(f"Archivo .tex guardado en: {file_path}")


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

class BD():

    def __init__(self) -> None:
        self.professors = Professors(self)
        self.classrooms = Classrooms(self)
        self.groups = Groups(self)
        self.subjects = Subjects(self)
        pass
    
    def generate_pdf(self, save_path):
        
        schedule_latex = ScheduleLatex(self)
        latex_content = schedule_latex.compile_to_latex()
        save_latex_to_file_and_compile(latex_content, save_path)
        
    def load_db(self, file_path):
        with open(file_path, 'rb') as file:
            new_bd = pickle.load(file)
            self.professors = new_bd.professors
            self.classrooms = new_bd.classrooms
            self.groups = new_bd.groups
            self.subjects = new_bd.subjects
            
            
    def save_db(self, save_path):
        save_object_to_pickle(self, save_path)

    def update_bd(self):
        pass

