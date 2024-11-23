# vamos a recrear un ejemplo donde se ponga a ejemplo 
# 3 profesores 
# 3 aulas
# 5 materias 
# 3 grupos 
import sys  

sys.path.append("src/Logic/")
# agregar un bloque en una materia de una materia y ver si se propagan las disponibilidades de las materias

from BD import BD
from Subjects import InfoSubject, HoursComposition,  HoursSlotsComposition
BD = BD()

# ? Añadir 3 profesores

BD.professors.new("Juan de Jesus Venegas Flores")
BD.professors.new("Jose Manuel Gomez Soto")
BD.professors.new("Maria de los Angeles Perez")

# ? Añadir 3 aulas

BD.classrooms.new("Aula 1")
BD.classrooms.new("Aula 2")
BD.classrooms.new("Aula 3")

# ? crear 1 carrera, 3 semestres y 3 subgrupos 

BD.groups.careers.new("Ingenieria Informatica")
BD.groups.semesters.new("Semestre 1")
BD.groups.semesters.new("Semestre 2")
BD.groups.semesters.new("Semestre 3")

BD.groups.subgroups.new("Subgrupo 1")
BD.groups.subgroups.new("Subgrupo 2")
BD.groups.subgroups.new("Subgrupo 3")

# ? crear 3 Grupos 

for i in range(3):
    BD.groups.new(BD.groups.careers.get()[0], BD.groups.semesters.get()[i], BD.groups.subgroups.get()[i])

# ? Crear 3 materias

comp_horas = HoursComposition(1, 2, 5)

info1 = InfoSubject("Programacion Matematica", "PROGRA", BD.professors.get()[0], BD.classrooms.get()[0], [BD.classrooms.get()[0]], comp_horas)
BD.subjects.add(info1)

comp_horas = HoursComposition(1, 2, 5)
info2 = InfoSubject("Calculo Diferencial", "CALC", BD.professors.get()[0], BD.classrooms.get()[1], [BD.classrooms.get()[1]], comp_horas)
BD.subjects.add(info2)

comp_horas = HoursComposition(1, 2, 5)
info3 = InfoSubject("Algebra Lineal", "ALGE", BD.professors.get()[1], BD.classrooms.get()[2], [BD.classrooms.get()[2]], comp_horas)
BD.subjects.add(info3)

# añadimos 1 bloque a la primera materia 


#BD.materias.get()[0].colocar_horas((0, 4), 1)
materia_1 = BD.subjects.get()[0]
materia_2 = BD.subjects.get()[1]
materia_3 = BD.subjects.get()[2]

# print(materia_1.disponibilidad, "\n")
# print(materia_2.disponibilidad, "\n")
# print(materia_3.disponibilidad)


# el colocar horas el la primera materia deberia propagar la disponibilidad en la tercer materia 
# al parecer funciona bien la propagacion de la disponibilidad a las materias 

#BD.materias.get()[0].eliminar_horas((0, 4), 1)

# print(materia_1.disponibilidad, "\n")
# print(materia_2.disponibilidad, "\n")
# print(materia_3.disponibilidad)

# print(materia_1.horas_colocadas)

# profesor_juan = BD.profesores.get()[0]

# print(profesor_juan.colores_materias.color[materia_1])

# sum([False, True])
