import random


# fitness function = number of non-attacking pairs of queens (min = 0, max = 28)
def number_of_non_attacking_pairs_of_queens_fitness_function(board_state: list[int]) -> int:
    return 28 - get_number_of_attacking_queens(board_state)


def get_number_of_attacking_queens(board_state: list[int]) -> int:
    # There is only 1 queen per column in this formulation, so they will never be attacking vertically
    attacking_queens = 0
    # check for horizontally attacking queens
    for i in board_state:
        attacking_queens += board_state.count(i) - 1
    # check for diagonally attacking queens
    attacking_queens += get_number_of_attacking_queens_on_diagonal(board_state)

    return attacking_queens // 2


def get_number_of_attacking_queens_on_diagonal(board_state) -> int:
    attacking_queens = 0

    # for each queen
    for i in range(0, 8):
        for j in range(0, 7):
            if abs(i - j) == abs(board_state[i] - board_state[j]) and i != j:
                attacking_queens += 1

    return attacking_queens


class Individual:
    def __init__(self, board_state, parents, generation):
        self.board_state: [] = board_state
        self.fitness = self.calculate_fitness()
        self.parents: [Individual] = parents
        self.generation = generation

    def calculate_fitness(self) -> int:
        return number_of_non_attacking_pairs_of_queens_fitness_function(self.board_state)

    def mutate(self):
        self.board_state[random.randint(0, 7)] = random.randint(1, 8)


class Population:
    def __init__(self, population_size: int, generation_number: int, fitness_function, mutation_percent, population=[]):
        self.population_size = population_size
        self.generation = generation_number
        self.fitness_function = fitness_function
        self.mutation_percent = mutation_percent
        if generation_number == 1:
            self.population: [Individual] = self.generate_random_population(population_size)
        else:
            self.population: [Individual] = population
        self.average_fitness = self.calculate_average_fitness_of_population()
        self.fitness_standard_deviation = self.calculate_fitness_standard_deviation()
        self.parents: [Individual] = []
        self.children: [Individual] = []

    def __str__(self):
        string = ''
        for individual in self.population:
            string += str(individual.board_state)
            string += '\n'
        return string

    @staticmethod
    def generate_random_individual() -> Individual:
        random_board_state = random.choices(range(1, 9), k=8)
        # print(str(random_board_state))
        return Individual(random_board_state, [None], 0)

    def generate_random_population(self, population_size) -> [Individual]:
        random_population = []
        for i in range(0, population_size):
            random_population.append(self.generate_random_individual())
        return random_population

    def generate_new_generation(self):
        # select fit parents
        self.select_parents()
        # generate children
        self.generate_children()
        # mutate children
        self.mutate_children()
        return Population(self.population_size, self.generation + 1, self.fitness_function, self.mutation_percent,
                          self.children)

    def select_parents(self):
        for individual in self.population:
            if random.gauss(mu=self.average_fitness, sigma=self.fitness_standard_deviation) \
                    >= self.normalized_fitness(individual):
                self.parents.append(individual)
            if len(self.parents) > self.population_size:
                break

    def generate_children(self):
        shuffled_parents = self.parents
        random.shuffle(shuffled_parents)
        i = 0
        crossover = random.randint(0, 7)
        while i < len(shuffled_parents) - 2:
            child1 = Individual(shuffled_parents[i].board_state[:crossover] +
                                shuffled_parents[i+1].board_state[crossover:],
                                [shuffled_parents[i], shuffled_parents[i+1]], self.generation + 1)
            child2 = Individual(shuffled_parents[i+1].board_state[:crossover]
                                + shuffled_parents[i].board_state[crossover:],
                                [shuffled_parents[i], shuffled_parents[i+1]], self.generation + 1)
            self.children += [child1, child2]
            crossover = random.randint(0, 7)
            i = i + 2

    def mutate_children(self):
        for child in self.children:
            if random.randrange(0, 100) >= (100 - self.mutation_percent):
                child.mutate()

    def calculate_average_fitness_of_population(self):
        fitness_sum = 0
        for individual in self.population:
            fitness_sum += individual.fitness
        return fitness_sum / self.population_size

    def normalized_fitness(self, individual):
        return individual.fitness / self.average_fitness

    def calculate_fitness_standard_deviation(self):
        variance = sum([((individual.fitness - self.average_fitness) ** 2) for individual in self.population]) \
                   / self.population_size
        return variance ** 0.5


test_population = Population(10, 1, number_of_non_attacking_pairs_of_queens_fitness_function, 1)
print(str(test_population))

test_population2 = test_population.generate_new_generation()
print(str(test_population2))

#test_board_state: [int] = [7, 6, 2, 5, 7, 4, 8, 3]
#print(str(get_number_of_attacking_queens(test_board_state)))
