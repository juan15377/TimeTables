from src.models.database.components.export_functions.components.grid_formats import SymbologyLatex, SubjectLatex
from src.tests.database_example import database_example 


professor = database_example.professors.get()[0]
materia1 = professor.subjects[0]

symbology = SymbologyLatex()
materia_tex = SubjectLatex(materia1)
symbology.add_subject(materia_tex)
template = symbology.to_latex_string()
print(template)

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

            {input_content}

            \\end{{document}}
    """ 
    

input_text = LATEX_TEMPLATE(template)

import pyperclip

pyperclip.copy(input_text)