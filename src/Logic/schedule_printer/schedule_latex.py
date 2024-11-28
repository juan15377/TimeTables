# convertir la base de datos a una estrictura mas agradable para poder hacer
# la conversion a pdf latex
from professor_latex import *
from classroom_latex import *
from group_latex import *
from schedulegrid import *

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
        if result.returncode == 0:
            print(f"PDF generado exitosamente en: {save_path}/{file_name}.pdf")
        else:
            print("Hubo un error durante la compilación de LaTeX:")
            print(result.stderr.decode())  # Mostrar el error si la compilación falla
    finally:
        # Eliminar archivos temporales generados por pdflatex
        latex_files = [f'{file_name}.aux', f'{file_name}.log', f'{file_name}.out', f'{file_name}.toc', f'{file_name}.fls', f'{file_name}.synctex.gz']
        for file in latex_files:
            file_path = os.path.join(save_path, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Archivo temporal eliminado: {file_path}")

        os.chdir(original_directory)  # Restaurar el directorio original

    print(f"Archivo .tex guardado en: {tex_file_path}")
    
    
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
            print(professors_tex)
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
        
        
        
    def compile_to_latex(self, save_path, file_name):
        
        print(type(self.professors[1]))
        
        input_text = f"""
        {create_professors_latex(self.professors)}
        
        {create_classrooms_latex(self.classrooms)}
        
        {create_groups_latex(self.groups)}
    
        
        """
        
        latex_content = f"""
            \\documentclass{{article}}
            \\usepackage[utf8]{{inputenc}}
            \\usepackage[spanish]{{babel}}
            \\usepackage{{amsmath}}
            \\usepackage{{amsfonts}}
            \\usepackage{{amssymb}}
            \\usepackage{{graphicx}}
            \\usepackage{{xcolor, colortbl}}
            \\usepackage{{lscape}}
            \\usepackage{{array, multirow, multicol}}
            \\usepackage[margin=0.5in]{{geometry}} % Adjust margins to 0.5 inches
            \\usepackage{{fancyhdr}}
            \\usepackage{{longtable}}
            \\usepackage{{adjustbox}}

            % Define a new command for subsubsubsections
            \\newcommand{{\\subsubsubsection}}[1]{{ \\paragraph{{#1}}\\mbox{{}}\\\\ }}

            % Adjust the depth of numbered sections
            \\setcounter{{secnumdepth}}{{4}}

            % Adjust the depth of sections in the table of contents
            \\setcounter{{tocdepth}}{{4}}

            \\begin{{document}}

            \\tableofcontents
            \\newpage

            {input_text}

            \\end{{document}}
            """
            
        save_latex_to_file_and_compile(latex_content, save_path, file_name)
        
        
        pass 
