
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

A = 1

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

function decrecent_function(x::Int)
    if x < 1 || x > 30
        error("x debe estar en el rango [1, 30]")
    end
    return 100 * (30 - x) / 29
end

function score2(minimo::Real, maximo::Real, total::Real)
    """
    Calcula una puntuación basada en si `total` está dentro del rango [minimo, maximo].
    La puntuación es máxima (1) si `total` está dentro del rango, y disminuye a medida que
    `total` se aleja de los límites.

    Parámetros:
        minimo: Límite inferior del rango.
        maximo: Límite superior del rango.
        total: Valor a evaluar.

    Retorna:
        Un valor entre 0 y 1 que representa la puntuación.
    """
    # Verifica que el mínimo sea menor o igual al máximo
    if minimo > maximo
        error("El valor de 'minimo' debe ser menor o igual que 'maximo'.")
    end

    # Si el total está dentro del rango, la puntuación es máxima (1)
    if minimo <= total <= maximo
        return 1.0
    end

    # Si el total está fuera del rango, calcula la distancia al límite más cercano
    if total < minimo
        distancia = minimo - total
    else
        distancia = total - maximo
    end

    # Calcula la puntuación como 1 / (1 + distancia)
    # Esto asegura que la puntuación disminuya a medida que la distancia aumenta
    return 1000 * 1 / (1 + distancia)
end


function crecimiento_decrecimiento_rapido(x::Real, total::Real, tasa_crecimiento::Real=1.0, tasa_decrecimiento::Real=10.0)
    """
    Función que crece hasta un valor `total` y decrece rápidamente cuando `x` lo supera.

    Parámetros:
        x: Valor de entrada.
        total: Valor máximo hasta el cual la función crece.
        tasa_crecimiento: Controla qué tan rápido crece la función (opcional, default=1.0).
        tasa_decrecimiento: Controla qué tan rápido decrece la función después de superar `total` (opcional, default=10.0).

    Retorna:
        El valor de la función en `x`.
    """
    if x == 0
        return 0
    end
    if x <= total
        # Crecimiento suave: usamos una función sigmoide
        return 1 / (1 + exp(-tasa_crecimiento * (x - total/2)))
    else
        # Decrecimiento rápido: usamos una exponencial negativa
        return exp(-tasa_decrecimiento * (x - total))
    end
end

crecimiento_decrecimiento_rapido(1, 10)


function score!(cell::Cell)
    new_score = 0.0
    # entre mas bajo sea la posicion del bloque, mejor
    blocks = descomponer(cell.matrix_allocated)
    total = cell.cell_info.total
    completed = sum(cell.matrix_allocated)
    aumento = crecimiento_decrecimiento_rapido(completed, total)
    new_score += aumento

    cell.score = new_score
end

function crossover_matrices(matrix1::Matrix, matrix2::Matrix, score1::Float64, score2::Float64)
    """
    Realiza el cruce de dos matrices intercambiando una mitad continua de una columna o fila,
    teniendo en cuenta los scores de las matrices.

    Parámetros:
    - matrix1: Primera matriz padre (Matrix).
    - matrix2: Segunda matriz padre (Matrix).
    - score1: Score de la primera matriz.
    - score2: Score de la segunda matriz.

    Retorna:
    - child: Matriz hija resultante del cruce.
    """
    # Verificar que las matrices tengan la misma forma
    if size(matrix1) != size(matrix2)
        error("Las matrices deben tener la misma forma")
    end

    # Crear una copia de matrix1 para el hijo
    child = copy(matrix1)

    # Calcular la probabilidad de elegir segmentos de matrix1 o matrix2
    total_score = score1 + score2
    prob_matrix1 = score1 / total_score  # Probabilidad de elegir de matrix1
    prob_matrix2 = score2 / total_score  # Probabilidad de elegir de matrix2

    # Elegir aleatoriamente si cruzar por filas o columnas
    if rand() < 0.5
        # Cruce por columnas
        col = rand(1:size(matrix1, 2))  # Elegir una columna al azar
        split_point = rand(1:size(matrix1, 1))  # Elegir un punto de división en la columna

        # Decidir de qué matriz tomar el segmento basado en los scores
        if rand() < prob_matrix1
            child[split_point:end, col] = matrix1[split_point:end, col]  # Tomar de matrix1
        else
            child[split_point:end, col] = matrix2[split_point:end, col]  # Tomar de matrix2
        end
    else
        # Cruce por filas
        row = rand(1:size(matrix1, 1))  # Elegir una fila al azar
        split_point = rand(1:size(matrix1, 2))  # Elegir un punto de división en la fila

        # Decidir de qué matriz tomar el segmento basado en los scores
        if rand() < prob_matrix1
            child[row, split_point:end] = matrix1[row, split_point:end]  # Tomar de matrix1
        else
            child[row, split_point:end] = matrix2[row, split_point:end]  # Tomar de matrix2
        end
    end

    return child
end

[i for i in 1:100, j in 1:1000]

# Ejemplo de uso
matrix1 = [1 2 3;
           4 5 6; 
           7 8 9]

matrix2 = [9 8 7; 
           6 5 4;
           3 2 1]
        

score1 = 10.0  # Score de matrix1
score2 = 5.0  # Score de matrix2

child = crossover_matrices(matrix1, matrix2, score1, score2)
println("Matriz hija:")
println(child)


function cross!(cell_1::Cell, cell_2::Cell, schedule)

    
    if cell_1.score < cell_2.score
        # imponemos la matrix_allocated de la celula 1 en la celula 2
        cell_2.matrix_allocated = crossover_matrices(cell_1.matrix_allocated, cell_2.matrix_allocated, cell_1.score, cell_2.score)
        # actualizar cambio en las demas celulas
        propagate_changes!(schedule, cell_2)
    else
        # imponemos la matrix_allocated de la celula 2 en la celula 1
        cell_1.matrix_allocated = crossover_matrices(cell_2.matrix_allocated, cell_1.matrix_allocated, cell_2.score, cell_1.score)
        # actualizar cambio en las demas celulas
        propagate_changes!(schedule, cell_1)
    end
end 

mutable struct AdyacentMatrixGraph
    matrix::Matrix{Bool}
end 

function generate_population()

end 

subjects = Dict(
    1 => Dict(
        :matrix_reestriction => fill(true, 30, 7),  # Usar símbolo :matrix_reestriction
        :info => CellInfo(1, 2, 5),                # Usar símbolo :info
        :matrix_available => fill(true, 30, 7),    # Usar símbolo :matrix_available
        :matrix_allocated => fill(false, 30, 7),   # Usar símbolo :matrix_allocated
    ),
    2 => Dict(
        :matrix_reestriction => fill(true, 30, 7),
        :info => CellInfo(1, 2, 5),
        :matrix_available => fill(true, 30, 7),
        :matrix_allocated => fill(false, 30, 7),
    ),
    3 => Dict(
        :matrix_reestriction => fill(true, 30, 7),
        :info => CellInfo(1, 2, 5),
        :matrix_available => fill(true, 30, 7),
        :matrix_allocated => fill(false, 30, 7),
    ),
    4 => Dict(
        :matrix_reestriction => fill(true, 30, 7),
        :info => CellInfo(1, 2, 5),
        :matrix_available => fill(true, 30, 7),
        :matrix_allocated => fill(false, 30, 7),
    )
)

cells::Vector{Cell} = []
c=1
for (key, value) in subjects
    cell = Cell(0.0, value[:matrix_available], value[:matrix_reestriction], value[:matrix_allocated], value[:info], c)
    score!(cell)
    push!(cells, cell)
    c += 1
end

adyacent_matrix = AdyacentMatrixGraph(
    [
        0 1 1 0;
        1 0 1 1;
        1 1 0 0;
        0 1 0 0;
    ]
)

p1 = [1, 2]
p2 = [3, 4]

g1 = [1, 2]
g2 = [3, 4]

a1 = [1, 4]
a2 = [2, 3]

subjects_classrooms = Dict(
    1 => a1,
    2 => a2,
)

subjects_professors = Dict(
    1 => p1,
    2 => p2,
)

subjects_groups = Dict(
    1 => g1,
    2 => g2,
)

mutable struct Schedule
    cells::Vector{Cell}
    adyacent_matrix_graph::AdyacentMatrixGraph
    names_subjects::Vector{String}
    subjects_classrooms::Dict{Number, Vector{Int}}
    subjects_professors::Dict{Number, Vector{Int}}
    subjects_groups::Dict{Number, Vector{Int}}
    score::Float64

    function Schedule(adyacent_matrix_graph::AdyacentMatrixGraph, cells::Vector{Cell}, subjects_classrooms, subjects_professors, subjects_groups, names_subjects)

        score = sum([cell.score for cell in cells])
        schedule = new(cells, adyacent_matrix_graph, names_subjects, subjects_classrooms, subjects_professors, subjects_groups, score)
        return schedule
    end

end
cells
adyacent_matrix

schedule = Schedule(adyacent_matrix, cells, subjects_classrooms, subjects_professors, subjects_groups, ["mathematics, algorithms","calculus", "physics"])

schedules = [deepcopy(schedule) for _ in 1:10]

"""
la funcion propaga los cambios para que las matrices de viabilidad de las demas 
celulas se actualicen para que en estos no sea posibles colocar bloques ahi
"""
function propagate_changes!(schedule::Schedule, cell::Cell)
    index_cells_to_interate = findall(schedule.adyacent_matrix_graph.matrix[cell.index])
    for index in index_cells_to_interate
        cell_ = schedule.cells[index]
        cell_.matrix_available = cell_.matrix_available .& .!(cell.matrix_available)
        before_score = cell_.score
        score!(cell_)
        new_score = cell_.score
        update_score!(schedule, before_score, new_score)
    end
end

findall([true, false, true, false])

function update_score!(schedule::Schedule, before_score::Float64, new_score::Float64)
    schedule.score -= before_score
    schedule.score += new_score
end 



function mutate!(schedule::Schedule, α::Float64)
    for cell in schedule.cells
        if rand() < α
            index = sum(cell.matrix_available) == 0 ? continue :  rand(findall(cell.matrix_available)) 
            cell.matrix_allocated[index] = !cell.matrix_allocated[index]
            before_score = cell.score
            score!(cell)
            new_score = cell.score
            update_score!(schedule, before_score, new_score)
            propagate_changes!(schedule, cell)
        end
    end
end 



function cross!(schedule_1::Schedule, schedule_2::Schedule, schedule)
    # se seleccionan una cantidad aleatoria de celulas dependiendo de sus scores
    proportion = 0

    if schedule_1.score > schedule_2.score 
        val = 0
        if schedule_1.score == 0
            val = 1
        end 
        proportion = schedule_1.score / (schedule_2.score + val + schedule_1.score)
    else
        val = 0
        if schedule_2.score == 0
            val = 1
        end
        proportion = schedule_2.score / (schedule_1.score + val + schedule_1.score)
    end

    if proportion == NaN
        proportion = .5
    end

    proportion = rand()

    num_cells_to_cross = Int(round(proportion * length(schedule_1.cells)))

    indexs_cells_to_cross = rand(collect(1:length(schedule_1.cells)), num_cells_to_cross)
    for index_cell in indexs_cells_to_cross
        cross!(schedule_1.cells[index_cell], schedule_2.cells[index_cell], schedule)

        before_score_1 = schedule_1.cells[index_cell].score
        before_score_2 = schedule_2.cells[index_cell].score

        score!(schedule_1.cells[index_cell])
        score!(schedule_2.cells[index_cell])

        new_score_1 = schedule_1.cells[index_cell].score
        new_score_2 = schedule_2.cells[index_cell].score

        update_score!(schedule_1, before_score_1, new_score_1)
        update_score!(schedule_2, before_score_2, new_score_2)
    end
end 

function roulette_wheel_selection(population::Vector, fitness_scores::Vector{Float64})
    """
    Selecciona un individuo de la población usando el método de ruleta.

    Parámetros:
        population: Vector de individuos.
        fitness_scores: Vector de puntuaciones de aptitud (fitness) correspondientes a cada individuo.

    Retorna:
        Un individuo seleccionado.
    """
    # Verifica que la población y las puntuaciones de aptitud tengan el mismo tamaño
    if length(population) != length(fitness_scores)
        error("La población y las puntuaciones de aptitud deben tener el mismo tamaño.")
    end

    # Calcula la aptitud total de la población
    total_fitness = sum(fitness_scores)

    # Si la aptitud total es cero, selecciona un individuo al azar
    if total_fitness == 0
        return population[rand(1:length(population))]
    end

    # Genera un número aleatorio entre 0 y la aptitud total
    pick = rand() * total_fitness

    # Itera sobre la población para seleccionar un individuo
    current = 0.0
    for (i, fitness) in enumerate(fitness_scores)
        current += fitness
        if current > pick
            return population[i]
        end
    end

    # Si no se selecciona ningún individuo (por errores de redondeo), devuelve el último
    return population[end]
end



function execute_genetic_algorithm(schedule, α::Float64, num_generations::Int, num_schedules::Int)
    schedules = [deepcopy(schedule) for _ in 1:num_schedules]

    for _ in 1:num_generations
        for i in 1:3
            schedule_1 = roulette_wheel_selection(schedules, [s.score for s in schedules])
            schedule_2 = roulette_wheel_selection(schedules, [s.score for s in schedules])

            cross!(schedule_1, schedule_2, schedule)
        end
        indexs_cells = rand(1:num_schedules, rand(1:10))
        for index in indexs_cells
            mutate!(schedules[index], α)
        end
    end
    print([s.score for s in schedules])
    best_schedule = (sort(schedules, by = x -> x.score))[end]
    return best_schedule
end

schedule.cells[1].matrix_allocated

best_schedule = execute_genetic_algorithm(schedule, 0.1, 100_000, 100)

crecimiento_decrecimiento_rapido(0,5)

sum(best_schedule.cells[1].matrix_allocated)

best_schedule.cells[1].matrix_allocated

best_schedule.cells[3].score = 0
score!(best_schedule.cells[2])

crecer__(210, 5)

for i in 1:1000
    print(i)
end 

using Base.Threads

results = zeros(100)
@threads for i in 1:100
    results[i] = expensive_computation(i)
end

@fastmath function fast_sum(x)
    return sum(x)
end


A = rand(10000, 1000)

@allocated Aa