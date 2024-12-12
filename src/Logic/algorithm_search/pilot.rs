use rand::Rng;
use rand::seq::SliceRandom;

// Estructura para representar un objeto
#[derive(Clone, Debug)]
struct Item {
    weight: i32,
    value: i32,
}

// Estructura para representar un individuo (solución)
#[derive(Clone)]
struct Individual {
    genes: Vec<bool>,
    fitness: f64,
}

struct GeneticKnapsack {
    items: Vec<Item>,
    max_weight: i32,
    population_size: usize,
    generations: usize,
    mutation_rate: f64,
    crossover_rate: f64,
}

impl GeneticKnapsack {
    fn new(items: Vec<Item>, max_weight: i32) -> Self {
        GeneticKnapsack {
            items,
            max_weight,
            population_size: 100,
            generations: 200,
            mutation_rate: 0.01,
            crossover_rate: 0.7,
        }
    }

    // Inicializar población aleatoria
    fn initialize_population(&self) -> Vec<Individual> {
        let mut rng = rand::thread_rng();
        (0..self.population_size)
            .map(|_| {
                let genes: Vec<bool> = (0..self.items.len())
                    .map(|_| rng.gen_bool(0.5))
                    .collect();
                Individual { 
                    genes, 
                    fitness: 0.0 
                }
            })
            .collect()
    }

    // Calcular fitness de un individuo
    fn calculate_fitness(&self, individual: &mut Individual) {
        let mut total_weight = 0;
        let mut total_value = 0;

        for (i, &included) in individual.genes.iter().enumerate() {
            if included {
                total_weight += self.items[i].weight;
                total_value += self.items[i].value;
            }
        }

        // Penalizar soluciones que excedan el peso máximo
        individual.fitness = if total_weight > self.max_weight {
            0.0
        } else {
            total_value as f64
        };
    }

    // Selección por torneo
    fn tournament_selection(&self, population: &[Individual]) -> Individual {
        let mut rng = rand::thread_rng();
        let tournament_size = 5;
        let mut tournament = Vec::new();

        for _ in 0..tournament_size {
            let random_individual = population.choose(&mut rng).cloned().unwrap();
            tournament.push(random_individual);
        }

        tournament.into_iter().max_by(|a, b| a.fitness.partial_cmp(&b.fitness).unwrap()).unwrap()
    }

    // Cruzamiento de un punto
    fn crossover(&self, parent1: &Individual, parent2: &Individual) -> (Individual, Individual) {
        let mut rng = rand::thread_rng();
        let mut offspring1 = parent1.clone();
        let mut offspring2 = parent2.clone();

        if rng.gen_bool(self.crossover_rate) {
            let crossover_point = rng.gen_range(0..parent1.genes.len());
            
            offspring1.genes[crossover_point..].copy_from_slice(&parent2.genes[crossover_point..]);
            offspring2.genes[crossover_point..].copy_from_slice(&parent1.genes[crossover_point..]);
        }

        (offspring1, offspring2)
    }

    // Mutación
    fn mutate(&self, individual: &mut Individual) {
        let mut rng = rand::thread_rng();
        for gene in individual.genes.iter_mut() {
            if rng.gen_bool(self.mutation_rate) {
                *gene = !*gene;
            }
        }
    }

    // Algoritmo genético principal
    fn solve(&mut self) -> Individual {
        let mut population = self.initialize_population();

        for _ in 0..self.generations {
            // Evaluar fitness
            population.iter_mut().for_each(|ind| self.calculate_fitness(ind));

            // Ordenar por fitness
            population.sort_by(|a, b| b.fitness.partial_cmp(&a.fitness).unwrap());

            // Crear nueva generación
            let mut new_population = population[0..10].to_vec(); // Elitismo

            while new_population.len() < self.population_size {
                let parent1 = self.tournament_selection(&population);
                let parent2 = self.tournament_selection(&population);

                let (mut child1, mut child2) = self.crossover(&parent1, &parent2);
                
                self.mutate(&mut child1);
                self.mutate(&mut child2);

                new_population.push(child1);
                new_population.push(child2);
            }

            population = new_population;
        }

        // Obtener mejor solución
        population.iter_mut().for_each(|ind| self.calculate_fitness(ind));
        population.into_iter().max_by(|a, b| a.fitness.partial_cmp(&b.fitness).unwrap()).unwrap()
    }

    // Método para imprimir la mejor solución
    fn print_solution(&self, best_solution: &Individual) {
        println!("Mejor solución encontrada:");
        println!("Fitness: {}", best_solution.fitness);
        
        let mut total_weight = 0;
        let mut total_value = 0;
        
        println!("Objetos seleccionados:");
        for (i, &included) in best_solution.genes.iter().enumerate() {
            if included {
                println!(
                    "- Objeto {}: Peso = {}, Valor = {}",
                    i, self.items[i].weight, self.items[i].value
                );
                total_weight += self.items[i].weight;
                total_value += self.items[i].value;
            }
        }
        
        println!("Peso total: {}", total_weight);
        println!("Valor total: {}", total_value);
    }
}

fn main() {
    // Ejemplo de uso
    let items = vec![
        Item { weight: 10, value: 60 },
        Item { weight: 20, value: 100 },
        Item { weight: 30, value: 120 },
        Item { weight: 15, value: 80 },
        Item { weight: 5, value: 40 },
    ];

    let max_weight = 50;

    let mut solver = GeneticKnapsack::new(items, max_weight);
    let best_solution = solver.solve();
    solver.print_solution(&best_solution);
}