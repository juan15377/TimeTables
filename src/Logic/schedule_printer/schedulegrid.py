
from typing import List
from dataclasses import dataclass
import sys 
sys.path.append("src/Logic/")
from Colors import *


@dataclass
class SubjectLatex:
    name: str
    code: str
    professor: str
    classroom: str
    careers: List[str]
    semesters: List[str]
    groups: List[str]
    hours: float
    color: tuple
    hours_matrix: List[List[bool]]

    def __init__(self, name, code, professor, classroom, careers, semesters, groups, hours, color, hours_matrix):
        self.name = name
        self.code = code
        self.professor = professor
        self.classroom = classroom
        self.careers = careers
        self.semesters = semesters
        self.groups = groups
        self.hours = hours
        self.color = color  # Convert color to RGB tuple (0-1 range)
        self.hours_matrix = hours_matrix


class GridLatex:
    def __init__(self):
        # Initialize the LaTeX matrix and boolean matrix for row visibility
        self.matrix_rows = [[True for _ in range(8)] for _ in range(31)]
        self.matrix_latex = [["" for _ in range(8)] for _ in range(31)]

        # Define time slots and days headers in LaTeX format
        self.time_labels = [
            "", "7:00-7:30", "7:30-8:00", "8:00-8:30", "8:30-9:00", 
            "9:00-9:30", "9:30-10:00", "10:00-10:30", "10:30-11:00",
            "11:00-11:30", "11:30-12:00", "12:00-12:30", "12:30-1:00",
            "1:00-1:30", "1:30-2:00", "2:00-2:30", "2:30-3:00", 
            "3:00-3:30", "3:30-4:00", "4:00-4:30", "4:30-5:00",
            "5:00-5:30", "5:30-6:00", "6:00-6:30", "6:30-7:00"
        ]
        self.day_labels = ["Hours", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        # Assign headers to the matrix
        self.matrix_latex[0] = [f"\\textbf{{{day}}}" for day in self.day_labels]
        for i, label in enumerate(self.time_labels, start=1):
            self.matrix_latex[i][0] = f"\\textbf{{{label}}}"

    def add_subject(self, subject: 'SubjectLatex'):
        matrix_latex = self.matrix_latex
        matrix_rows = self.matrix_rows

        abbreviation = subject.code
        hours_matrix = subject.hours_matrix
        color = subject.color

        def R(c): return int(round(c * 255))
        color_red, color_green, color_blue = R(color.red/255), R(color.green/255), R(color.blue/255)

        def main_block(block_size):
            return f"\\multirow{{-{block_size}}}{{*}}{{\\cellcolor[RGB]{{{color_red},{color_green},{color_blue}}} \\textbf{{{abbreviation}}}}}"

        def secondary_block():
            return f"\\cellcolor[RGB]{{{color_red},{color_green},{color_blue}}}"

        for day in range(7):
            for block in self.break_into_blocks(hours_matrix[day]):
                block_size = len(block)
                row = block[-1] + 1
                column = day + 1
                matrix_latex[row][column] = main_block(block_size)

                for aux_row in block[:-1]:
                    matrix_latex[aux_row + 1][column] = secondary_block()
                    matrix_rows[aux_row + 1][column] = False

    def break_into_blocks(self, boolean_vector: List[bool]) -> List[List[int]]:
        """Breaks a boolean vector into continuous blocks of `True` indices."""
        blocks, current_block = [], []

        for i, val in enumerate(boolean_vector):
            if val:
                current_block.append(i)
            elif current_block:
                blocks.append(current_block)
                current_block = []
        if current_block:
            blocks.append(current_block)
        return blocks

    def compile_latex(self) -> str:
        """Compiles the LaTeX representation of the grid into a string."""
        columns = "|".join(["c" for _ in range(8)])
        latex_code = f"\\begin{{tabular}}{{|{columns}|}}\n\\hline\n"
        
        for row in self.matrix_latex:
            latex_code += " & ".join(row) + " \\\\\n\\hline\n"

        latex_code += "\\end{tabular}"
        return latex_code
