# necesito una funcion que reciba la base de datos, el id de un professor, aula o grupo

# me genere el grid -> string 
# genere la simbologia -> string
import numpy as np  
from typing import List

HOURS_LABELS = [
            "",
            "7:00-7:30 am", "7:30-8:00 am", "8:00-8:30 am", "8:30-9:00 am", "9:00-9:30 am", "9:30-10:00 am",
            "10:00-10:30 am", "10:30-11:00 am", "11:00-11:30 am", "11:30-12:00 pm", "12:00-12:30 pm", "12:30-1:00 pm",
            "1:00-1:30 pm", "1:30-2:00 pm", "2:00-2:30 pm", "2:30-3:00 pm", "3:00-3:30 pm", "3:30-4:00 pm",
            "4:00-4:30 pm", "4:30-5:00 pm", "5:00-5:30 pm", "5:30-6:00 pm", "6:00-6:30 pm", "6:30-7:00 pm",
            "7:00-7:30 pm", "7:30-8:00 pm", "8:00-8:30 pm", "8:30-9:00 pm", "9:00-9:30 pm", "9:30-10:00 pm"
        ]



class GridLatex:
    def __init__(self):

        self.hours =  ["7:00AM", "7:30AM", "8:00AM", "8:30AM", "9:00AM", "9:30AM", "10:00AM", 
            "10:30AM", "11:00AM", "11:30AM", "12:00PM", "12:30PM", "1:00PM", "1:30PM", 
            "2:00PM", "2:30PM", "3:00PM", "3:30PM", "4:00PM", "4:30PM", "5:00PM", 
            "5:30PM", "6:00PM", "6:30PM", "7:00PM", "7:30PM", "8:00PM", "8:30PM", 
            "9:00PM", "9:30PM", "10:00PM", "10:30PM"]
        
        hours_labels = HOURS_LABELS

        self.hours_labels = [f"\\textbf{{{x}}}" for x in hours_labels]
        days_labels = ["Horas", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        self.days_labels = [f"\\cellcolor{{headercolor}}\\textcolor{{white}}{{{x}}}" for x in days_labels]

        self.row_matrix = np.full((31, 8), True)
        self.latex_matrix = np.full((31, 8), " ", dtype=object)

        self.latex_matrix[:, 0] = self.hours_labels
        self.latex_matrix[0, :] = self.days_labels
        
    def add_subject(self, subject_latex):
        latex_matrix = self.latex_matrix
        row_matrix = self.row_matrix
        code = subject_latex.code
        hours_matrix = subject_latex.hours_matrix
        color = subject_latex.color
        red, green, blue = color


        days_block_hours = decompose_days_into_hour_blocks(hours_matrix)

        def principal(length_block, initial_hour, end_hour):
            # Determina el color del texto basado en la luminosidad del fondo
            luminance = 0.299 * red + 0.587 * green + 0.114 * blue
            text_color = "white" if luminance < 128 else "black"

            if length_block == 1:
                return (
                    f"\\multirow{{{-length_block}}}{{*}}{{"
                    f"\\cellcolor[RGB]{{{red},{green},{blue}}}"
                    f"\\textcolor{{{text_color}}}{{\\textbf{{\\small{{{code}}}}}}}"
                    f"}}"
                )

            return (
                f"\\multirow{{{-length_block}}}{{*}}{{"
                f"\\cellcolor[RGB]{{{red},{green},{blue}}}"
                f"\\textcolor{{{text_color}}}{{"
                f"\\stackunder{{"
                f"\\stackon{{"
                f"\\textbf{{{code}}}"
                f"}}{{\\scalebox{{0.9}}{{\\tiny {initial_hour}}}}}"
                f"}}{{\\scalebox{{0.9}}{{\\tiny {end_hour}}}}}"
                f"}}"
                f"}}"
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
        string_ = f"""\\begin{{table}}[ht]
                    \\centering
                    \\small
                    \\begin{{tabular}}{{|{columns}|}}
                    \\hline"""

        for row in range(31):
            string_items = unir_elementos_de_un_vector(latex_matrix[row, :])
            list_rows = lineas_fila(row_matrix[row, :])
            string_ += f"{string_items} \\\\\n{list_rows} \n"

        string_ += "\\end{tabular}\\end{table}"
        return string_


# romper_vector_partes([True, False, False, False, True, True]) -> [[1], [5, 6]]
#print(romper_vector_partes([False, False])) -> []

def split_vector_into_blocks(vector: List[bool]) -> List[List[int]]:
    """
    Splits a boolean vector into blocks of consecutive True values.

    This function identifies sequences of consecutive True values in the input vector
    and returns a list of blocks, where each block contains the indices (1-based) of
    the True values in the sequence.

    Args:
        vector: A list of boolean values (True or False).

    Returns:
        A list of blocks, where each block is a list of indices (1-based) of consecutive True values.

    Example:
        >>> split_vector_into_blocks([True, True, False, True, False, True, True])
        [[1, 2], [4], [6, 7]]
    """
    blocks = [] 
    current_block = []  
    in_block = False  

    for index, value in enumerate(vector):
        if value:

            current_block.append(index + 1)
            in_block = True
            continue

        if in_block:
            blocks.append(current_block)
            current_block = []  
            in_block = False  

    if current_block:
        blocks.append(current_block)

    return blocks


def decompose_days_into_hour_blocks(schedule_matrix: np.ndarray) -> dict[int, list[list[int]]]:
    """
    Decomposes a schedule matrix into blocks of consecutive hours for each day.

    This function takes a 2D boolean matrix (hours x days) and splits each day's column
    into blocks of consecutive True values using the `split_vector_into_blocks` function.
    The result is a dictionary where keys are days (0-6) and values are lists of blocks
    for that day.

    Args:
        schedule_matrix: A 2D numpy array of boolean values (True or False) representing
                        the schedule. Rows correspond to hours, and columns correspond to days.

    Returns:
        A dictionary where:
        - Keys are integers representing days (0 = Monday, 1 = Tuesday, ..., 6 = Sunday).
        - Values are lists of blocks, where each block is a list of 1-based indices of
          consecutive True values for that day.

    Example:
        >>> schedule_matrix = np.array([
        ...     [True, False, False, False, False, False, False],  # Monday
        ...     [False, True, False, False, False, False, False],   # Tuesday
        ...     [False, True, True, True, False, False, False],  # Wednesday
        ...     # ... (rest of the matrix)
        ... ])
        >>> decompose_days_into_hour_blocks(schedule_matrix)
        {
            0: [[1]],          # Monday: Block at hour 1
            1: [[2, 3]],       # Tuesday: Block at hours 2 and 3
            2: [[3]],          # Wednesday: Block at hour 4
            # ... (rest of the days)
        }
    """
    day_blocks = {}  

    for day in range(7):  # Iterate over each day (0 = Monday, 6 = Sunday)
        day_column = schedule_matrix[:, day]  # Extract the column for the current day
        blocks = split_vector_into_blocks(day_column)  # Split into blocks of consecutive True values
        day_blocks[day] = blocks  # Store the blocks for the current day

    return day_blocks


def lineas_fila(vector_bool):
    valores = split_vector_into_blocks(vector_bool)
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
    cadena = f"\\begin{{table}}[ht]\\centering\\small\\begin{{tabular}}{{|{columnas}|}}\\thickhline"

    for fila in range(31):
        cadena_de_elementos = unir_elementos_de_un_vector(matriz_latex[fila, :])
        lista_de_renglones = lineas_fila(matriz_renglones[fila, :])
        cadena += f"{cadena_de_elementos} \\\\\n{lista_de_renglones} \n"

    cadena += "\\end{tabular}\\end{table}"
    return cadena
