# convertir la base de datos a una estrictura mas agradable para poder hacer
# la conversion a pdf latex
from .professor_latex import ProfessorLatex, create_professors_latex
from .classroom_latex import ClassroomLatex, create_classrooms_latex
from .group_latex import GroupLatex, create_groups_latex
from .schedulegrid import GridLatex, SubjectLatex

import os
import subprocess
from pylatex import Document
import os

from pathlib import Path

def generate_output_path(directory: str, filename: str) -> str:
    # Crear un objeto Path para la ruta del directorio
    dir_path = Path(directory)

    # Combinar el directorio con el nombre del archivo (agrega la extensión .pdf)
    full_path = dir_path / f"{filename}.pdf"

    # Convertir a string para devolver la ruta como texto
    return str(full_path)


def generate_pdf_from_latex(latex_string: str, output_path: str):
    # Crear el directorio si no existe
    os.makedirs(output_path, exist_ok=True)

    # Crear el documento
    doc = Document()
    doc.preamble.append(latex_string)

    # Generar el PDF en la ruta especificada
    output_file = os.path.join(output_path, 'output')
    doc.generate_pdf(output_file, clean_tex=False)

def save_latex_to_file_and_compile(latex_content, save_path, file_name):
    """
    Guarda el contenido LaTeX en un archivo .tex con el nombre especificado,
    genera un PDF y elimina los archivos temporales generados durante la compilación.
    
    Args:
        latex_content (str): Contenido del documento LaTeX.
        save_path (str): Ruta donde se guardará el archivo .tex y se generará el PDF.
        file_name (str): Nombre del archivo (sin extensión) para el archivo .tex y el PDF generado.
    """
    # Crear la ruta completa para el archivo .tex
    tex_file_path = os.path.join(save_path, f"{file_name}.tex")

    # Guardar el contenido LaTeX en el archivo .tex
    with open(tex_file_path, "w") as f:
        f.write(latex_content)

    # Cambiar al directorio de salida antes de compilar el PDF
    original_directory = os.getcwd()
    os.chdir(save_path)  # Cambiar al directorio especificado

    try:
        # Ejecutar pdflatex para compilar el archivo .tex a PDF
        result = subprocess.run(['pdflatex', f'{file_name}.tex'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = subprocess.run(['pdflatex', f'{file_name}.tex'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Verificar si la compilación fue exitosa
    finally:
        # Eliminar archivos temporales generados por pdflatex
        latex_files = [f'{file_name}.aux', f'{file_name}.log', f'{file_name}.out', f'{file_name}.toc', f'{file_name}.fls', f'{file_name}.synctex.gz']
        for file in latex_files:
            file_path = os.path.join(save_path, file)
            if os.path.exists(file_path):
                os.remove(file_path)

        os.chdir(original_directory)  # Restaurar el directorio original


def delete_exceptions(texto):

    replace_ = {
    # Letras minúsculas con acentos y diéresis
    'á': r"\'a", 'é': r"\'e", 'í': r"\'i", 'ó': r"\'o", 'ú': r"\'u",
    'à': r"\`a", 'è': r"\`e", 'ì': r"\`i", 'ò': r"\`o", 'ù': r"\`u",
    'ä': r'\"a', 'ë': r'\"e', 'ï': r'\"i', 'ö': r'\"o', 'ü': r'\"u',
    'ã': r'\~a', 'õ': r'\~o', 'ñ': r'\~n',

    # Letras mayúsculas con acentos y diéresis
    'Á': r"\'A", 'É': r"\'E", 'Í': r"\'I", 'Ó': r"\'O", 'Ú': r"\'U",
    'À': r"\`A", 'È': r"\`E", 'Ì': r"\`I", 'Ò': r"\`O", 'Ù': r"\`U",
    'Ä': r'\"A ', 'Ë': r'\"E', 'Ï': r'\"I', 'Ö': r'\"O', 'Ü': r'\"U',
    'Ã': r' \~A ', 'Õ': r'\~O', 'Ñ': r'\~N',

    # Reemplazo de comillas dobles
    '"': r' \textquotedblleft  ',  # Comillas de apertura
    '"': r' \textquotedblright ',  # Comillas de cierre
    }


    
    for caracter, latex in replace_.items():
        texto = texto.replace(caracter, latex)
    
    return texto


class ScheduleLatex():
    
    def __init__(self, bd):
        professors_tex = []
        classrooms_tex = []
        groups_tex = []
        
        for professor in bd.professors.get():
            professor_tex = ProfessorLatex(professor.name)
            for subject  in professor.get_subjects():
                subject_tex = SubjectLatex(
                    subject.name,
                    subject.code,
                    professor.name,
                    subject.classroom.name,
                    [group.career.name for group in subject.groups],
                    [group.semester.name for group in subject.groups],
                    [group.subgroup.name for group in subject.groups],
                    subject.hours_distribution.total(),
                    professor.subject_colors.colors[subject],
                    subject.allocated_subject_matrix
                )
                
                professor_tex.add_subject(subject_tex)
            professors_tex.append(professor_tex)
        
        for classroom in bd.classrooms.get():
            classroom_tex = ClassroomLatex(classroom.name)
            for subject  in classroom.get_subjects():
                subject_tex = SubjectLatex(
                    subject.name,
                    subject.code,
                    subject.professor.name,
                    subject.classroom.name,
                    [group.career.name for group in subject.groups],
                    [group.semester.name for group in subject.groups],
                    [group.subgroup.name for group in subject.groups],
                    subject.hours_distribution.total(),
                    classroom.subject_colors.colors[subject],
                    subject.allocated_subject_matrix
                )
                
                classroom_tex.add_subject(subject_tex)
            classrooms_tex.append(classroom_tex)
            
        for group in bd.groups.get():
            group_tex = GroupLatex(
                group.career.key,
                group.career.name,
                group.semester.key,
                group.semester.name,
                group.subgroup.key,
                group.subgroup.name,
            )
            for subject in group.get_subjects():
                subject_tex = SubjectLatex(
                    subject.name,
                    subject.code,
                    subject.professor.name,
                    subject.classroom.name,
                    [group.career.name for group in subject.groups],
                    [group.semester.name for group in subject.groups],
                    [group.subgroup.name for group in subject.groups],
                    subject.hours_distribution.total(),
                    group.subject_colors.colors[subject],
                    subject.allocated_subject_matrix
                )
                
                group_tex.add_subject(subject_tex)
            groups_tex.append(group_tex)
            
        self.professors = professors_tex
        self.classrooms = classrooms_tex
        self.groups = groups_tex
        
        
        
    def compile_to_latex(self):
                
        input_text = f"""
        {create_professors_latex(self.professors)}

        {create_groups_latex(self.groups)}
        
        {create_classrooms_latex(self.classrooms)}
        
    
        """
        
        latex_content = f"""
           \\documentclass{{article}}
            \\usepackage[utf8]{{inputenc}}
            \\usepackage[T1]{{fontenc}}
            \\usepackage[spanish]{{babel}}
            \\usepackage[utf8]{{inputenc}}
            \\usepackage[spanish]{{babel}}
            \\usepackage{{amsmath}}
            \\usepackage{{amsfonts}}
            \\usepackage{{amssymb}}
            \\usepackage{{graphicx}}
            \\usepackage{{xcolor, colortbl}}
            \\usepackage{{lscape}}
            \\usepackage{{array, multirow, multicol}}
            \\usepackage[margin=0.47in]{{geometry}} % Adjust margins to 0.5 inches
            \\usepackage{{fancyhdr}}
            \\usepackage{{longtable}}
            \\usepackage{{adjustbox}}
            \\usepackage[table,xcdraw]{{xcolor}} % Para colores en las tablas
            \\usepackage{{enumitem}} % Para personalizar las listas
            \\usepackage{{stackengine}}
            \\usepackage{{graphicx}}
            \\usepackage[nottoc,notlof,notlot]{{tocbibind}}
            \\usepackage{{tocloft}}

            % Define a new command for subsubsubsections
            \\newcommand{{\\subsubsubsection}}[1]{{ \\paragraph{{#1}}\\mbox{{}}\\\\ }}

            % Adjust the depth of numbered sections
            \\setcounter{{secnumdepth}}{{4}}

            % Adjust the depth of sections in the table of contents
            \\setcounter{{tocdepth}}{{4}} 
            
            \\renewcommand{{\\cfttoctitlefont}}{{\\Large\\bfseries}}
            \\setlength{{\\cftbeforetoctitleskip}}{{0pt}}
            \\setlength{{\\cftaftertoctitleskip}}{{10pt}}
            \\setlength{{\\cftbeforesecskip}}{{0pt}}
            \\setlength{{\\cftparskip}}{{0pt}}

            \\begin{{document}}
            
            % Configuración de la numeración de página para el índice
            \\pagenumbering{{roman}}
            %\\setcounter{{page}}{{1}}


            \\tableofcontents
            \\clearpage  % Asegura un salto de página limpio

            % Reiniciar numeración de página para el contenido principal
            \\pagenumbering{{arabic}}
            \\setcounter{{page}}{{1}}

            {input_text}

            \\end{{document}}
            """
            
        return  delete_exceptions(latex_content)
            
        
        
        pass 
