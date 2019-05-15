import numpy as np
import random as rand
from operator import attrgetter

from food_source import FoodSource


class ABC(object):

    food_sources = []

    def __init__(self, npopulation, nruns, fn_eval, *, trials_limit=100, fn_lb,
        fn_ub):

        super(ABC, self).__init__()
        self.npopulation = npopulation
        self.nruns = nruns
        self.fn_eval = fn_eval
        self.trials_limit = trials_limit
        self.fn_lb = np.array(fn_lb)
        self.fn_ub = np.array(fn_ub)
        self.food_source_history = []

        self.employed_bees = round(npopulation/2)
        self.onlooker_bees = npopulation - self.employed_bees

        self.fitness_assessment = 0

    def optimize(self,funcao):
        self.initialize()
        best_fs = self.best_source()
        i=0
        while i < self.nruns:
            if self.fitness_assessment <= 500000:
                for nrun in range(0, self.npopulation):
                    self.employed_bees_stage()
                    self.onlooker_bees_stage()
                    self.scout_bees_stage()

                for food in self.food_sources:
                    if(food!=None and funcao != None):
                        food.fitnessreal = funcao(food.solution)
                        pass
                best_fs = self.best_source()
                self.food_source_history.append(best_fs.fitnessreal)
                i += 1
            else:
                break
        return best_fs.solution


    def initialize(self):
        self.food_sources = [self.create_foodsource() for i in range(self.employed_bees)]

    def employed_bees_stage(self):
        for i in range(self.employed_bees):
            food_source = self.food_sources[i]
            new_solution = self.generate_solution(i)
            best_solution = self.best_solution(food_source.solution, new_solution)

            self.set_solution(food_source, best_solution)

    def onlooker_bees_stage(self):
        for i in range(self.onlooker_bees):
            probabilities = [self.probability(fs) for fs in self.food_sources]
            selected_index = self.selection(range(len(self.food_sources)), probabilities)
            selected_source = self.food_sources[selected_index]
            new_solution = self.generate_solution(selected_index)
            best_solution = self.best_solution(selected_source.solution, new_solution)

            self.set_solution(selected_source, best_solution)

    def scout_bees_stage(self):
        for i in range(self.employed_bees):
            food_source = self.food_sources[i]

            if food_source.trials > self.trials_limit:
                food_source = self.create_foodsource()


    def generate_solution(self, current_solution_index):
        solution = self.food_sources[current_solution_index].solution
        k_source_index = self.random_solution_excluding([current_solution_index])
        k_solution = self.food_sources[k_source_index].solution
        d = rand.randint(0, len(self.fn_lb) - 1)
        r = rand.uniform(-1, 1)

        new_solution = np.copy(solution)
        new_solution[d] = solution[d] + r * (solution[d] - k_solution[d])

        return np.around(new_solution, decimals=4)

    def random_solution_excluding(self, excluded_index):
        available_indexes = set(range(self.employed_bees))
        exclude_set = set(excluded_index)
        diff = available_indexes - exclude_set
        selected = rand.choice(list(diff))

        return selected

    def best_solution(self, current_solution, new_solution):
        if self.fitness(new_solution) > self.fitness(current_solution):
            return new_solution
        else:
            return current_solution

    def probability(self, solution_fitness):
        fitness_sum = sum([fs.fitness for fs in self.food_sources])
        probability = solution_fitness.fitness / fitness_sum

        return probability

    def fitness(self, solution):
        result = self.fn_eval(solution)
        self.fitness_assessment += 1
        if result >= 0:
            fitness = 1 / (1 + result)
        else:
            fitness = 1 + abs(result)

        return fitness

    def selection(self, solutions, weights):
        return rand.choices(solutions, weights)[0]

    def set_solution(self, food_source, new_solution):
        if np.array_equal(new_solution, food_source.solution):
            food_source.trials += 1
        else:
            food_source.solution = new_solution
            food_source.trials = 0

    def best_source(self):
        best = max(self.food_sources, key=attrgetter('fitness'))

        return best

    def create_foodsource(self):
        solution = self.candidate_solution(self.fn_lb, self.fn_ub)
        fitness = self.fitness(solution)

        return FoodSource(solution, fitness)

    def candidate_solution(self, lb, ub):
        r = rand.random()
        solution = lb + (ub - lb) * r

        return np.around(solution, decimals=4)