class FoodSource(object):
    trials = 0

    def __init__(self, initial_solution, initial_fitness):
        #teste = []
        super(FoodSource, self).__init__()

        self.solution = initial_solution
        self.fitness = initial_fitness
        self.fitnessreal = None
        #teste.append(self.fitness)



    def __repr__(self):
        return f'<FoodSource s:{self.solution} f:{self.fitnessreal} />'
