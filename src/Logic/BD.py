
import sys

sys.path.append("src/Logic/")

from Subjects import Subjects
from Professor_Classroom_Group import Professors, Classrooms, Groups


class BD():

    def __init__(self) -> None:
        self.professors = Professors(self)
        self.classrooms = Classrooms(self)
        self.groups = Groups(self)
        self.subjects = Subjects(self)
        pass