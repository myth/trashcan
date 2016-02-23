# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/19/16

from copy import deepcopy
from logging import getLogger
from modules.population import Individual, Population
import random
import settings


class EvolutionLoop(object):
    """
    Class that manages the evolutionary algorithm, and acts as the main
    controller class.
    """

    def __init__(self):
        """
        Constructor
        """

        self.__generation__ = 0
        self.__run__ = 0
        self.__running__ = False
        self._log = getLogger(__name__)

        self.adults = Population(0, settings.GENOME_LENGTH, evolution_loop=self)
        self.children = Population(settings.INITIAL_POPULATION_SIZE, settings.GENOME_LENGTH, evolution_loop=self)

        self.results = []

    def start(self):
        """
        Starts the evolutionary loop
        """

        if settings.ENABLE_LOGGING:
            self._log.info('Starting evolutionary loop')

        self.__running__ = True
        while self.__running__:
            self.__generation__ += 1
            if settings.ENABLE_LOGGING:
                self._log.info('Processing generation %d' % self.__generation__)

            self._update_fitness(self.children)
            self._update_fitness(self.adults)
            self._apply_adult_selection()
            # If we have found a solution at this point, (i.e fitness 1.0), just terminate
            if self.adults.most_fit and self.adults.most_fit.fitness == 1.0:
                if settings.ENABLE_LOGGING:
                    self._log.info('Success! Found solution: %s' % self.adults.most_fit)
                break
            # Print some stats
            if settings.ENABLE_LOGGING:
                self._log.info('Average fitness in population: %.5f' % self.adults.avg_fitness)
                self._log.info('Most fit individual: %s' % self.adults.most_fit)

            # Adult phase
            self._apply_age_filtering()
            parents = self._apply_parent_selection()

            # Reproductive phase
            self._reproduce(parents)
            self._apply_mutations(self.adults.individuals)
            self._apply_mutations(self.children.individuals)

            # Check if we have reached our limit
            if self.__generation__ >= settings.MAX_GENERATIONS:
                self.stop()

        return self.adults.most_fit, self.generation, self.adults.avg_fitness

    def stop(self):
        """
        Stops the evolutionary loop
        """

        if settings.ENABLE_LOGGING:
            self._log.info('Stopping evolutionary loop')
        self.__running__ = False

    @property
    def generation(self):
        """
        The number of evolution loops (generations) has passed
        :return: The current generation as an integer
        """

        return self.__generation__

    # Internals

    @staticmethod
    def _update_fitness(population):
        """
        Helper method that updates the Population's fitness table. This method uses the fitness function as
        defined in the settings file to calculate the actual values.
        """

        population.update_fitness()

    def _apply_adult_selection(self):
        """
        Helper method that invokes the adult selection class
        """

        if settings.ENABLE_LOGGING:
            getLogger(__name__).debug('Activating adult selection process')

        adults = settings.ADULT_SELECTION_CLASS(evolution_loop=self)
        adults.select()

    def _apply_age_filtering(self):
        """
        Helper method that filters out individuals based on age
        """

        if settings.ENABLE_LOGGING:
            getLogger(__name__).debug('Activating age filtering process')

        pass

    def _apply_parent_selection(self):
        """
        Helper method that invokes the parent selection class
        """

        parent_selector = settings.PARENT_SELECTION_CLASS(evolution_loop=self)
        if settings.ENABLE_LOGGING:
            getLogger(__name__).debug('Activating parent selection process with selector class %s' % parent_selector)

        return parent_selector.select()

    def _reproduce(self, pool):
        """
        Helper method that invokes a reproduction process, given a pool of selected parents
        """

        self.children.individuals.clear()
        self.children.individuals.extend(self._apply_crossover(pool))

    @staticmethod
    def _apply_mutations(pool):
        """
        Helper method that applies stochastic mutation onto the individuals in the population.
        """

        if settings.ENABLE_LOGGING:
            getLogger(__name__).debug('Applying mutations on pool')

        for individual in pool:
            individual.mutate()

    def _apply_crossover(self, pool):
        """
        Helper method that applies crossover onto pairs of parents
        """

        if settings.ENABLE_LOGGING:
            getLogger(__name__).debug('Applying crossover on pool')

        children = list()
        random.shuffle(pool)
        pool_size = len(pool)
        i = 0
        while len(children) < settings.MAX_POPULATION_SIZE:
            # Re-shuffle and reset index if we have reached the end of the pool
            if i + 2 > pool_size:
                random.shuffle(pool)
                i = 0

            try:
                # Parent clone 1
                p1 = pool[i]
                c1 = Individual(genotype=deepcopy(p1.genotype), generation=self.__generation__ + 1)
                children.append(c1)

                # Parent clone 2
                p2 = pool[i + 1]
                c2 = Individual(genotype=deepcopy(p2.genotype), generation=self.__generation__ + 1)
                children.append(c2)

                # Crossover clones as children
                if random.random() < settings.GENOME_CROSSOVER_RATE:
                    c1.crossover(c2)

                i += 2
            except IndexError:
                i = 0

        return children
