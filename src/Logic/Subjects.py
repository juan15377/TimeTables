from .Keys import Key
from functools import reduce
import numpy as np
from .Hours import *
from .Professor_Classroom_Group import Professor, Classroom, Group, DEFAULT_PCG
from .Colors import MyColorRGB
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


def intersectAvailability(teacher, classroom, groups):
    if teacher == None or classroom == None or groups == []:
        return None
    group_availability_matrices = [group.availability_matrix for group in groups]
    availability_matrix_for_groups = reduce(lambda m1, m2: m1 & m2, group_availability_matrices)
    if not (classroom == None):
        availability_matrix_teacher = teacher.availability_matrix
    else:
        availability_matrix_teacher = np.ones((len(teacher.availability_matrix), len(teacher.availability_matrix[0])), dtype=bool)
    availability_matrix_classroom = classroom.availability_matrix

    avaibility_total = availability_matrix_for_groups & availability_matrix_teacher & availability_matrix_classroom

    return avaibility_total



def update_availability_subject(subject, position, length_hours, value = False):
    row = position[0]
    col = position[1]
    estandarized_length = int(length_hours)
    subject.professor.availability_matrix[row:row + estandarized_length, col] = value
    if not subject.online:
        subject.classroom.availability_matrix[row:row + estandarized_length, col] = value
    for group in subject.groups:
        group.availability_matrix[row:row + estandarized_length, col] = value

    subject.professor.methods.update_subjects_availability_matrices()
    if not subject.online:
        subject.classroom.methods.update_subjects_availability_matrices()
    for grupo in subject.groups:
        grupo.methods.update_subjects_availability_matrices()



class ClassroomOnline():
    name = "Online"
    availability_matrix = np.ones((30,7), dtype =  bool)
    


class Subject():

    def __init__(self, name, code, professor, classroom, groups, hours_distribution, is_online = False) -> None:
        
        if is_online:
            classroom = ClassroomOnline()
        
        self.name = name 
        self.code = code 
        self.professor = professor
        self.classroom = classroom
        self.online = is_online
        self.groups = groups
        self.hours_distribution = hours_distribution
        self.allocated_subject_matrix = np.full((30, 7), False) # Matrix
        

        self.availability_matrix = intersectAvailability(professor, classroom, groups)
        pass

    def update_availability_matrix(self):
        self.availability_matrix = intersectAvailability(self.professor, 
                                                         self.classroom, 
                                                         self.groups)
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
        self.allocated_subject_matrix[row:row + int(hours_length_block),col] = True
        self.hours_distribution.add_block_hour(hours_length_block)
        # esto debe dessencadenar que el profesor, aula y sus grupos relacionados a esta materia 
        # deben actualizar su disponibilidad  
        update_availability_subject(self, position, hours_length_block)
        self. update_availability_matrix()

    def remove_class_block(self, position, hours_length_block):
        row = position[0]
        col = position[1]
        self.allocated_subject_matrix[row:row+int(hours_length_block),col] = False
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

    # interceptamos donde se coloco la materia 
    # y la matriz de disponibilidad de cada uno y asi 
    # podemos deja como esta su disponibilidad
    
    professor.availability_matrix = np.logical_or(professor.availability_matrix, subject.allocated_subject_matrix)
    classroom.availability_matrix = np.logical_or(classroom.availability_matrix,  subject.allocated_subject_matrix)
    
    for group in groups:
        group.availability_matrix = np.logical_or(group.availability_matrix, subject.allocated_subject_matrix)
    
    professor.remove_subject(subject)
    if not type(classroom) == ClassroomOnline:
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
                 hours_distribution,
                 is_online) -> None:
        
        self.name = name
        self.code = code
        self.professor = professor
        self.classroom = classroom
        self.groups = groups
        self.hours_distribution = hours_distribution
        self.is_online = is_online
        
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
        is_online = subject_info.is_online
        subject = Subject(name, code, professor, classroom, groups, hours_distribution, is_online = is_online)
        self.subjects.append(subject)

        professor.add_subject(subject)
        if not is_online:
            classroom.add_subject(subject)
        for group in groups:
            group.add_subject(subject)


    def remove(self, subject):
        if subject in self.subjects:
            self.subjects.remove(subject)

        # The subject must also be removed from the teacher, classrooms, and groups
        delete_subject_from_DB(subject)

    def get(self):
        return self._subjects



DEFAULT_SUBJECT = Subject(
    "",
    "",
    None,
    None,
    [],
    HoursComposition(30, 30, 30),
)

DEFAULT_PCG.subjects.append(DEFAULT_SUBJECT)
DEFAULT_PCG.subject_colors.colors[DEFAULT_SUBJECT] = MyColorRGB(0, 0, 0)

