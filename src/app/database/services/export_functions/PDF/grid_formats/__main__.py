from .subject_latex import SubjectLatex 
from .schedule_grid import GridLatex 
from .symbology import SymbologyLatex
from .professors_latex import ProfessorLatex, create_professors_latex
from .classroom_latex import *
from .group_latex import * 


# convertir la base de datos a una estrictura mas agradable para poder hacer
# la conversion a pdf latex
from .professors_latex import ProfessorLatex, create_professors_latex
from .classroom_latex import ClassroomLatex, create_classrooms_latex
from .group_latex import GroupLatex, create_groups_latex

import os
import subprocess
from pylatex import Document
from pathlib import Path

from ..utils import *

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
        latex_files = [f'{file_name}.aux', f'{file_name}.log', f'{file_name}.out', 
                       f'{file_name}.toc', f'{file_name}.fls', f'{file_name}.synctex.gz']
        
        for file in latex_files:
            file_path = os.path.join(save_path, file)
            if os.path.exists(file_path):
                os.remove(file_path)

        os.chdir(original_directory)  # Restaurar el directorio original



import threading

def run_in_thread(target_function, *args, **kwargs):
    thread = threading.Thread(target=target_function, args=args, kwargs=kwargs, daemon=True)
    thread.start()
    
    
class ExportGridFormats:
    
    def __init__(self, db):
        self.db = db
        
    def complete_schedule_in_one_file_async(self, save_path, file_name):
        run_in_thread(self.complete_schedule_in_one_file, save_path, file_name)        

    def complete_schedule_in_one_file(self, save_path, file_name):
        
        input_text = f"""
        {create_professors_latex(self.db)}

        {create_groups_latex(self.db)}
        
        {create_classrooms_latex(self.db)}
        
        """
        latex_content_filter = replace_exceptions(input_text)
        latex_content = LATEX_TEMPLATE(latex_content_filter)
        
        print(latex_content)
        
        save_latex_to_file_and_compile(latex_content, save_path, file_name)
        
            
    def complete_schedule_async(self, save_path, folder_path):
        run_in_thread(self.complete_schedule, save_path, folder_path)
    
        
    def complete_schedule(self, save_path, folder_name):
        folder_path = os.path.join(save_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # crear dentro de save_path una carpeta llamada Professors        
        
        folders = ["professors", "classrooms", "groups"]
        
        for folder in folders:
            os.makedirs(os.path.join(folder_path, folder), exist_ok=True)
        pass 
    
    
        path_professors = os.path.join(folder_path, "professors")
        path_classrooms = os.path.join(folder_path, "classrooms")
        path_groups = os.path.join(folder_path, "groups")
        
        all_professors = self.db.professors.get()
        all_classrooms = self.db.classrooms.get()
        all_groups = self.db.groups.get()
        
        self.individual_professors(all_professors, path_professors)
        
        self.individual_classrooms(all_classrooms, path_classrooms)
        
        self.individual_groups(all_groups, path_groups)
        
        
        self.complete_schedule_in_one_file(folder_path, "schedule_completed")
        
    
    def individual_professors_async(self, professors, save_path):
        run_in_thread(self.individual_professors, professors, save_path)
        pass 
    
    
    def individual_professors(self, professors, save_path):
        
        for professor in professors:
            professor_latex = ProfessorLatex(self.db, professor)
            professor_name = self.db.professors.get_name(professor)
            latex_content = LATEX_TEMPLATE(professor_latex.create_template_string(), table_of_contents=False)
            latex_content_filter = replace_exceptions(latex_content)
            os.makedirs(save_path, exist_ok=True) # crea el directorio en caso de que no exista
            save_latex_to_file_and_compile(latex_content_filter, save_path, professor_name)
            
    def individual_classrooms_async(self, classrooms, save_path):
        run_in_thread(self.individual_classrooms, classrooms, save_path)
        pass

    def individual_classrooms(self, classrooms, save_path):
        
        for classroom in classrooms:
            classroom_latex = ClassroomLatex(self.db, classroom)
            classroom_name = self.db.classrooms.get_name(classroom)
            latex_content = classroom_latex.create_template_string()
            latex_content_filter = LATEX_TEMPLATE(replace_exceptions(latex_content), table_of_contents=False)
            os.makedirs(save_path, exist_ok=True) # crea el directorio en caso de que no exista
            save_latex_to_file_and_compile(latex_content_filter, save_path, classroom_name)
        pass

    def individual_groups_async(self, groups, save_path):
        run_in_thread(self.individual_groups, save_path)
        pass 

    def individual_groups(self, groups, save_path):
        
        for group in groups:
            group_latex = GroupLatex(self.db, group)
            group_name = self.db.groups.get_name(group)
            latex_content = group_latex.create_template_string()
            latex_content_filter = LATEX_TEMPLATE(replace_exceptions(latex_content), table_of_contents=False)
            os.makedirs(save_path, exist_ok=True) # crea el directorio en caso de que no exista
            save_latex_to_file_and_compile(latex_content_filter, save_path, group_name)
        pass


