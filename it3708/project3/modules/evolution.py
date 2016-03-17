# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/19/16

from logging import getLogger

import settings

from modules.flatland import FOOD, POISON, FlatLand
from modules.nnet import NeuralNetwork
from modules.population import Population


class EvolutionLoop(object):
    """
    Class that manages the evolutionary algorithm, and acts as the main
    controller class.
    """

    def __init__(self):
        """
        Constructor
        """

        self.__generation__ = -1
        self.__run__ = 0
        self.__running__ = False
        self._log = getLogger(__name__)

        self.adults = Population(0, settings.GENOME_LENGTH, evolution_loop=self)
        self.children = Population(settings.MAX_CHILD_POOL_SIZE, settings.GENOME_LENGTH, evolution_loop=self)

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

            # Let the children grow up
            # Assess fitness
            self._update_fitness(self.children)
            self._apply_adult_selection()
            self._update_fitness(self.adults)

            # Print some stats
            if settings.ENABLE_LOGGING:
                self._log.info('Mean: %f Std.Dev: %f' % (self.adults.avg_fitness, self.adults.std_dev))
                self._log.info('Most fit individual: %s' % self.adults.most_fit)
            # Do some statistics gathering
            self.results.append(
                (self.__generation__, self.adults.avg_fitness, self.adults.std_dev, self.adults.most_fit.fitness)
            )

            # Adult phase
            self._apply_parent_selection()
            self._apply_mutations(self.adults.individuals)
            self._apply_mutations(self.children.individuals)

            # Check if we have reached our limit
            if self.__generation__ >= settings.MAX_GENERATIONS:
                self.stop()

        agent = self.adults.most_fit.agent
        agent.flatland = FlatLand()
        nn = NeuralNetwork()
        nn.set_weights(self.adults.most_fit.phenotype)

        nn.test(agent.sense())
        print('FOOD: %d' % agent.stats[FOOD])
        print('POISON: %d' % agent.stats[POISON])

        return self.results

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

    def _apply_parent_selection(self):
        """
        Helper method that invokes the parent selection class
        """

        parent_selector = settings.PARENT_SELECTION_CLASS(evolution_loop=self)
        if settings.ENABLE_LOGGING:
            getLogger(__name__).debug('Activating parent selection process with selector class %s' % parent_selector)

        parent_selector.select()

    @staticmethod
    def _apply_mutations(pool):
        """
        Helper method that applies stochastic mutation onto the individuals in the population.
        """

        if settings.ENABLE_LOGGING:
            getLogger(__name__).debug('Applying mutations on pool')

        for individual in pool:
            individual.mutate()
