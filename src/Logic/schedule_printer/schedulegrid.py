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
        self.hours =  ["7:00AM", "7:30AM", "8:00AM", "8:30AM", "9:00AM", "9:30AM", "10:00AM", 
            "10:30AM", "11:00AM", "11:30AM", "12:00PM", "12:30PM", "1:00PM", "1:30PM", 
            "2:00PM", "2:30PM", "3:00PM", "3:30PM", "4:00PM", "4:30PM", "5:00PM", 
            "5:30PM", "6:00PM", "6:30PM", "7:00PM", "7:30PM", "8:00PM", "8:30PM", 
            "9:00PM", "9:30PM", "10:00PM", "10:30PM"]
        
        hours_labels = ["", "7:00-7:30", "7:30-8:00", "8:00-8:30", "8:30-9:00", "9:00-9:30", "9:30-10:00", "10:00-10:30",
                        "10:30-11:00", "11:00-11:30", "11:30-12:00", "12:00-12:30", "12:30-1:00", "1:00-1:30", "1:30-2:00",
                        "2:00-2:30", "2:30-3:00", "3:00-3:30", "3:30-4:00", "4:00-4:30", "4:30-5:00", "5:00-5:30", 
                        "5:30-6:00", "6:00-6:30", "6:30-7:00", "7:00-7:30", "7:30-8:00", "8:00-8:30", "8:30-9:00", "9:00-9:30", "9:30-10:00"]

        self.hours_labels = [f"\\textbf{{{x}}}" for x in hours_labels]
        days_labels = ["Horas", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        self.days_labels = [f"\\cellcolor{{black}}\\textcolor{{white}}{{{x}}}" for x in days_labels]

        self.row_matrix = np.full((31, 8), True)
        self.latex_matrix = np.full((31, 8), " ", dtype=object)

        self.latex_matrix[:, 0] = self.hours_labels
        self.latex_matrix[0, :] = self.days_labels
        
    def add_subject(self, subject):
        latex_matrix = self.latex_matrix
        row_matrix = self.row_matrix

        code = subject.code
        hours_matrix = subject.hours_matrix
        color = subject.color
        red, green, blue = [int(round(c)) for c in (color.red, color.green, color.blue)]

        days_block_hours = descomponer_dias_bloques_horas(hours_matrix)

        def principal(tamaño_bloque, initiaL_hour, end_hour):
            # Escapando correctamente las llaves para f-string
            if length_block == 1:
                return (
                    "\\multirow{" + f"{-length_block}" + "}{*}{" +
                    f"\\cellcolor[RGB]{{{red},{green},{blue}}}" +
                    "\\textbf{"  + "\\small{" f"{code}" + "}}" 
                    "}"
                )

            return (
                "\\multirow{" + f"{-length_block}""}{*}{" + f"\\cellcolor[RGB]{{{red},{green},{blue}}}"
                " \\stackunder{"
                "\\stackon{"
                "\\textbf{" + f"{code}" + "}" + "}"
                "{\\scalebox{0.6}{\\tiny " + f"{initiaL_hour}" + "}}"
                "}"
                "{\\scalebox{0.6}{\\tiny " + f"{end_hour}" + "}}"
                "}" 
            )

        def secundary():
            return f"\\cellcolor[RGB]{{{red},{green},{blue}}}"

        for day in range(7):
            blocks_hours_for_day = days_block_hours[day]
            for block in blocks_hours_for_day:
                length_block = len(block) 
                row = block[-1] 
                column = day + 1
                initial_hour = self.hours[row - length_block]
                end_hour = self.hours[row]
                
                latex_matrix[row, column] = principal(length_block, initial_hour, end_hour)

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


