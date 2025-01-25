import julia
julia.install()
from julia.api import Julia
jl = Julia(compiled_modules=False)  # Desactiva módulos compilados

from julia import Main

# Cargar el archivo de Julia
Main.include("src/Logic/algorithm_search/pilot.jl")

# Llamar a la función de Julia
resultado = Main.suma(3, 4)
print("Resultado de la suma en Julia:", resultado)  # Salida: 7