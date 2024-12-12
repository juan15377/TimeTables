# Variables que se van a insertar
code = "Centro"
initiaL_hour = "9:00 am"
end_hour = "10:00 pm"

# LaTeX con escapado de llaves
latex_code = (
    "\\stackunder{"
    "\\stackon{"
    "\\textbf{" + f"{code}" + "}"
    "{\\scalebox{0.6}{\\tiny " + f"{initiaL_hour}" + "}}"
    "}"
    "{\\scalebox{0.6}{\\tiny " + f"{end_hour}" + "}}"
    "}"
)

length_block = 4

red = 100
green = 100
blue = 100

colors = f"\\cellcolor[RGB]{{{red},{green},{blue}}}"

block = (
    "\\multirow{" + f"{-length_block}""}{*}{" + f"\\cellcolor[RGB]{{{red},{green},{blue}}}"
    " \\stackunder{"
    "\\stackon{"
    "\\textbf{" + f"{code}" + "}" + "}"
    "{\\scalebox{0.6}{\\tiny " + f"{initiaL_hour}" + "}}"
    "}"
    "{\\scalebox{0.6}{\\tiny " + f"{end_hour}" + "}}"
    "}" 
)


bueno = "\multirow{-4}{*}{\cellcolor[RGB]{254,230,74} \stackunder{\stackon{\\textbf{Centro}}{\scalebox{0.6}{\\tiny 9:00 am}}}{\scalebox{0.6}{\\tiny 10:00 pm }} } "

print(block)
