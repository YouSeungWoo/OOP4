import random, copy
from network import Network
from input_layer import input_layer

class Generation():
    def __init__(self, population, keep_best, lucky_few, chance_of_mutation):
        self.genomes = []
        self.input_layers = []

        self.population = population
        self.keep_best = keep_best
        self.lucky_few = lucky_few
        self.chance_of_mutation = chance_of_mutation

    def set_initial_genomes(self, input_size):
        self.genomes = []
        input_layers = []

        for i in range(self.population):
            self.genomes.append(Network(input_size))

        for g in self.genomes:
            input_layers.append(input_layer(False))
            input_layers[-1].set_ai(g)

        return self.genomes, input_layers

    def set_genomes(self, genomes):
        self.genomes = genomes
        input_layers = []

        for g in self.genomes:
            input_layers.append(input_layer(False))
            input_layers[-1].set_ai(g)

        return input_layers

    def keep_best_genomes(self):
        self.genomes.sort(key = lambda x: x.fitness, reverse = True)
        self.best_genomes = self.genomes[: self.keep_best]
        self.genomes = copy.deepcopy(self.best_genomes[:])

    def mutations(self):
        while len(self.genomes) < self.keep_best * 4 :
            genome1 = random.choice(self.best_genomes)
            genome2 = random.choice(self.best_genomes)
            self.genomes.append(self.mutate(self.cross_over(genome1, genome2)))

        while len(self.genomes) < self.population:
            genome = random.choice(self.best_genomes)
            self.genomes.append(self.mutate(genome))

        random.shuffle(self.genomes)

        return self.genomes

    def cross_over(self, genome1, genome2):
        new_genome = copy.deepcopy(genome1)
        other_genome = copy.deepcopy(genome2)

        for k in range(len(new_genome.W)):
            cut_location = int(len(new_genome.W[k]) * random.uniform(0, 1))

            for i in range(cut_location):
                new_genome.W[k][i], other_genome.W[k][i] = other_genome.W[k][i], new_genome.W[k][i]

        return new_genome

    def mutate_weights(self, weights):
        if random.uniform(0, 1) < self.chance_of_mutation:
          return weights * (random.uniform(0, 1) - 0.5) * 3 + (random.uniform(0, 1) - 0.5)
        else:
          return 0

    def mutate(self, genome):
        new_genome = copy.deepcopy(genome)

        for k in range(len(new_genome.W)):
            new_genome.W[k] += self.mutate_weights(new_genome.W[k])

        return new_genome