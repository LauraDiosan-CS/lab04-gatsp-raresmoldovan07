import random
import itertools
import math


class Solver(object):

    POPULATION_SIZE = 100
    sys_random = random.SystemRandom()

    def __init__(self, filename):
        self.__inputFile = filename
        file_data = filename.split('.')
        self.__outputFile = file_data[0] + '_solution.' + file_data[1]
        try:
            open(self.__outputFile, 'w')
        except FileNotFoundError:
            print('File not found')

    def get_random_permutation(self, list_sample):
        for i in range(len(list_sample)):
            self.sys_random.seed(a=None, version=2)
            x = self.sys_random.randrange(len(list_sample))
            y = self.sys_random.randrange(len(list_sample))
            while x == y:
                y = self.sys_random.randrange(len(list_sample))
            list_sample[x], list_sample[y] = list_sample[y], list_sample[x]
        return list_sample

    def modularity(self, permutation, graph):
        cost = 0
        for i in range(len(permutation) - 1):
            cost += graph[permutation[i]][permutation[i + 1]]
        cost += graph[permutation[-1]][permutation[0]]
        return cost

    def get_permutation_based_representation(self, graph):
        p_list = [i for i in range(len(graph))]
        permutation = self.get_random_permutation(p_list)
        return permutation

    def population_initialization(self, graph):
        population = []
        for i in range(self.POPULATION_SIZE):
            chromosome = self.get_permutation_based_representation(graph)
            while self.modularity(chromosome, graph) == 0 or chromosome in population:
                chromosome = self.get_permutation_based_representation(graph)
            population.append(chromosome)
        return population

    def natural_selection(self, population, graph):
        return sorted(population, key=lambda x: self.modularity(x, graph))[:self.POPULATION_SIZE]

    def sort_selection(self, population, graph):
        return sorted(population, key=lambda x: self.modularity(x, graph))

    def turnir_selection(self, population, graph):
        random_list = []
        nr = len(population) // 10
        if nr < 2:
            nr = 2
        for i in range(nr):
            rand = random.choice(population)
            while rand in random_list:
                self.sys_random.seed(a=None, version=2)
                rand = self.sys_random.choice(population)
            random_list.append(rand)
        random_list = self.sort_selection(random_list, graph)
        return random_list[0], random_list[1]

    def cross_over(self, population, graph, number_of_sons):
        for son in range(number_of_sons):
            chromosome1, chromosome2 = self.turnir_selection(population, graph)
            start = self.sys_random.choice([i for i in range(len(chromosome1) // 2)])
            stop = start + len(chromosome1) // 2
            new_chromosome = [-1 for i in range(len(chromosome1))]
            for i in range(start, stop):
                new_chromosome[i] = chromosome1[i]
            i = stop
            j = stop
            nr = len(chromosome1) - len(chromosome1) // 2
            while nr > 0:
                if chromosome2[j] not in new_chromosome:
                    new_chromosome[i] = chromosome2[j]
                    i += 1
                    nr -= 1
                j += 1
                if i == len(chromosome2):
                    i = 0
                if j == len(chromosome2):
                    j = 0
            population.append(new_chromosome)
        return population

    def swap_mutation(self, population):
        new_population = []
        for i in range(len(population)):
            chromosome = []
            chromosome += population[i]
            self.sys_random.seed(a=None, version=2)
            chance = self.sys_random.choice([0, 1])
            if chance == 1 or i < len(population) // 2:
                x = self.sys_random.randrange(len(chromosome))
                y = self.sys_random.randrange(len(chromosome))
                while x == y:
                    y = self.sys_random.randrange(len(chromosome))
                aux = chromosome[x]
                chromosome[x] = chromosome[y]
                chromosome[y] = aux
            new_population.append(chromosome)
        return new_population

    def get_best_chromosome(self, population, graph):
        best_fitness = 1000000
        solution = []
        index = 0
        for i in range(len(population)):
            p = population[i]
            if self.modularity(p, graph) < best_fitness:
                best_fitness = self.modularity(p, graph)
                solution = p
                index = i
        return solution, index

    def solve(self, graph):
        self.POPULATION_SIZE = 3
        steps = 200
        best_fitness = 1000000
        population = self.population_initialization(graph)
        f = open(self.__outputFile, 'w')
        for step in range(steps):
            population = self.cross_over(population, graph, 1)
            population_after_mutation = self.swap_mutation(population)
            selected_population = self.natural_selection(population_after_mutation, graph)
            best_chromosome, index = self.get_best_chromosome(selected_population, graph)
            new_fitness = self.modularity(best_chromosome, graph)
            # for p in selected_population:
            #     print(str(p ) + str(self.modularity(p, graph))

            if new_fitness < best_fitness:
                f.write("Solutie optima gasita la pasul " + str(step) + "\n")
                f.write("Costul soltuiei: " + str(new_fitness) + "\n")
                f.write(str(best_chromosome) + "\n")
                f.write("\n")
                best_fitness = new_fitness

            population = selected_population
