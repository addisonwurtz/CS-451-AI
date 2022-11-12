import random
import matplotlib.pyplot as plt


# fitness function = number of non-attacking pairs of queens (min = 0, max = 28)
def non_attacking_queens_fitness_function(board_state: list[int]) -> int:
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

    def __str__(self):
        return str(self.fitness) + '\t' + str(self.board_state)

    def calculate_fitness(self) -> int:
        return non_attacking_queens_fitness_function(self.board_state)

    def mutate(self):
        self.board_state[random.randint(0, 7)] = random.randint(1, 8)


class Epoch:
    def __init__(self, population_size: int, generation_number: int, fitness_function, mutation_percent, population=[]):
        self.population_size = population_size
        self.generation = generation_number
        self.fitness_function = fitness_function
        self.mutation_percent = mutation_percent
        if not population:
            self.population: [Individual] = self.generate_random_population(population_size)
        else:
            self.population: [Individual] = population
        self.average_fitness = self.calculate_average_fitness_of_population()
        self.fittest_individual = self.find_fittest()
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

    def create_new_generation(self):
        # select fit parents
        self.select_parents()
        # generate children
        while len(self.children) < self.population_size:
            self.generate_children()
        # mutate children
        self.mutate_children()
        return Epoch(self.population_size, self.generation + 1, self.fitness_function, self.mutation_percent,
                     self.children)

    def select_parents(self):
        for individual in self.population:
            if random.randrange(0, 20) <= self.normalized_fitness(individual):
                self.parents.append(individual)
            if len(self.parents) > self.population_size:
                break

    def generate_children(self):
        shuffled_parents: [] = self.parents
        random.shuffle(shuffled_parents)
        i = 0
        crossover = random.randint(0, 7)
        while i < len(shuffled_parents) - 1:
            child1 = Individual(shuffled_parents[i].board_state[:crossover] +
                                shuffled_parents[i + 1].board_state[crossover:],
                                [shuffled_parents[i], shuffled_parents[i + 1]], self.generation + 1)
            child2 = Individual(shuffled_parents[i + 1].board_state[:crossover]
                                + shuffled_parents[i].board_state[crossover:],
                                [shuffled_parents[i], shuffled_parents[i + 1]], self.generation + 1)
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

    def find_fittest(self):
        fittest: Individual = self.population[0]
        for individual in self.population:
            if individual.fitness > fittest.fitness:
                fittest = individual
        return fittest


def plot_average_fitness(generation_list, average_fitness_list, population_list, mutation_percent):
    plt.plot(generation_list, average_fitness_list)
    plt.xlabel('Generation')
    plt.ylabel('Average Fitness')
    plt.title(f'\n8 Queens Genetic Algorithm\nPopulation: {population_list}, Mutation Rate: {mutation_percent}%')
    plt.show()


def plot_maximum_fitness(generation_list, most_fit_list, population_list, mutation_percent):
    plt.plot(generation_list, most_fit_list)
    plt.xlabel('Generation')
    plt.ylabel('Maximum Fitness')
    plt.title(f'\n8 Queens Genetic Algorithm\nPopulation: {population_list}, Mutation Rate: {mutation_percent}%')
    plt.show()


population = int(input("Population size: "))
mutation_rate = float(input("Mutation percent: "))
num_iterations = int(input("Number of iterations: "))
print()

initial_epoch = Epoch(population, 0, non_attacking_queens_fitness_function, mutation_rate)
epochs = [initial_epoch]
generation = [0]
average_fitness = [initial_epoch.average_fitness]
most_fit = [initial_epoch.fittest_individual]
highest_fitness = [initial_epoch.fittest_individual.fitness]

for i in range(0, num_iterations):
    generation.append(i)
    new_epoch = epochs[i].create_new_generation()
    epochs.append(new_epoch)
    average_fitness.append(new_epoch.average_fitness)
    most_fit.append(new_epoch.fittest_individual)
    highest_fitness.append(new_epoch.fittest_individual.fitness)


print('Maximum fitness achieved: ' + max(highest_fitness))

print('Fittest individual from each epoch:')
for each in most_fit:
    print(str(each.board_state))

plot_average_fitness(generation, average_fitness, population, mutation_rate)
plot_maximum_fitness(generation, highest_fitness, population, mutation_rate)

