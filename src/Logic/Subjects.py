from Keys import Key
from functools import reduce
import numpy as np
from Hours import *
from Professor_Classroom_Group import Professor, Classroom, Group

class NameSubject():

    def __init__(self, name : str, code : str):
        self.name = name 
        self.code = code
        pass

class PGASubject():

    def __init__(self, professor: Professor, classrroom : Classroom, groups :list[Group]):
        self.professor = professor
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
    group_availability_matrices = [group.availability_matrix for group in groups]
    availability_matrix_for_groups = reduce(lambda m1, m2: m1 & m2, group_availability_matrices)
    availability_matrix_teacher = teacher.availability_matrix
    availability_matrix_classroom = classroom.availability_matrix

    avaibility_total = availability_matrix_for_groups & availability_matrix_teacher & availability_matrix_classroom

    return avaibility_total



def update_availability_subject(subject: Subject, position, length_hours, value = False):
    row = position[0]
    col = position[1]
    estandarized_length = int(length_hours)
    subject.professor.availability_matrix[row:row + estandarized_length, col] = value
    subject.classroom.availability_matrix[row:row + estandarized_length, col] = value
    for group in subject.groups:
        group.availability_matrix[row:row + estandarized_length, col] = value

    subject.professor.methods.update_subjects_availability_matrices()
    subject.classroom.methods.update_subjects_availability_matrices()
    for grupo in subject.groups:
        grupo.methods.update_subjects_availability_matrices()





class Subject():

    def __init__(self, name, code, professor, classroom, groups, hours_distribution) -> None:
        self.name = name 
        self.code = code 
        self.professor = professor
        self.classroom = classroom
        self.groups = groups
        self.hours_distribution = hours_distribution
        self.allocated_subject_matrix = np.full((30, 7), False) # Matrix

        self.availability_matrix = intersectAvailability(professor, classroom, groups)
        pass

    def update_availability_matrix(self):
        self.availability_matrix = intersectAvailability(self.professor, self.classroom, self.groups)
        pass

    def set_hours_distribution(self, new_hours_distribution):
        self.hours_distribution = new_hours_distribution
        self.allocated_subject_matrix = np.full((30, 7), False)
        self.update_availability_matrix()

    def restart(self):
        # se reinicia todas las horas colocadas 
        self.allocated_subject_matrix = np.full((30, 7), False)
        self.hours_distribution.restart()
        self.update_availability_matrix()

    def assign_class_block(self, position, hours_length_block):
        row = position[0]
        col = position[1]
        self.allocated_subject_matrix[row:int(hours_length_block),col] = True
        self.hours_distribution.add_block_hour(hours_length_block)
        # esto debe dessencadenar que el profesor, aula y sus grupos relacionados a esta materia 
        # deben actualizar su disponibilidad  
        update_availability_subject(self, position, hours_length_block)
        self. update_availability_matrix()

    def remove_class_block(self, position, hours_length_block):
        row = position[0]
        col = position[1]
        self.allocated_subject_matrix[row:int(hours_length_block*2),col] = False
        self.hours_distribution.remove_length_hour(hours_length_block)
        # esto debe dessencadenar que el profesor, aula y sus grupos relacionados a esta materia 
        # deben actualizar su disponibilidad  
        update_availability_subject(self, position, hours_length_block, True)
        self.update_availability_matrix()

    def total(self):
        return self.hours_distribution.total()
    
    def remaining(self):
        return self.hours_distribution.remaining()


def delete_subject_from_DB(subject):
    professor = subject.professor
    classroom = subject.classroom
    groups = subject.groups

    professor.remove_subject(subject)
    classroom.remove_subject(subject)
    for group in groups:
        group.remove_subject(subject)


class InfoSubject():
    
    def __init__(self, 
                 name, 
                 code, 
                 professor, 
                 classroom, 
                 groups, 
                 hours_distribution) -> None:
        
        self.name = name
        self.code = code
        self.professor = professor
        self.classroom = classroom
        self.groups = groups
        self.hours_distribution = hours_distribution
        
        pass

class Subjects:

    def __init__(self, DB) -> None:
        self.subjects = []
        self.DB = DB

    def add(self, subject_info):
        # This adds a new subject
        name = subject_info.name
        code = subject_info.code
        professor = subject_info.professor
        classroom = subject_info.classroom
        groups = subject_info.groups
        hours_distribution = subject_info.hours_distribution
        subject = Subject(name, code, professor, classroom, groups, hours_distribution)
        self.subjects.append(subject)

        professor.add_subject(subject)
        classroom.add_subject(subject)
        for group in groups:
            group.add_subject(subject)

    def remove(self, subject):
        self.subjects.remove(subject)

        # The subject must also be removed from the teacher, classrooms, and groups
        delete_subject_from_DB(subject)

    def get(self):
        return self.subjects
