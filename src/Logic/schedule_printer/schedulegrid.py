import numpy as np

import numpy as np
from typing import List

class SubjectLatex:
    def __init__(self, name: str, code: str, professor: str, classroom: str, 
                 careers: List[str], semesters: List[str], subgroups: List[str], 
                 hours: float, color, hours_matrix: np.ndarray):
        """
        Initializes a Materiatex instance.

        Parameters:
        - name: Name of the subject.
        - code: Abbreviation for the subject.
        - professor: Name of the professor.
        - classroom: Classroom location.
        - careers: List of careers.
        - semesters: List of semesters.
        - groups: List of groups.
        - hours: Total number of hours.
        - color: Color in RGBA format.
        - hours_matrix: Boolean matrix for the schedule.
        """
        self.name = name
        self.code = code
        self.professor = professor
        self.classroom = classroom
        self.careers = careers
        self.semesters = semesters
        self.subgroups = subgroups
        self.hours = hours
        self.color = color
        self.hours_matrix = hours_matrix

class GridLatex:
    def __init__(self):
        hours_labels = ["", "7:00-7:30 ", "7:30-8:00", "8:00-8:30", "8:30-9:00", "9:00-9:30", "9:30-10:00", "10:00-10:30",
                        "10:30-11:00", "11:00-11:30", "11:30-12:00", "12:00-12:30", "12:30-1:00", "1:00-1:30", "1:30-2:00",
                        "2:00-2:30", "2:30-3:00", "3:00-3:30", "3:30-4:00", "4:00-4:30", "4:30-5:00", "5:00-5:30", 
                        "5:30-6:00", "6:00-6:30", "6:30-7:00", "7:00-7:30", "7:30-8:00", "8:00-8:30", "8:30-9:00", "9:00-9:30", "9:30-10:00"]

        self.hours_labels = [f"\\textbf{{{x}}}" for x in hours_labels]
        days_labels = ["Horas", " Lunes  ", " Martes ", "Miercoles", " Jueves ", " Viernes ", " Sabado ", " Domingo "]
        
        self.days_labels = [f"\\cellcolor{{black}}\\textcolor{{white}}{{{x}}}" for x in days_labels]

        self.row_matrix = np.full((31, 8), True)
        self.latex_matrix = np.full((31, 8), " ", dtype=object)

        self.latex_matrix[:, 0] = self.hours_labels
        self.latex_matrix[0, :] = self.days_labels
        
        print(self.latex_matrix)

    def add_subject(self, subject):
        latex_matrix = self.latex_matrix
        row_matrix = self.row_matrix

        code = subject.code
        hours_matrix = subject.hours_matrix
        color = subject.color
        red, green, blue = [int(round(c)) for c in (color.red, color.green, color.blue)]

        days_block_hours = descomponer_dias_bloques_horas(hours_matrix)
        def principal(tamaño_bloque):
            return f"\\multirow{{-{tamaño_bloque}}}{{*}}{{\\cellcolor[RGB]{{{red},{green},{blue}}} \\textbf{{{code}}} }}"

        def secundary():
            return f"\\cellcolor[RGB]{{{red},{green},{blue}}}"

        for day in range(7):
            blocks_hours_for_day = days_block_hours[day]
            for block in blocks_hours_for_day:
                length_block = len(block) 
                row = block[-1] 
                column = day + 1
                latex_matrix[row, column] = principal(length_block)

                for auxiliar_color in block[:-1]:
                    latex_matrix[auxiliar_color , column] = secundary()
                    row_matrix[auxiliar_color, column] = False
                    
        self.latex_matrix = latex_matrix
        self.row_matrix = row_matrix

    def compile_to_latexstring(self):
        latex_matrix = self.latex_matrix
        row_matrix = self.row_matrix

        columns = "|".join(["c"] * 30)
        string_ = f"\\begin{{table}}[ht]\\centering\\small\\begin{{tabular}}{{|{columns}|}}\\hline"

        for row in range(31):
            string_items = unir_elementos_de_un_vector(latex_matrix[row, :])
            list_rows = lineas_fila(row_matrix[row, :])
            string_ += f"{string_items} \\\\\n{list_rows} \n"

        string_ += "\\end{tabular}\\end{table}"
        return string_

# romper_vector_partes([True, False, False, False, True, True]) -> [[1], [5, 6]]
#print(romper_vector_partes([False, False])) -> []

def romper_vector_partes(vector):
    lista = []
    elemento = []
    switch = False

    for i, val in enumerate(vector):
        if val:
            elemento.append(i + 1)
            switch = True
            continue

        if switch:
            lista.append(elemento)
            elemento = []
            switch = False

    if elemento:
        lista.append(elemento)

    return lista


def descomponer_dias_bloques_horas(matriz_de_horas):
    bloques_dias = {}

    for dia in range(7):
        dia_columna = matriz_de_horas[:, dia]
        bloques_dia = romper_vector_partes(dia_columna)
        bloques_dias[dia] = bloques_dia

    return bloques_dias


def lineas_fila(vector_bool):
    valores = romper_vector_partes(vector_bool)
    cadena = ""

    for valor in valores:
        primero = valor[0]
        ultimo = valor[-1]
        cadena += f" \\cline{{{primero}-{ultimo}}}"

    return cadena

def unir_elementos_de_un_vector(vector):
    print(vector)
    return " & ".join(vector)


def convertir_stringlatex(cuadricula):
    matriz_latex = cuadricula.matriz_latex
    matriz_renglones = cuadricula.matriz_renglones

    columnas = "|".join(["c"] * 31)
    cadena = f"\\begin{{table}}[ht]\\centering\\small\\begin{{tabular}}{{|{columnas}|}}\\hline"

    for fila in range(31):
        cadena_de_elementos = unir_elementos_de_un_vector(matriz_latex[fila, :])
        lista_de_renglones = lineas_fila(matriz_renglones[fila, :])
        cadena += f"{cadena_de_elementos} \\\\\n{lista_de_renglones} \n"

    cadena += "\\end{tabular}\\end{table}"
    return cadena
