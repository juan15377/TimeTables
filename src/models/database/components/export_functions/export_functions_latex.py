# convertir la base de datos a una estrictura mas agradable para poder hacer
# la conversion a pdf latex
from .components.grid_formats.professor_latex import ProfessorLatex, create_professors_latex
from .components.grid_formats.classroom_latex import ClassroomLatex, create_classrooms_latex
from .components.grid_formats.group_latex import GroupLatex, create_groups_latex
from .components.grid_formats.schedulegrid import GridLatex, SubjectLatex
from .utils.exceptions import replace_exceptions

import os
import subprocess
from pylatex import Document
from pathlib import Path

def LATEX_TEMPLATE(input_content, table_of_contents=True):
    return f""" 
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


            {"\\tableofcontents" if table_of_contents else ""}
            \\clearpage  % Asegura un salto de página limpio

            % Reiniciar numeración de página para el contenido principal
            \\pagenumbering{{arabic}}
            \\setcounter{{page}}{{1}}

            {input_text}

            \\end{{document}}
    """ 
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
        latex_files = [f'{file_name}.tex', f'{file_name}.aux', f'{file_name}.log', f'{file_name}.out', 
                       f'{file_name}.toc', f'{file_name}.fls', f'{file_name}.synctex.gz']
        
        for file in latex_files:
            file_path = os.path.join(save_path, file)
            if os.path.exists(file_path):
                os.remove(file_path)

        os.chdir(original_directory)  # Restaurar el directorio original


class ExportFunctionsLatex:
    
    def __init__(self, database):
        self.database = database
        
    def complete_schedule_in_one_file(save_path):
        
        input_text = f"""
        {create_professors_latex(self.database.professors.get())}

        {create_groups_latex(self.database.groups.get())}
        
        {create_classrooms_latex(self.database.classrooms.get())}
        
        """
        latex_content = LATEX_TEMPLATE(input_text)
        latex_content_filter = replace_exceptions(latex_content)
        
        save_latex_to_file_and_compile(latex_content, save_path)
        
        pass
        
    def complete_schedule(self, save_path):
        os.makedirs(save_path, exist_ok=True)
        
        # crear dentro de save_path una carpeta llamada Professors
        careers = self.database.groups.careers.get()
        careers_names = [career.name for career in careers]
        
        schedule_path_complete = os.path.join(save_path, "schedule_completed")
        self.complete_schedule(schedule_path_complete)
        
        folders = ["professors", "classrooms", "groups"]
        
        for folder_name in folders:
            os.makedirs(os.path.join(save_path, folder_name), exist_ok=True)
        pass 
    
        path_professors = s.path.join(save_path, "professors")
        path_classrooms = s.path.join(save_path, "classrooms")
        path_groups = s.path.join(save_path, "groups")
        
        all_professors = self.database.professors.get()
        all_classrooms = self.database.classrooms.get()
        all_groups = self.database.groups.get()
        
        self.individual_professors(all_professors, path_professors)
        self.individual_classrooms(all_classrooms, path_classrooms)
        self.individual_groups(all_groups, path_groups)
    
    def individual_professors(self, professors, save_path):
        
        for professor in professors:
            professor_latex = ProfessorLatex(professor)
            latex_content = LATEX_TEMPLATE(professor_latex.create_template_string(), table_of_contents=False)
            latex_content_filter = replace_exceptions(latex_content)
            save_latex_to_file_and_compile(latex_content, save_path)
            
        
    def individual_classrooms(self, classrooms, save_path):
        
        for classrom in classrooms:
            classroom_latex = ClassroomLatex(classroom)
            latex_content = classroom_latex.create_template_string()
            latex_content_filter = LATEX_TEMPLATE(filter_exceptions(latex_content), table_of_contents=False)
            save_latex_to_file_and_compile(latex_content, save_path)
        pass
    
    def individual_groups(self, groups, save_path):
        
        for group in groups:
            group_latex = GroupLatex(group)
            latex_content = group_latex.create_template_string()
            latex_content_filter = LATEX_TEMPLATE(filter_exceptions(latex_content), table_of_contents=False)
            save_latex_to_file_and_compile(latex_content, save_path)
        pass


