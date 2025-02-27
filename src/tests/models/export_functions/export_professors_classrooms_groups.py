from src.models.database.components.export_functions.components.grid_formats import ProfessorLatex 
from src.tests.database_example import database_example 
from src.models.database.components.export_functions.utils import LATEX_TEMPLATE


database_example.export.individual_professors(database_example.professors.get(), "/home/juan/Escritorio/")


latex_content = LATEX_TEMPLATE(template, table_of_contents=False)
print(latex_content)

import pyperclip

pyperclip.copy(latex_content)
