
import sys

sys.path.append("src/Logic/")

from Subjects import Subjects
from Professor_Classroom_Group import Professors, Classrooms, Groups

import sys 

sys.path.append("src/Logic/schedule_printer/")
from schedule_latex import *

import pickle


import pickle
import os

def save_object_to_pickle(obj, path, filename):
    """
    Guarda un objeto en un archivo pickle en la ruta especificada.

    Parámetros:
    - obj: Objeto que se desea guardar.
    - path: Ruta donde se almacenará el archivo.
    - filename: Nombre del archivo (sin extensión .pickle).
    """
    # Asegurarse de que la ruta exista
    os.makedirs(path, exist_ok=True)

    # Crear la ruta completa con el nombre del archivo
    full_path = os.path.join(path, f"{filename}.pickle")

    # Guardar el objeto usando pickle
    with open(full_path, "wb") as file:
        pickle.dump(obj, file)

    print(f"Objeto guardado exitosamente en {full_path}")


class BD():

    def __init__(self) -> None:
        self.professors = Professors(self)
        self.classrooms = Classrooms(self)
        self.groups = Groups(self)
        self.subjects = Subjects(self)
        pass
    
    def generate_pdf(self, save_path, file_name):
        
        schedule_latex = ScheduleLatex(self)
        schedule_latex.compile_to_latex(save_path, file_name)
        
    def load_db(self, file_path):
        with open(file_path, 'rb') as file:
            new_bd = pickle.load(file)
            self.professors = new_bd.professors
            self.classrooms = new_bd.classrooms
            self.groups = new_bd.groups
            self.subjects = new_bd.subjects
            
            
    def save_db(self, file_path, name_file):
        save_object_to_pickle(self, file_path, name_file)

    def update_bd(self):
        pass

