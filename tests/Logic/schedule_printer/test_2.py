import sys

sys.path.append("src/Logic/")
sys.path.append("src/Logic/schedule_printer")

from classroom_latex import ClassroomLatex
from schedulegrid import GridLatex, SubjectLatex
from Colors import MyColorRGB
from symbology import SymbolLatex, SubjectLatex
import numpy as np

hours_matrix = np.full((30, 7), False)
hours_matrix[0:3,1] = True

hours_matrix = np.full((30, 7), False)
hours_matrix[0:3,1] = True

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


sym = SymbolLatex()
sym.add_subject(subject_1)

print(sym.to_latex_string())