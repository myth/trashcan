# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/19/16

import itertools
from logging import getLogger
from random import randint, random

import settings

from modules.flatland import Agent
from modules.operators import GeneticOperator, Phenotype


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
        self.dirty = True
        self.invulnerable = False
        if genome_length:
            self.genotype = [randint(0, settings.WEIGHT_GRANULARITY - 1) for i in range(settings.GENOME_LENGTH)]
        else:
            self.genotype = genotype[:]

        self.generation = generation
        self.fitness = 0.0
        self.phenotype = None

    def crossover(self, other):
        self.dirty = True
        other.dirty = True
        self.genotype, other.genotype = GeneticOperator.crossover(self.genotype, other.genotype)

    def mutate(self):
        # Reset invulnerability and return if we are in an non-mutating mode
        if self.invulnerable:
            self.invulnerable = False
            return

        # Check for single index mutation
        if random() < settings.GENOME_MUTATION_RATE:
            self.dirty = True
            GeneticOperator.int_mutate(self.genotype, m=settings.WEIGHT_GRANULARITY)

        # Check for component mutation
        if random() < settings.GENOME_COMPONENT_MUTATION_RATE:
            self.dirty = True
            GeneticOperator.int_component_mutate(self.genotype, m=settings.WEIGHT_GRANULARITY)

    def translate(self):
        """
        Translates this individual's genotype into a phenotype representation
        """

        if self.dirty:
            self.phenotype = Phenotype.translate_genotype_to_phenotype(self.genotype)
            self.dirty = False

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
            ind = Individual(genome_length=genome_length)
            self.individuals.append(ind)

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
            # Set the nnet weights to current pheno:
            self.loop.nn.set_weights(i.translate())

            # Run agent trough each flatland scenario in settings and set the accumulated fitness
            i_tot_fitness = 0
            for fs in range(settings.FLATLAND_SCENARIOS):
                fl = settings.FLATLANDS[fs]
                agent = Agent(flatland=fl)
                agent.run(self.loop.nn, timesteps=settings.FLATLAND_TIMESTEPS)
                i_tot_fitness += agent.fitness

            i.fitness = i_tot_fitness

            if not most_fit:
                most_fit = i
            if i.fitness > most_fit.fitness:
                most_fit = i
            tot_fitness += i.fitness

        self.avg_fitness = tot_fitness / self.size
        self.std_dev = sum(map(lambda x: (x.fitness - self.avg_fitness)**2, self.individuals)) / self.size
        self.most_fit = most_fit

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
