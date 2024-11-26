from Keys import Key
from abc import ABC, abstractmethod
import numpy as np
import random as rn
from Colors import MyColorRGB
#from Subjects import *
from Hours import HoursComposition

class PCGMethods:
    """Handles shared methods for PGA instances."""

    def __init__(self, pcg) -> None:
        self.pcg = pcg

    def change_availability_matrix(self, new_availability_matrix):
        """Changes the availability of the PGA and updates associated subjects."""
        self.pcg.availability_matrix = new_availability_matrix
        for subject in self.pcg.subjects:
            subject.update_availability_matrix()

    def update_subjects_availability_matrices(self):
        """Updates availability for all associated subjects."""
        for subject in self.pcg.subjects:
            subject.update_availability_matrix()

    def completion_rate(self):
        """Calculates the completion rate of assigned hours."""
        total_hours = 0
        missing_hours = 0
        for subject in self.pcg.subjects:
            total_hours += subject.hours_distribution.total()
            missing_hours += subject.hours_distribution.remaining()
        return 1 - missing_hours / total_hours if total_hours != 0 else 1


class SubjectColors:
    """Manages colors for subjects."""

    def __init__(self) -> None:
        self.colors = {}

    def change_color(self, subject, color):
        """Changes the color assigned to a subject."""
        self.colors[subject] = color

    def add_subject(self, subject):
        """Assigns a random color to a new subject."""
        red = rn.randint(0, 255)
        green = rn.randint(0, 255)
        blue = rn.randint(0, 255)
        color = MyColorRGB(red, green, blue)
        self.colors[subject] = color

    def remove_subject(self, subject):
        """Removes a subject from the color mapping."""
        if subject in self.colors:
            del self.colors[subject]


class PCG:
    """Base class for shared properties and methods among professors, classrooms, and groups."""

    def __init__(self) -> None:
        self.subjects = []
        self.key = Key()
        self.availability_matrix = np.full((30, 7), True)
        self.methods = PCGMethods(self)
        self.subject_colors = SubjectColors()

    def add_subject(self, subject):
        """Adds a subject to the PGA and assigns a color."""
        self.subjects.append(subject)
        self.subject_colors.add_subject(subject)

    def remove_subject(self, subject):
        """Removes a subject from the PGA and updates its color mapping."""
        if subject in self.subjects:
            self.subjects.remove(subject)
            self.subject_colors.remove_subject(subject)

    def get_subjects(self):
        """Returns the list of subjects."""
        return self.subjects

# ? Profesor
# ? Professor, Classroom, and Group classes extend from PGA

DEFAULT_PCG = PCG()


class Professor(PCG):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name


# ? Classroom

class Classroom(PCG):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name


# ? Groups have a more complex constructor, requiring three components:
# ? an associated Career, Semester, and Subgroup. 
# ? Therefore, the creation of Groups will be managed by a GroupManager.

class Career:
    def __init__(self, name):
        self.name = name
        self.key = Key()


class Semester:
    def __init__(self, name):
        self.name = name
        self.key = Key()


class Subgroup:
    def __init__(self, name):
        self.name = name
        self.key = Key()


class Group(PCG):
    def __init__(self, career: Career, semester: Semester, subgroup: Subgroup) -> None:
        super().__init__()
        self.career = career
        self.semester = semester
        self.subgroup = subgroup


class Careers:
    def __init__(self) -> None:
        self.careers = []

    def get(self):
        return self.careers

    def remove(self, career):
        self.careers.remove(career)

    def new(self, name):
        career = Career(name)
        self.careers.append(career)


class Semesters:
    def __init__(self) -> None:
        self.semesters = []

    def get(self):
        return self.semesters

    def remove(self, semester):
        self.semesters.remove(semester)

    def new(self, name):
        semester = Semester(name)
        self.semesters.append(semester)


class Subgroups:
    def __init__(self) -> None:
        self.subgroups = []

    def get(self):
        return self.subgroups

    def remove(self, subgroup):
        self.subgroups.remove(subgroup)

    def new(self, name):
        subgroup = Subgroup(name)
        self.subgroups.append(subgroup)


class Groups:
    def __init__(self, BD) -> None:
        self.careers = Careers()
        self.semesters = Semesters()
        self.subgroups = Subgroups()
        self.groups = []

    def new(self, career: Career, semester: Semester, subgroup: Subgroup):
        # If a group with the same career, semester, and subgroup already exists, do not create a new one.
        for group in self.groups:
            if group.career == career and group.semester == semester and group.subgroup == subgroup:
                return None

        group = Group(career, semester, subgroup)
        self.groups.insert(0, group)

    def get(self):
        return self.groups

    def remove(self, group):
        self.groups.remove(group)


class Professors:
    def __init__(self, BD) -> None:
        self.professors = []

    def new(self, name):
        professor = Professor(name)
        self.professors.insert(0, professor)

    def get(self):
        return self.professors

    def remove(self, professor):
        self.professors.remove(professor)


class Classrooms:
    def __init__(self, BD) -> None:
        self.classrooms = []

    def new(self, name):
        classroom = Classroom(name)
        self.classrooms.insert(0, classroom)

    def get(self):
        return self.classrooms

    def remove(self, classroom):
        self.classrooms.remove(classroom)
