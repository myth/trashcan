# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/19/16

import logging
import random
import settings


class GeneticOperator(object):

    @staticmethod
    def mutate(genotype):
        """
        This genetic operator performs mutations on a genotype
        :param genotype: A bit vector
        """

        pos = random.randint(0, settings.GENOME_LENGTH - 1)
        logging.getLogger(__name__).debug('Mutation occurred in pos %d' % pos)
        genotype[pos] = not bool(genotype[pos])

    @staticmethod
    def crossover(genotype_one, genotype_two):
        """
        This genetic operator performs crossover on a pair of genotypes
        """

        s = random.randint(0, settings.GENOME_LENGTH - 1)
        logging.getLogger(__name__).debug('Crossover occurred in pos %d' % s)

        return genotype_one[:s] + genotype_two[s:], genotype_two[:s] + genotype_one[s:]


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
