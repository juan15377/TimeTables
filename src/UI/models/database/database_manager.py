
import sys


from .models.Subjects import Subjects
from .models.Professor_Classroom_Group import Professors, Classrooms, Groups

import sys 

from .components.export_functions import *

import pickle

import os
import subprocess

import pickle
import os

def save_in_pickle(objeto, ruta):
    """
    Guarda un objeto en un archivo pickle en la ruta especificada.

    :param objeto: El objeto a guardar.
    :param ruta: La ruta completa del archivo donde se guardará el objeto.
    """
    try:
        # Asegurarse de que el directorio existe
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        
        with open(ruta, 'wb') as archivo:
            pickle.dump(objeto, archivo)
        print(f"Objeto guardado en {ruta}")
    except Exception as e:
        print(f"Error al guardar el objeto: {e}")

class DataBaseManager():

    def __init__(self) -> None:
        self.professors = Professors(self)
        self.classrooms = Classrooms(self)
        self.groups = Groups(self)
        self.subjects = Subjects(self)
        self.export = ExportFunctionsLatex(self)
        pass

    def load_db(self, path_new_db):
        with open(path_new_db, "rb") as file:
            new_bd = pickle.load(file)
            self.professors = new_bd.professors
            self.classrooms = new_bd.classrooms
            self.groups = new_bd.groups
            self.subjects = new_bd.subjects
            self.subjects.BD = self    
    
    def save_db(self, path_save_db):
        save_in_pickle(self, path_save_db)

    def update_bd(self):
        pass
    
    def get_status_completed(self):
        sum_hours_total = 0
        sum_hours_restart = 0
        
        for subject in self.subjects.get():
            sum_hours_total += subject.hours_distribution.total
            sum_hours_remaining += subject.hours_distribution.remaining
        
        return 1 - sum_hours_remaining / sum_hours_total if sum_hours_total != 0 else 1 

