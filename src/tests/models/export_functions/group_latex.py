from src.models.database.components.export_functions.components.grid_formats import GroupLatex, create_groups_latex
from src.tests.database_example import database_example 
from src.models.database.components.export_functions.utils import LATEX_TEMPLATE


group = database_example.groups.get()[0]
group_latex = GroupLatex(group)
template = create_groups_latex(database_example.groups.get())

latex_content = LATEX_TEMPLATE(template, table_of_contents=False)
print(latex_content)

import pyperclip

pyperclip.copy(latex_content)
