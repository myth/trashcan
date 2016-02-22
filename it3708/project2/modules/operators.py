# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/19/16

from logging import getLogger
import numpy as np
import random
import settings


class GeneticOperator(object):

    @staticmethod
    def mutate(genotype):
        """
        This genetic operator performs mutations on a genotype
        :param genotype: A numpy bit vector
        """

        pos = random.randint(0, len(genotype) - 1)
        getLogger(__name__).debug('Mutation has occured in %s in position %d' % (genotype, pos))
        genotype[pos] = not bool(genotype[pos])

    @staticmethod
    def crossover(genotype_one, genotype_two):
        """
        This genetic operator performs crossover on a pair of genotypes
        """

        new_genotype_one = np.array([])
        new_genotype_two = np.array([])
        points = settings.GENOME_CROSSOVER_POINTS
        step = int(len(genotype_one) / ((points + 1) * 2))  # We want to divide into N equal steps, and skip every other
        for x in range(0, len(genotype_one), step):
            new_genotype_one = np.append(new_genotype_one, genotype_two[x:x + step])
            new_genotype_two = np.append(new_genotype_two, genotype_one[x:x + step])

        genotype_one = new_genotype_one
        genotype_two = new_genotype_two

        return genotype_one, genotype_two


# Phenotype representation functions

class Phenotype(object):

    @staticmethod
    def translate_genotype_to_phenotype(genotype):
        """
        Translates a genotype representation into a phenotype representation
        :param genotype: A numpy bit array
        :return: A Phenotype representation of the genotype
        """

        return settings.PHENOTYPE_FUNCTION(genotype)

    @staticmethod
    def bitstring_phenotype(genotype):
        """
        Translates a genotype into a bitstring phenotype
        :param genotype: A numpy bit array
        :return: A phenotype represented as a string of bit values (0 or 1)
        """

        return ''.join(map(str, map(int, genotype)))
