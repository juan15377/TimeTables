
import sys

sys.path.append("src/Logic/")

from Subjects import Subjects
from Professor_Classroom_Group import Professors, Classrooms, Groups
from schedule_printer.schedule_latex import *

class BD():

    def __init__(self) -> None:
        self.professors = Professors(self)
        self.classrooms = Classrooms(self)
        self.groups = Groups(self)
        self.subjects = Subjects(self)
        pass
    
    def generate_pdf(self, save_path, file_name):
        
        schedule_latex = ScheduleLatex(self)
        schedule_latex.compile_to_latex(save_path, file_name)

