# Addison Wurtz
# CS 541
# Homework #2, Problem 13
# Gradient Descent Algorithm

import random
from math import sqrt

eta1 = 0.1
eta2 = 0.01
eta3 = 0.001


def problem_function(x: float, y: float):
    return 5 * (x ** 2) + 40 * x + (y ** 2) - 12 * y + 127


def calculate_neighbor(step_size, x, y) -> (float, float):
    x -= step_size * (10 * x + 40)
    y -= step_size * (2 * y + 12)
    return x,y


def gradient_descent(problem, step_size):
    current = (random.uniform(-10, 10), random.uniform(-10, 10))
    neighbor = (float, float)
    step_count = 0

    while step_count <= 500:
        step_count += 1
        neighbor = calculate_neighbor(step_size, current[0], current[1])
        if problem(neighbor[0], neighbor[1]) >= problem(current[0], current[1]):
            return current
        else:
            current = neighbor


def run_trials(step_size):
    best_solution = (100, 100)
    print("Step Size = " + str(step_size))
    for i in range(10):
        solution = gradient_descent(problem_function, eta1)

        if (problem_function(solution[0], solution[1])) < (problem_function(best_solution[0], best_solution[1])):
            best_solution = solution

    print("Best Solution: " + str(best_solution))
    print()


run_trials(eta1)
run_trials(eta2)
run_trials(eta3)




