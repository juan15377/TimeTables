# vamos a recrear un ejemplo donde se ponga a ejemplo 
# 3 profesores 
# 3 aulas
# 5 materias 
# 3 grupos 
import sys  
from src.Logic.Bd import BD
sys.path.append("src/Logic/")
# agregar un bloque en una materia de una materia y ver si se propagan las disponibilidades de las materias

from Bd import BD
from Subjects import InfoSubject, HoursComposition,  HoursSlotsComposition
Bd = BD()

# ? Añadir 3 profesores

Bd.professors.new("Juan de Jesus Venegas Flores")
Bd.professors.new("Jose Manuel Gomez Soto")
Bd.professors.new("Maria de los Angeles Perez")

# ? Añadir 3 aulas

Bd.classrooms.new("Aula 1")
Bd.classrooms.new("Aula 2")
Bd.classrooms.new("Aula 3")

# ? crear 1 carrera, 3 semestres y 3 subgrupos 

Bd.groups.careers.new("Ingenieria Informatica")
Bd.groups.semesters.new("Semestre 1")
Bd.groups.semesters.new("Semestre 2")
Bd.groups.semesters.new("Semestre 3")

Bd.groups.subgroups.new("Subgrupo 1")
Bd.groups.subgroups.new("Subgrupo 2")
Bd.groups.subgroups.new("Subgrupo 3")

# ? crear 3 Grupos 

for i in range(3):
    Bd.groups.new(Bd.groups.careers.get()[0], Bd.groups.semesters.get()[i], Bd.groups.subgroups.get()[i])

# ? Crear 3 materias

comp_horas = HoursComposition(1, 2, 5)



comp_horas = HoursComposition(0.5, 2, 5)
info3 = InfoSubject("Calculo Diferencial", "CALC1", Bd.professors.get()[0], Bd.classrooms.get()[1], [Bd.groups.get()[2]], comp_horas)
Bd.subjects.add(info3)

comp_horas = HoursComposition(0.5, 2, 5)
info3 = InfoSubject("Algebra Lineal", "ALGLI", Bd.professors.get()[0], Bd.classrooms.get()[2], [Bd.groups.get()[0]], comp_horas)
Bd.subjects.add(info3)


comp_horas = HoursComposition(0.5, 2, 5)
info3 = InfoSubject("Algebra Lineal", "ALGLI", Bd.professors.get()[0], Bd.classrooms.get()[2], [Bd.groups.get()[0]], comp_horas)
Bd.subjects.add(info3)

comp_horas = HoursComposition(0.5, 2, 5)
info3 = InfoSubject("Algebra Lineal", "ALGLI", Bd.professors.get()[0], Bd.classrooms.get()[2], [Bd.groups.get()[0]], comp_horas)
Bd.subjects.add(info3)

comp_horas = HoursComposition(0.5, 2, 5)
info3 = InfoSubject("Algebra Lineal", "ALGLI", Bd.professors.get()[0], Bd.classrooms.get()[2], [Bd.groups.get()[0]], comp_horas)
Bd.subjects.add(info3)

comp_horas = HoursComposition(0.5, 2, 5)
info3 = InfoSubject("Algebra Lineal", "ALGLI", Bd.professors.get()[0], Bd.classrooms.get()[2], [Bd.groups.get()[0]], comp_horas)
Bd.subjects.add(info3)

comp_horas = HoursComposition(0.5, 2, 5)
info3 = InfoSubject("Algebra Lineal", "ALGLI", Bd.professors.get()[0], Bd.classrooms.get()[2], [Bd.groups.get()[0]], comp_horas)
Bd.subjects.add(info3)

comp_horas = HoursComposition(0.5, 2, 5)
info3 = InfoSubject("Algebra Lineal", "ALGLI", Bd.professors.get()[0], Bd.classrooms.get()[2], [Bd.groups.get()[0]], comp_horas)
Bd.subjects.add(info3)

comp_horas = HoursComposition(0.5, 2, 5)
info3 = InfoSubject("Algebra Lineal", "ALGLI", Bd.professors.get()[0], Bd.classrooms.get()[2], [Bd.groups.get()[0]], comp_horas)
Bd.subjects.add(info3)

comp_horas = HoursComposition(0.5, 2, 5)
info3 = InfoSubject("Algebra Lineal", "ALGLI", Bd.professors.get()[0], Bd.classrooms.get()[2], [Bd.groups.get()[0]], comp_horas)
Bd.subjects.add(info3)

comp_horas = HoursComposition(0.5, 2, 5)
info3 = InfoSubject("Algebra Lineal", "ALGLI", Bd.professors.get()[0], Bd.classrooms.get()[2], [Bd.groups.get()[0]], comp_horas)
Bd.subjects.add(info3)

comp_horas = HoursComposition(0.5, 2, 5)
info3 = InfoSubject("Algebra Lineal", "ALGLI", Bd.professors.get()[0], Bd.classrooms.get()[2], [Bd.groups.get()[0]], comp_horas)
Bd.subjects.add(info3)


Bd.subjects.remove(Bd.subjects.get())[0]

#comp_horas = HoursComposition(1, 2, 5)
#info3 = InfoSubject("Algebra Lineal", "ALGE", Bd.professors.get()[1], Bd.classrooms.get()[2], [Bd.groups.get()[2]], comp_horas)
#Bd.subjects.add(info3)
#
#comp_horas = HoursComposition(1, 2, 5)
#info3 = InfoSubject("Algebra Lineal", "ALGE", Bd.professors.get()[1], Bd.classrooms.get()[0], [Bd.groups.get()[0]], comp_horas)
#Bd.subjects.add(info3)
#comp_horas = HoursComposition(1, 2, 5)
#info3 = InfoSubject("Algebra Lineal", "ALGE", Bd.professors.get()[1], Bd.classrooms.get()[2], [Bd.groups.get()[2]], comp_horas)
#Bd.subjects.add(info3)
#comp_horas = HoursComposition(1, 2, 5)
#info3 = InfoSubject("Algebra Lineal", "ALGE", Bd.professors.get()[0], Bd.classrooms.get()[2], [Bd.groups.get()[1]], comp_horas)
#Bd.subjects.add(info3)
#comp_horas = HoursComposition(1, 2, 5)
#info3 = InfoSubject("Algebra Lineal", "ALGE", Bd.professors.get()[1], Bd.classrooms.get()[2], [Bd.groups.get()[2]], comp_horas)
#Bd.subjects.add(info3)
#
# añadimos 1 bloque a la primera materia 


#BD.materias.get()[0].colocar_horas((0, 4), 1)
materia_1 = Bd.subjects.get()[0]
materia_2 = Bd.subjects.get()[1]
#materia_3 = Bd.subjects.get()[2]

#materia_3.assign_class_block((5,4), 5)
materia_1.assign_class_block((27,1), 3)
#materia_2.assign_class_block((1,2), 5)

# print(materia_1.disponibilidad, "\n")
# print(materia_2.disponibilidad, "\n")
# print(materia_3.disponibilidad)

print(len(Bd.groups.get()[0].get_subjects()))
print(len(Bd.classrooms.get()[0].get_subjects()))

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
