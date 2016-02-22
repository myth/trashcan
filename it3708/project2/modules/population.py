# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/19/16

import itertools
from logging import getLogger
from modules.operators import GeneticOperator
from modules.operators import Phenotype
import numpy as np
from random import choice, random
import settings


class Individual(object):
    """
    An individual containing a genome
    """

    next_id = itertools.count().__next__

    def __init__(self, genotype=None, genome_length=None, fitness=0, generation=0):
        """
        Constructor
        """

        self.ID = self.next_id()
        if genome_length:
            self.genotype = np.random.random_integers(0, 1, genome_length)
        else:
            self.genotype = genotype
        self.fitness = fitness
        self.generation = generation

    def mutate(self):
        """
        Performs a mutation operation
        """

        if random() < settings.GENOME_MUTATION_RATE:
            GeneticOperator.mutate(self.genotype)

    def crossover(self, other):
        """
        Performs a crossover operation
        """

        self.genotype, other.genotype = GeneticOperator.crossover(self.genotype, other.genotype)

    def diversity(self, other):
        """
        Calculates the diversity of this individual compared to another
        """

        if self is other:
            return 0

        return sum(a != b for a in self.genotype for b in other.genotype) / len(self.genotype)

    def translate(self):
        """
        Translates this individual's genotype into a phenotype representation
        """

        return Phenotype.translate_genotype_to_phenotype(self.genotype)

    def __str__(self):
        """
        String representation of this indiviudal"
        """

        return "Individual[%d] (F:%.9f) %s" % (self.ID, self.fitness, self.translate())

    def __repr__(self):
        """
        Object representation
        """

        return self.__str__()


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
        self._log.info('Generating a population of %d individuals with genome length %d' % (
            population_size,
            genome_length
        ))
        self.loop = evolution_loop

        # Initialize a population size of given genome length as random values, and
        # round to nearest integer
        self.individuals = set()
        for i in range(population_size):
            self.individuals.add(Individual(genome_length=genome_length))

    def add_individual(self, individual):
        """
        Adds an individual to the population, and removes one of the five oldest individuals if full.
        :param individual: An Individual object
        """

        if individual not in self.individuals:
            if self.size < settings.MAX_POPULATION_SIZE:
                self.individuals.add(individual)
            else:
                self.individuals.remove(choice(sorted(list(self.individuals), key=lambda i: i.generation)[:5]))

    def add_individuals(self, individuals):
        """
        Adds a group of individuals to the population, and removes the corresponding number of oldest individuals
        from the population if it is full.
        :param individuals: A list of Individual objects
        """

        diff = settings.MAX_POPULATION_SIZE - self.size - len(individuals)
        if diff > 0:
            self.individuals.update(individuals)
        else:
            # Remove the oldest
            diff = abs(diff)
            for i in sorted(list(self.individuals), key=lambda x: x.generation)[:diff]:
                self.individuals.remove(i)
            # Add the new ones
            self.individuals.update(individuals)

    @property
    def size(self):
        """
        Returns the number of individuals in this population
        :return: The number of individuals in this population as an integer
        """

        return len(self.individuals)

    @property
    def avg_fitness(self):
        """
        Returns the average fitness of the individuals in this population
        :return: The average fitness level as a floating point number
        """

        if self.size == 0:
            return 0

        return sum(p.fitness for p in self.individuals) / self.size

    def get_random_individual(self):
        """
        Returns the genotype of a random individual
        :return: A Individual object
        """

        return choice(self.individuals)

    def get_most_fit(self):
        """
        Returns the most fit individuals in the population
        :return: The most fit individual
        """

        if self.individuals:
            return max(self.individuals, key=lambda x: x.fitness)
        return None

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
