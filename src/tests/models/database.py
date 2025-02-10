from src.models.database import *

BD = DataBaseManager()

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

info = InfoSubject("Programacion Matematica", "PROGRA", BD.professors.get()[0], BD.classrooms.get()[0], [BD.groups.get()[0]], comp_horas, False)

BD.subjects.add(info)

print(BD.subjects.get()[0].hours_distribution.get_avaible_hours())

professor = BD.professors.get()[0]

subject = BD.subjects.get()[0]

#print(subject.assign_class_block((0, 0), 4))
#print(subject.availability_matrix)

#print(subject.availability_matrix)
#print(subject.hours_distribution.get_avaible_hours())

import numpy as np

professor = BD.professors.get()[0]
group = BD.groups.get()[0]
nueva_disponibilidad = np.full((30,7), False)

#profesor.M1.cambiar_disponibilidad(nueva_disponibilidad)
group.methods.change_availability_matrix(nueva_disponibilidad)
subject = BD.subjects.get()[0]


print(professor.subjects[0].availability_matrix)
print(professor)

# eliminar materia de la base de datos, esto tambien debe tener en que esto quita las horas puestas # de las materias, lo que debe descencadenar un cambio en la disponibilidad de las materias
subject = BD.subjects.get()[0]
print(len(group.subjects))

BD.subjects.remove(subject)

print(len(group.subjects))


# añadir_un bloque a una materia bajo su disponibilidad 
# - debe actualizar la disponibilidad de las materias

# eliminar_bloque de una materia bajo su disponibilidad 