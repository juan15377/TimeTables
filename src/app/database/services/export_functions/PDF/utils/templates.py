def LATEX_TEMPLATE(input_content, table_of_contents=True):
    return f"""
\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage[spanish]{{babel}}
\\usepackage{{amsmath}}
\\usepackage{{amsfonts}}
\\usepackage{{amssymb}}
\\usepackage{{graphicx}}
\\usepackage{{xcolor, colortbl}}
\\usepackage{{lscape}}
\\usepackage{{array, multirow, multicol}}
\\usepackage[margin=0.47in]{{geometry}} % Manteniendo los márgenes originales
\\usepackage{{fancyhdr}}
\\usepackage{{longtable}}
\\usepackage{{adjustbox}}
\\usepackage[table,xcdraw]{{xcolor}}
\\usepackage{{enumitem}}
\\usepackage{{stackengine}}
\\usepackage{{graphicx}}
\\usepackage[nottoc,notlof,notlot]{{tocbibind}}
\\usepackage{{tocloft}}

% Define a new command for subsubsubsections (mantenido del original)
\\newcommand{{\\subsubsubsection}}[1]{{ \\paragraph{{#1}}\\mbox{{}}\\\\  }}

% Adjust the depth of numbered sections (mantenido del original)
\\setcounter{{secnumdepth}}{{4}}

% Adjust the depth of sections in the table of contents (mantenido del original)
\\setcounter{{tocdepth}}{{4}}

\\renewcommand{{\\cfttoctitlefont}}{{\\Large\\bfseries}}
\\setlength{{\\cftbeforetoctitleskip}}{{0pt}}
\\setlength{{\\cftaftertoctitleskip}}{{10pt}}
\\setlength{{\\cftbeforesecskip}}{{0pt}}
\\setlength{{\\cftparskip}}{{0pt}}

% Mejoras estéticas
\\definecolor{{headercolor}}{{RGB}}{{40, 60, 100}} % Azul oscuro para cabeceras
\\definecolor{{subjectcolor}}{{RGB}}{{42, 157, 80}} % Verde para materias (similar al original)
\\definecolor{{backgroundcolor}}{{RGB}}{{245, 250, 255}} % Fondo celeste muy claro

% Configuración de encabezados de página
\\pagestyle{{fancy}}
\\fancyhf{{}}
\\renewcommand{{\\headrulewidth}}{{1pt}}
\\fancyfoot[C]{{\\thepage}}
\\setlength{{\\arrayrulewidth}}{{1.5pt}} % Grosor para \hline y líneas verticales
\\newcommand{{\\thickhline}}{{
  \\noalign{{\\vskip 1pt}}%
  \\hrule height 1pt%
  \\noalign{{\\vskip 1pt}}%
}}

\\begin{{document}}
\\setlength{{\\arrayrulewidth}}{{1.2pt}} % Grosor de todas las líneas de la tabla
\\newlength{{\mylinewidth}}
\\setlength{{\mylinewidth}}{{1.2pt}}
% Configuración de la numeración de página para el índice
\\pagenumbering{{roman}}
%\\setcounter{{page}}{{1}}

{f"\\\\tableofcontents" if table_of_contents else ""}

\\clearpage % Asegura un salto de página limpio

% Reiniciar numeración de página para el contenido principal
\\pagenumbering{{arabic}}
\\setcounter{{page}}{{1}}

{input_content}

\\end{{document}}
"""