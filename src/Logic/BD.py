
from pga import Profesores, Aulas, Grupos 
from Subjects import Subject


class BD():

    def __init__(self) -> None:
        #self.materias = Materias(self)
        self.profesores = Profesores(self)
        self.aulas = Aulas(self)
        self.grupos = Grupos(self)
        self.materias = Materias(self)
        pass