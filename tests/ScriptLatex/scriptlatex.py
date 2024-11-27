import subprocess

# Contenido del archivo LaTeX
latex_content = r"""
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\title{Documento Generado desde Python}
\author{Autor Automático}
\date{\today}
\maketitle

\section*{Introducción}
Este documento ha sido generado automáticamente usando Python.

\section*{Ecuación de ejemplo}
La ecuación cuadrática es:
\begin{equation}
ax^2 + bx + c = 0
\end{equation}

\end{document}
"""

# Crear el archivo LaTeX
filename = "documento_generado.tex"
with open(filename, "w") as file:
    file.write(latex_content)

print(f"Archivo LaTeX generado: {filename}")

# Compilar el archivo LaTeX a PDF usando pdflatex
try:
    subprocess.run(["pdflatex", filename], check=True)
    print("PDF generado con éxito.")
except subprocess.CalledProcessError:
    print("Error al generar el PDF. Verifica que pdflatex esté instalado y accesible.")
