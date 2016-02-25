# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/19/16

from copy import deepcopy
import itertools
from logging import getLogger
from modules.fitness import Fitness
from modules.operators import GeneticOperator
from modules.operators import Phenotype
import numpy as np
from random import choice, random, randint
import settings


class Individual(object):
    """
    An individual containing a genome
    """

    next_id = itertools.count().__next__

    def __init__(self, genotype=None, genome_length=None, generation=0):
        """
        Constructor
        """

        self.ID = self.next_id()
        if genome_length:
            self.genotype = np.random.random_integers(0, 1, genome_length)
            self.genotype = [int(i) for i in self.genotype]
        else:
            self.genotype = genotype[:]
        self.generation = generation
        self.fitness = 0.0
        self.phenotype = self.translate()

    def mutate(self):
        """
        Performs a mutation operation
        """

        if random() < settings.GENOME_MUTATION_RATE:
            GeneticOperator.mutate(self.genotype)
            self.phenotype = self.translate()

        if random() < settings.GENOME_COMPONENT_MUTATION_RATE:
            GeneticOperator.component_mutate(self.genotype)
            self.phenotype = self.translate()

    def crossover(self, other):
        """
        Performs a crossover operation
        """

        self.genotype, other.genotype = GeneticOperator.crossover(self.genotype, other.genotype)
        self.translate()
        other.translate()

    def diversity(self, other):
        """
        Calculates the diversity of this individual compared to another
        """

        if self is other:
            return 0

        e = 0
        for i, val in enumerate(self.genotype):
            e += int(val == other.genotype[i])

        return 1 / (1 + e)

    def translate(self):
        """
        Translates this individual's genotype into a phenotype representation
        """

        self.phenotype = Phenotype.translate_genotype_to_phenotype(self.genotype)
        self.fitness = settings.FITNESS_FUNCTION(self.phenotype)

        return self.phenotype

    def __str__(self):
        """
        String representation of this indiviudal"
        """

        return "Individual[%d] (F:%f) %s" % (self.ID, self.fitness, self.phenotype)

    def __repr__(self):
        """
        Object representation
        """

        return self.__str__()


class IntIndividual(Individual):
    def __init__(self, genotype=None, generation=0):
        if genotype:
            super(IntIndividual, self).__init__(
                genotype=deepcopy(genotype),
                generation=generation
            )
        else:
            super(IntIndividual, self).__init__(
                genotype=[randint(0, settings.SURPRISING_SEQUENCE_S - 1) for i in range(settings.GENOME_LENGTH)]
            )

    def mutate(self):
        if random() < settings.GENOME_MUTATION_RATE:
            GeneticOperator.int_mutate(self.genotype, m=settings.SURPRISING_SEQUENCE_S)
            self.phenotype = self.translate()

        if random() < settings.GENOME_COMPONENT_MUTATION_RATE:
            GeneticOperator.int_component_mutate(self.genotype, m=settings.SURPRISING_SEQUENCE_S)
            self.phenotype = self.translate()

    def crossover(self, other):
        self.genotype, other.genotype = GeneticOperator.crossover(self.genotype, other.genotype)
        self.translate()
        other.translate()


class Population(object):
    """
    A population of genotypes
    """

    def __init__(self, population_size, genome_length, evolution_loop=None):
        """
        Constructor
        :param population_size: The total amount of individuals in the population
        :param genome_length: The length of the genotype of each individual
        :return: A population object
        """

        self._log = getLogger(__name__)
        if settings.ENABLE_LOGGING:
            self._log.info('Generating a population of %d individuals with genome length %d' % (
                population_size,
                genome_length
            ))
        self.loop = evolution_loop
        self.avg_fitness = 0.0
        self.std_dev = 0.0
        self.most_fit = None

        # Initialize a population size of given genome length as random values, and
        # round to nearest integer
        self.individuals = list()
        for i in range(population_size):
            if settings.FITNESS_FUNCTION is Fitness.surprising_sequence:
                self.individuals.append(IntIndividual())
            else:
                self.individuals.append(Individual(genome_length=genome_length))

    @property
    def size(self):
        """
        Returns the number of individuals in this population
        :return: The number of individuals in this population as an integer
        """

        return len(self.individuals)

    def update_fitness(self):
        """
        Returns the average fitness of the individuals in this population
        :return: The average fitness level as a floating point number
        """

        if self.size == 0:
            return 0

        tot_fitness = 0.0
        most_fit = None
        for i in self.individuals:
            if not most_fit:
                most_fit = i
            if i.fitness > most_fit.fitness:
                most_fit = i
            tot_fitness += i.fitness

        self.avg_fitness = tot_fitness / self.size
        self.std_dev = sum(map(lambda x: (x.fitness - self.avg_fitness)**2, self.individuals)) / self.size
        self.most_fit = most_fit

    def get_random_individual(self):
        """
        Returns the genotype of a random individual
        :return: A Individual object
        """

        return choice(self.individuals)

    def get_n_most_fit(self, n=5):
        """
        Returns a list of the N most fit individuals in the population
        :return: A list of individals with the highest fitness
        """

        return list(self.sorted())[:n]

    def sorted(self):
        """
        Returns a sorted list of the individuals in this population
        :return: A sorted list of Individuals
        """

        return sorted(self.individuals, key=lambda x: x.fitness, reverse=True)

    def __str__(self):
        """
        String serialization method
        :return: A representation of this Population object as a string
        """

        return "Population[%d]" % self.size
