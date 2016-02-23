# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/21/16

from abc import abstractmethod, ABC
import logging
from modules.evolution import EvolutionLoop
import random
import settings


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
        self.pool.extend(self.loop.children.sorted()[:settings.MAX_POPULATION_SIZE])

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
        num = 0
        for i in self.loop.children.sorted():
            self.pool.append(i)
            num += 1
            if num == settings.MAX_POPULATION_SIZE:
                break
        self.loop.adults.individuals.extend(self.pool)

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
        num = 0
        for i in sorted(self.pool, key=lambda x: x.fitness, reverse=True):
            self.loop.adults.individuals.append(i)
            num += 1
            if num == settings.MAX_POPULATION_SIZE:
                break
        self.loop.children.individuals.clear()

        return self.pool


# Parent Selection

class ParentSelection(AbstractSelection):
    """
    Parent Selection abstract base class
    """

    def __init__(self, *args, **kwargs):
        """
        Constructpr
        """

        super(ParentSelection, self).__init__(*args, **kwargs)

    @abstractmethod
    def select(self):
        """
        Selects a set of individuals for the pool from a Population object
        :return: This ParentSelection object, with an up to date pool
        """

        return self


class FitnessProportionate(ParentSelection):
    """
    Selects a set of individuals for reproduction
    """

    def select(self):
        log = logging.getLogger(__name__)


class SigmaScaling(ParentSelection):
    """
    Selects a set of individuals for reproduction
    """

    def select(self):
        pass


class TournamentSelection(ParentSelection):
    """
    Selects a set of individuals for reproduction
    """

    log = logging.getLogger(__name__)

    def select(self):
        self.pool.clear()
        individuals = self.loop.adults.individuals[:]
        random.shuffle(individuals)
        while individuals:
            local_group = list()
            for i in range(settings.TOURNAMENT_SELECTION_K):
                try:
                    candidate = individuals.pop()
                except IndexError:
                    break
                local_group.append(candidate)

            if random.random() < 1 - settings.TOURNAMENT_SELECTION_EPSILON:
                winner = max(local_group, key=lambda x: x.fitness)
            else:
                winner = random.choice(list(local_group))
            self.pool.append(winner)
            if settings.ENABLE_LOGGING:
                self.log.debug('Selected %s from local group for mating' % winner)

        return self.pool


class RankedDiversitySelection(ParentSelection):
    """
    Selects a set of individuals for reproduction
    """

    def select(self):
        pass
