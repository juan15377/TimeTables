import sys

sys.path.append("src/Logic/")
sys.path.append("src/Logic/schedule_printer")

from classroom_latex import ClassroomLatex
from schedulegrid import GridLatex, SubjectLatex
from Colors import MyColorRGB
import numpy as np

hours_matrix = np.full((30, 7), False)
hours_matrix[28:30,1] = True

print(hours_matrix)

subject_1 = SubjectLatex(
    name="Matemáticas",
    code="MATEM",
    professor="Profesor 1",
    classroom="Aula 1",
    careers=["Career 1", "Career 2"],
    semesters=["Semestre 1", "Semestre 2"],
    subgroups=["Grupo 1", "Grupo 2"],
    hours=3,
    color=MyColorRGB(100, 100, 100),
    hours_matrix= hours_matrix
)


hours_matrix_2 = np.full((30, 7), False)
hours_matrix_2[0:3,4] = True


subject_2 = SubjectLatex(
    name="Matemáticas",
    code="CALC",
    professor="Profesor 1",
    classroom="Aula 1",
    careers=["Career 1", "Career 2"],
    semesters=["Semestre 1", "Semestre 2"],
    subgroups=["Grupo 1", "Grupo 2"],
    hours=3,
    color=MyColorRGB(255, 100, 100),
    hours_matrix= hours_matrix_2
)

#print(subject_1)

#print(subject_1)

grid = GridLatex()

grid.add_subject(subject_1)
grid.add_subject(subject_2)

print(grid.compile_to_latexstring())

