import sys

sys.path.append("src/Logic/")
sys.path.append("src/Logic/schedule_printer")

from classroom_latex import ClassroomLatex
from schedulegrid import SubjectLatex, GridLatex
from Colors import MyColorRGB
import numpy as np

subject_1 = SubjectLatex(
    name="Matemáticas",
    code="MATEMÁTICA-1",
    professor="Profesor 1",
    classroom="Aula 1",
    careers=["Career 1", "Career 2"],
    semesters=["Semestre 1", "Semestre 2"],
    groups=["Grupo 1", "Grupo 2"],
    hours=3,
    color=MyColorRGB(100, 100, 100),
    hours_matrix= np.random.choice([True, False], size=(30, 7))
)

print(subject_1.hours_matrix)

grid = GridLatex()

grid.add_subject(subject_1)

print(grid.compile_latex())
