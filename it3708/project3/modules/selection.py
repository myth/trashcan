# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/21/16

import logging
import math
import random
from abc import ABC, abstractmethod
from copy import deepcopy

import settings

from modules.evolution import EvolutionLoop
from modules.population import Individual


class AbstractSelection(ABC):
    """
    Abstract base class for selector classes
    """

    def __init__(self, evolution_loop):
        """
        Constructor that requires a reference to the evolution loop
        """

        if not isinstance(evolution_loop, EvolutionLoop):
            raise TypeError('Argument "evolution_loop" must be an instance of "EvolutionLoop"')

        self.loop = evolution_loop
        self.pool = list()


# Adult Selection

class AdultSelection(AbstractSelection):
    """
    Base AdultSelection class
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor
        """

        super(AdultSelection, self).__init__(*args, **kwargs)

    @abstractmethod
    def select(self):
        """
        Selects a set of individuals for the pool from a Population object
        :return: This AdultSelection object, with an up to date pool
        """

        return self


class FullGenerationalReplacement(AdultSelection):
    def __init__(self, *args, **kwargs):
        super(FullGenerationalReplacement, self).__init__(*args, **kwargs)

    def select(self):
        """
        Kills all existing parents and allows all children to grow up
        :return: This AdultSelection object, with an up to date pool
        """

        if settings.ENABLE_LOGGING:
            logging.getLogger(__name__).debug('ChildPoolSize: %d, AdultPoolSize: %d' % (
                self.loop.children.size,
                self.loop.adults.size
            ))

        self.loop.adults.individuals.clear()
        self.pool.clear()
        self.pool.extend(self.loop.children.sorted()[:settings.MAX_ADULT_POOL_SIZE])

        if settings.ENABLE_LOGGING:
            logging.getLogger(__name__).debug('Transferring child pool of size %d to adult pool' % len(self.pool))

        self.loop.adults.individuals.extend(self.pool)
        self.loop.children.individuals.clear()

        return self.pool


class OverProduction(AdultSelection):
    def __init__(self, *args, **kwargs):
        super(OverProduction, self).__init__(*args, **kwargs)

    def select(self):
        """
        Selects a set of individuals for the pool from a Population object
        :return: This AdultSelection object, with an up to date pool
        """

        self.pool.clear()
        self.loop.adults.individuals.clear()
        self.loop.adults.individuals.extend(self.loop.children.sorted()[:settings.MAX_ADULT_POOL_SIZE])

        # Log some information
        if settings.ENABLE_LOGGING:
            logging.getLogger(__name__).debug(
                '%d adults selected from child pool of %d' % (
                    len(self.pool),
                    self.loop.children.size
                )
            )

        # Remove all children, as they are either grown up or dead
        self.loop.children.individuals.clear()

        return self.pool


class GenerationalMixing(AdultSelection):
    def __init__(self, *args, **kwargs):
        super(GenerationalMixing, self).__init__(*args, **kwargs)

    def select(self):
        """
        Selects a set of individuals for the pool from a Population object
        :return: This AdultSelection object, with an up to date pool
        """

        self.pool.clear()
        self.pool.extend(self.loop.children.individuals)
        self.pool.extend(self.loop.adults.individuals)
        self.loop.adults.individuals.clear()
        self.loop.children.individuals.clear()
        self.loop.adults.individuals.extend(
            sorted(self.pool, key=lambda x: x.fitness, reverse=True)[:settings.MAX_ADULT_POOL_SIZE]
        )

        # Log some information
        if settings.ENABLE_LOGGING:
            logging.getLogger(__name__).debug(
                '%d adults selected from child pool of %d' % (
                    len(self.loop.adults.individuals),
                    len(self.pool)
                )
            )

        return self.pool


# Parent Selection

class ParentSelection(AbstractSelection):
    """
    Parent Selection abstract base class
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor
        """

        super(ParentSelection, self).__init__(*args, **kwargs)

    @abstractmethod
    def select(self):
        """
        Selects a set of individuals for the pool from a Population object
        :return: This ParentSelection object, with an up to date pool
        """

        return self

    def reproduce(self, parents):
        """
        Helper that produces pairs of children from pairs of parents in an ordered list
        NB: Asssumes even numbered list of parents that is of size settings.MAX_CHILD_SIZE_POOL
        :param parents: A list of parents that children should be created from
        """

        individual_class = Individual

        parents = parents[:]
        self.pool.clear()
        self.loop.children.individuals.clear()
        if settings.ENABLE_LOGGING and settings.VERBOSE_DEBUG:
            logging.getLogger(__name__).debug('Reproduce on parents list with size: %d' % len(parents))

        while parents:
            # Parent clone 1
            p1 = parents.pop()
            c1 = individual_class(genotype=deepcopy(p1.genotype), generation=p1.generation + 1)
            self.loop.children.individuals.append(c1)

            # Parent clone 2
            p2 = parents.pop()
            c2 = individual_class(genotype=deepcopy(p2.genotype), generation=p2.generation + 1)
            self.loop.children.individuals.append(c2)

            # Crossover clones as children
            if random.random() < settings.GENOME_CROSSOVER_RATE:
                c1.crossover(c2)


class FitnessProportionate(ParentSelection):
    """
    Selects a set of individuals for reproduction
    """

    def select(self):
        log = logging.getLogger(__name__)
        if settings.ENABLE_LOGGING and settings.VERBOSE_DEBUG:
            log.debug('Performing FitnessProportionate parent selection')

        self.pool.clear()
        tot_fitness = sum(i.fitness for i in self.loop.adults.individuals)
        candidates = self.loop.adults.sorted()[:]
        self.pool.append(candidates[0])

        while len(self.pool) < settings.MAX_CHILD_POOL_SIZE:
            r = random.uniform(0, 1) * tot_fitness
            i = 0
            while r - candidates[i].fitness > 0:
                r -= candidates[i].fitness
                i += 1

            # Check that we cannot add the same parent twice
            if candidates[i] is self.pool[-1]:
                continue

            self.pool.append(candidates[i])

        self.reproduce(self.pool)


class SigmaScaling(ParentSelection):
    """
    Selects a set of individuals for reproduction
    """

    def select(self):
        self.pool.clear()
        if settings.ENABLE_LOGGING and settings.VERBOSE_DEBUG:
            logging.getLogger(__name__).debug('Applying sigma scaling')

        for i in self.loop.adults.individuals:
            i.fitness *= (1 + (i.fitness - self.loop.results[i.generation][1]) / 2 * self.loop.results[i.generation][2])

        tot_fitness = sum(i.fitness for i in self.loop.adults.individuals)
        candidates = self.loop.adults.sorted()[:]
        self.pool.append(candidates[0])
        while len(self.pool) < settings.MAX_CHILD_POOL_SIZE:
            r = random.uniform(0, 1) * tot_fitness
            i = 0
            while r - candidates[i].fitness > 0:
                r -= candidates[i].fitness
                i += 1

            # Check that we cannot add the same parent twice
            if candidates[i] is self.pool[-1]:
                continue

            self.pool.append(candidates[i])

        self.reproduce(self.pool)


class TournamentSelection(ParentSelection):
    """
    Selects a set of individuals for reproduction
    """

    log = logging.getLogger(__name__)

    def select(self):
        if settings.ENABLE_LOGGING and settings.VERBOSE_DEBUG:
            self.log.debug('Starting tournament selection (K:%d, e:%.2f)' % (
                settings.TOURNAMENT_SELECTION_K,
                settings.TOURNAMENT_SELECTION_EPSILON
            ))
        self.pool.clear()

        individuals = self.loop.adults.sorted()[:]

        # If we have elitism, just add the best candidates to the pool
        for i in range(settings.ELITISM_LEVEL):
            elite = individuals.pop(0)
            elite.invulnerable = True
            if settings.ENABLE_LOGGING and settings.VERBOSE_DEBUG:
                self.log.debug('Pre-selecting elite: %s' % elite)
            self.pool.append(elite)

        # Prepare for tournament
        random.shuffle(individuals)

        # As long as there are objects left in the individuals list, generate groups of K length
        # and perform tournament selection
        while len(self.pool) < settings.MAX_CHILD_POOL_SIZE:
            local_group = list()
            for i in range(settings.TOURNAMENT_SELECTION_K):
                local_group.append(random.choice(individuals))

            # Choose best if inside threshold, else random
            if random.random() < 1 - settings.TOURNAMENT_SELECTION_EPSILON:
                winner = max(local_group, key=lambda x: x.fitness)
            else:
                winner = random.choice(list(local_group))
            self.pool.append(winner)

            if settings.ENABLE_LOGGING and settings.VERBOSE_DEBUG:
                self.log.debug('Selected %s from local group for mating' % winner)

        self.reproduce(self.pool)


class BoltzmannSelection(ParentSelection):
    """
    Selects a set of individuals for reproduction
    """

    def select(self):
        self.pool.clear()
        if settings.ENABLE_LOGGING and settings.VERBOSE_DEBUG:
            logging.getLogger(__name__).debug('Applying ranked diversity scaling')

        # Do Rank space weighting
        candidates = self.loop.adults.sorted()

        # Do boltzmann
        for i in candidates:
            numerator = math.exp(i.fitness / (1 + settings.MAX_GENERATIONS - self.loop.generation))
            denominator = math.exp(self.loop.results[i.generation][1] / (1 + settings.MAX_GENERATIONS - i.generation))
            i.fitness *= numerator / denominator

        tot_fitness = sum(i.fitness for i in candidates)
        self.pool.append(candidates[0])
        candidates.sort(key=lambda x: x.fitness, reverse=True)
        while len(self.pool) < settings.MAX_CHILD_POOL_SIZE:
            r = random.uniform(0, 1) * tot_fitness
            i = 0
            while r - candidates[i].fitness > 0:
                r -= candidates[i].fitness
                i += 1

            # Check that we cannot add the same parent twice
            if candidates[i] is self.pool[-1]:
                continue

            self.pool.append(candidates[i])

        self.reproduce(self.pool)
