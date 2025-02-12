
import sys


from .models import *
from .models import Professors, Classrooms, Groups, InfoSubject
from .components.export_functions import *


import pickle

import os
import subprocess


class DataBaseManager:
    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):  # Evitar reinicializar en cada llamada
            self.professors = Professors(self)
            self.classrooms = Classrooms(self)
            self.groups = Groups(self)
            self.subjects = Subjects(self)
            self.export = ExportFunctionsLatex(self)
            self._initialized = True  # Marcar como inicializada

    def load(self, path_new_db):
        with open(path_new_db, "rb") as file:
            new_bd = pickle.load(file)
            self.professors = new_bd.professors
            self.classrooms = new_bd.classrooms
            self.groups = new_bd.groups
            self.subjects = new_bd.subjects
            self.subjects.BD = self    
    
    def save(self, path_save_db):
        save_object_to_pickle(self, path_save_db)

    def update(self):
        pass
    
    def get_status_completed(self):
        sum_hours_total = 0
        sum_hours_remaining = 0
        
        for subject in self.subjects.get():
            sum_hours_total += subject.hours_distribution.total
            sum_hours_remaining += subject.hours_distribution.remaining
        
        return 1 - sum_hours_remaining / sum_hours_total if sum_hours_total != 0 else 1
