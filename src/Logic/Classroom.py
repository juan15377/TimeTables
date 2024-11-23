#from Grupos import GestorGrupos
from keys import Key
from abc import ABC, abstractmethod
import numpy as np
import random as rn
from colores import MiColorRGB
#from Materia import Materia 

# ! La clase abstracta PGA es la superclase que tiene como subclases a profesor 
# ! Aula y Grupo, definiendo sus campos y metodos que comparten 
# al momento de que se cambia la disponibilidad de un pga, esta se actualizan 
# todas las materias que sean asociadas a este pga


class Metodos_1_PGA():

    def __init__(self, pga) -> None:
        self.pga = pga 

    def cambiar_disponibilidad(self, nueva_disponibilidad):
        self.pga.disponibilidad = nueva_disponibilidad
        for materia in self.pga.materias:
            materia.update_disponibilidad()
    def actualizar_disponibilidad_materias(self):
        for materia in self.pga.materias:
            materia.update_disponibilidad()

    def completado(self):
        total = 0
        faltantes = 0
        for materia in self.pga.materias:
            total += materia.composicion_horas.total()
            faltantes += materia.composicion_horas.faltantes()
        return 1 - faltantes/total if total != 0 else 1 



class ColoresMaterias():

    def __init__(self) -> None:
        self.color = {}

    def cambiar_color(self, materia, color):
        self.color[materia] = color

    def añadir_materia(self, materia):
        rojo = rn.randint(0,255)
        verde = rn.randint(0,255)
        azul = rn.randint(0,255)
        color = MiColorRGB(rojo, verde, azul)
        self.color[materia] = color
    def eliminar_materia(self, materia):
        del self.color[materia]
    
    


class PGA():

    def __init__(self) -> None:
        self.materias = []
        self.tablero = []
        self.key = Key()
        self.disponibilidad = np.full((30,7), True)
        self.m1 = Metodos_1_PGA(self)
        self.colores_materias = ColoresMaterias()

        pass

    def añadir_materia(self,materia):
        self.materias.append(materia)
        self.colores_materias.añadir_materia(materia)


    def eliminar_materia(self,materia):
        self.materias.remove(materia)
        self.colores_materias.eliminar_materia(materia)

    def get_materias(self):
        return self.materias



# ? Profesor

class Profesor(PGA):

    def __init__(self,nombre) -> None:
        super().__init__()
        self.nombre = nombre 


# ? Aula 

class Aula(PGA):
    
    def __init__(self,nombre) -> None:
        super().__init__()
        self.nombre = nombre 


# ? Para los Grupos el constructor es mas complejo, este requiere tres componenetes 
# ? Una Carrera asociada,Semestre y subgrupo, por lo que la creacion de Grupos se hara mediante 
# ? un Gestor de Grupos 


class Carrera():
    
    def __init__(self,nombre):
        
        self.nombre = nombre 
        self.key = Key()


class Semestre():
    
    def __init__(self,nombre):
        
        self.nombre = nombre 
        self.key = Key()

class Subgrupo():
    
    def __init__(self,nombre):
        
        self.nombre = nombre 
        self.key = Key()


class Grupo(PGA):

    def __init__(self,carrera:Carrera, semestre:Semestre, subgrupo:Subgrupo) -> None:

        super().__init__()

        self.carrera = carrera
        self.semestre = semestre
        self.subgrupo = subgrupo
    
    


class Carreras():

    def __init__(self) -> None:
        self.carreras = []
        pass

    def get(self):
        return self.carreras 
    
    def remove(self, carrera):
        self.carreras.remove(carrera)

    def new(self, nombre):
        carrera = Carrera(nombre)
        self.carreras.append(carrera)

    
class Semestres():

    def __init__(self) -> None:
        self.semestres = []
        pass

    def get(self):
        return self.semestres
    
    def remove(self, semestre):
        self.semestres.remove(semestre)

    def new(self, nombre):
        semestre = Semestre(nombre)
        self.semestres.append(semestre)
    

class Subgrupos():

    def __init__(self) -> None:
        self.subgrupos = []
        pass
    
    def get(self):
        return self.subgrupos 
    
    def remove(self, subgrupo):
        self.subgrupos.remove(subgrupo)

    def new(self, nombre):
        subgrupo = Subgrupo(nombre)
        self.subgrupos.append(subgrupo)


class Grupos():


    def __init__(self, BD) -> None:
        self.carreras = Carreras()
        self.semestres = Semestres()
        self.subgrupos = Subgrupos()
        self.grupos = []
        pass


    def new(self, carrera: Carrera, semestre: Semestre, subgrupo: Subgrupo):

        # en caso de que ya exista el grupo con la misma carrera,semestre y grupo no se crea un nuevo
        for grupo in self.grupos:
            if grupo.carrera == carrera and grupo.semestre == semestre and grupo.subgrupo == subgrupo:
                return None 

        grupo = Grupo(carrera,semestre,subgrupo)
        self.grupos.insert(0, grupo)

    def get(self):
        return self.grupos
    
    def remove(self, grupo):
        self.__grupos.remove(grupo)

    

class Profesores():

    def __init__(self, BD) -> None:
        self.profesores = []
        pass

    def new(self, nombre):
        profesor = Profesor(nombre)
        self.profesores.insert(0,profesor)

    def get(self):
        return self.profesores
    
    def remove(self, profesor):
        self.profesores.remove(profesor)


class Aulas():

    def __init__(self, BD) -> None:
        self.aulas = []
        pass

    def new(self, nombre):
        aula = Aula(nombre)
        self.aulas.insert(0, aula)

    def get(self):
        return self.aulas
    
    def remove(self, aula):
        self.aulas.remove(aula)



