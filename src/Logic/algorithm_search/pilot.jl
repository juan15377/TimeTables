
mutable struct CellInfo
    min::UInt64
    max::UInt64
    total::UInt64
end

mutable struct Cell
    score::Float64
    matrix_available::Matrix{Bool}
    matrix_reestriction::Matrix{Bool}
    matrix_allocated::Matrix{Bool}
    cell_info::CellInfo
    index::UInt64
end 



m1::Matrix{Bool} = [
    1 0 0 0;
    1 1 0 0;
    0 1 0 1;
    0 1 0 0; 
]

descomponer(m1) -> [((1,1), 2), ((2,2), 3), ((3, 4), 1)]

function descomponer(matriz::Matrix{Bool})
    # Dimensiones de la matriz
    filas, columnas = size(matriz)
    
    # Lista para almacenar los bloques
    bloques = Vector{Tuple{Tuple{Int, Int}, Int}}()
    
    # Recorrer cada columna
    for j in 1:columnas
        i = 1
        while i <= filas
            # Si encontramos un valor `true`
            if matriz[i, j]
                # Guardar la posición inicial del bloque
                posicion_inicial = (i, j)
                longitud = 1
                
                # Avanzar hacia abajo para medir la longitud del bloque
                i += 1
                while i <= filas && matriz[i, j]
                    longitud += 1
                    i += 1
                end
                
                # Guardar el bloque encontrado
                push!(bloques, (posicion_inicial, longitud))
            else
                # Avanzar al siguiente elemento de la columna
                i += 1
            end
        end
    end
    
    return bloques
end
descomponer(m1)

function funcion_decreciente(x::Int)
    if x < 1 || x > 30
        error("x debe estar en el rango [1, 30]")
    end
    return 100 * (30 - x) / 29
end


function score!(cell::Cell)
    new_score = 0.0
    # entre mas bajo sea la posicion del bloque, mejor
    blocks = descomponer(cell.matrix_allocated)
    for block in blocks
        new_score += funcion_decreciente(block[1][1])
    end
    cell.score = new_score
end

function mutate(cell_1::Cell, cell_2::Cell, schedule::Schedule)
    
    if cell_1.score < cell_2.score
        # imponemos la matrix_allocated de la celula 1 en la celula 2
        cell_2.matrix_allocated = cell_2.matrix_allocate .|| (cell_1.matrix_allocated .& cell_2.matrix_available)
        update!(schedule, cell_2)
    else
        # imponemos la matrix_allocated de la celula 2 en la celula 1
        cell_1.matrix_allocated = cell_1.matrix_allocate .|| (cell_2.matrix_allocated .& cell_1.matrix_available)
        update!(schedule, cell_1)
    end
end 
