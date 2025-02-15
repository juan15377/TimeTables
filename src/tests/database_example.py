from src.models.database import DataBaseManager 
from src.models.database import *


database_example = DataBaseManager()




# ? Prueba de añadir un profesor nuevo
database_example.professors.new("Juan de Jesus Venegas Flores")
database_example.professors.new("Jose Manuel Gomez Soto")

# ? Prueba de añadir aula, y grupo

database_example.classrooms.new("Aula 1")

# ? crear una carrera, semestre y un grupo 

database_example.groups.careers.new("Ingenieria Informatica")
database_example.groups.semesters.new("Semestre 2")
database_example.groups.subgroups.new("Subgrupo 1")


carrera =  database_example.groups.careers.get()[0]
semestre = database_example.groups.semesters.get()[0]
subgrupo = database_example.groups.subgroups.get()[0]


database_example.groups.new(carrera, semestre, subgrupo)

#print(len(BD.profesores.get()))

comp_horas = HoursComposition(1, 2, 5)

info = InfoSubject("Programacion Matematica", "PROGRA", database_example.professors.get()[0], database_example.classrooms.get()[0], [database_example.groups.get()[0]], comp_horas, False)

database_example.subjects.add(info)

professor = database_example.professors.get()[0]

subject = database_example.subjects.get()[0]

