from keys import Key
from functools import reduce
import numpy as np
from Hours import *

class NameSubject():

    def __init__(self, name : str, code : str):
        self.name = name 
        self.code = code
        pass

class PGASubject():

    def __init__(self, teacher : Teacher, classrroom : Classroom, groups :list[Group]):
        self.teacher = teacher
        self.classrroom = classrroom
        self.groups = groups
        pass


class Subject():

    def __init__(self, name_subject : NameSubject, pga_subject : PGASubject, composition_hours: WeeklyHoursDistribution) -> None:
        self.name_subject = name_subject
        self.pga_subject = pga_subject
        self.composition_hours = composition_hours
        pass


def intersectAvailability(teacher, classroom, groups):
    group_availability_matrices = [group.availabity_matrix for group in groups]
    availability_matrix_for_groups = reduce(lambda m1, m2: m1 & m2, group_availability_matrices)
    availability_matrix_teacher = teacher.avaibility_matrix
    availability_matrix_classroom = classroom.avaibility_matrix

    avaibility_total = availability_matrix_for_groups & availability_matrix_teacher & availability_matrix_classroom

    return avaibility_total

class Bloque_horas():

    def __init__(self, posicion, tamaño_horas) -> None:
        self.posicion = posicion
        self.tamaño_horas = tamaño_horas





def update_availability_subject(subject: Subject, position, length_hours, value = False):
    row = position[0]
    col = position[1]
    estandarized_length = int(length_hours)
    subject.teacher.availability_matrix[row:row + estandarized_length, col] = value
    subject.classroom.availability_matrix[row:row + estandarized_length, col] = value
    for group in subject.groups:
        group.availability_matrix[row:row + estandarized_length, col] = value

    subject.teacher.m1.update_availability_matrices_subjects()
    subject.classroom.m1.update_availability_matrices_subjects()
    for grupo in subject.groups:
        grupo.m1.update_availability_matrices_subjects()





class Subject():

    def __init__(self, name, code, teacher, classroom, groups, hours_distribution) -> None:
        self.name = name 
        self.code = code 
        self.teacher = teacher
        self.classroom = classroom
        self.groups = groups
        self.hours_distribution = hours_distribution
        self.allocated_subject_matrix = np.full((30, 7), False) # Matrix

        self.availability_matrix = intersectAvailability(teacher, classroom, groups)
        pass

    def update_availability_matrix(self):
        self.disponibilidad = intersectAvailability(self.profesor, self.aula, self.grupos)
        pass

    def set_hours_distribution(self, new_hours_distribution):
        self.hours_distribution = new_hours_distribution
        self.allocated_subject_matrix = np.full((30, 7), False)
        self.update_availability_matrix()

    def restart(self):
        # se reinicia todas las horas colocadas 
        self.allocated_subject_matrix = np.full((30, 7), False)
        self.hours_distribution.reiniciar()
        self.update_availability_matrix()

    def assign_class_block(self, position, hours_length_block):
        row = position[0]
        col = position[1]
        self.allocated_subject_matrix[row:int(hours_length_block),col] = True
        self.hours_distribution.add_block_hour(hours_length_block)
        # esto debe dessencadenar que el profesor, aula y sus grupos relacionados a esta materia 
        # deben actualizar su disponibilidad  
        update_availability_subject(self, position, hours_length_block)
        self.update_disponibilidad()

    def remove_class_block(self, position, hours_length_block):
        row = position[0]
        col = position[1]
        self.allocated_subject_matrix[row:int(hours_length_block*2),col] = False
        self.hours_distribution.eliminar_bloque(hours_length_block)
        # esto debe dessencadenar que el profesor, aula y sus grupos relacionados a esta materia 
        # deben actualizar su disponibilidad  
        update_availability_subject(self, position, hours_length_block, True)
        self.update_disponibilidad()

    def total(self):
        return self.hours_distribution.total()
    
    def remaining(self):
        return self.hours_distribution.remaining()




def eliminar_materia_BD(materia):
    profesor = materia.profesor
    aula = materia.aula
    grupos = materia.grupos

    profesor.eliminar_materia(materia)
    aula.eliminar_materia(materia)
    for grupo in grupos:
        grupo.eliminar_materia(materia)


class Subjects():

    def __init__(self, BD) -> None:
        self.subjects = []
        self.BD = BD

    def add(self, subject_info):
        # This adds a new subject
        name = subject_info.name
        code = subject_info.code
        teacher = subject_info.teacher
        classroom = subject_info.classroom
        groups = subject_info.groups
        hours_distribution = subject_info.hours_distribution
        subject = Subject(name, code, teacher, classroom, groups, hours_distribution)
        self.subjects.append(subject)

        teacher.add_subject(subject)
        classroom.add_subject(subject)
        for group in groups:
            group.add_subject(subject)

    def remove(self, subject):
        self.subjects.remove(subject)

        # The subject must also be removed from the teacher, classrooms, and groups
        delete_subject_from_BD(subject)
        # teacher = subject.teacher
        # classroom = subject.classroom
        # groups = subject.groups
        # teacher.remove_subject(subject)
        # classroom.remove_subject(subject)
        # for group in groups:
        #     group.remove_subject(subject)

    def get(self):
        return self.subjects
