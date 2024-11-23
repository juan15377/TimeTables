import sys

sys.path.append("src/")
sys.path.append("src/Logic/")




from Logic import BD
from Hours import *
from Subjects import *

BD = BD()

print(BD)

# ? Prueba de añadir un profesor nuevo
BD.professors.new("Juan de Jesus Venegas Flores")
BD.professors.new("Jose Manuel Gomez Soto")

# ? Prueba de añadir aula, y grupo

BD.classrooms.new("Aula 1")

# ? crear una carrera, semestre y un grupo 

BD.groups.careers.new("Ingenieria Informatica")
BD.groups.semesters.new("Semestre 2")
BD.groups.subgroups.new("Subgrupo 1")



carrera = BD.groups.careers.get()[0]
semestre = BD.groups.semesters.get()[0]
subgrupo = BD.groups.subgroups.get()[0]


BD.groups.new(carrera, semestre, subgrupo)

#print(len(BD.profesores.get()))

comp_horas = HoursComposition(1, 2, 5)

info = InfoSubject("Programacion Matematica", "PROGRA", BD.professors.get()[0], BD.classrooms.get()[0], [BD.groups.get()[0]], comp_horas)

BD.subjects.add(info)

print(BD.subjects.get()[0].hours_distribution.get_avaible_hours())

professor = BD.professors.get()[0]

subject = BD.subjects.get()[0]

#print(subject.assign_class_block((0, 0), 4))
#print(subject.availability_matrix)

#print(subject.availability_matrix)
#print(subject.hours_distribution.get_avaible_hours())