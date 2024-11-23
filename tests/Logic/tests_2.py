# Prueba de cambio de disponibilidad 
from test import BD
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