# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/19/16

import settings


class Fitness(object):

    @staticmethod
    def one_max(phenotype):
        """
        OneMax problem fitness function
        :param phenotype: The phenotype representation of a primitive genotype (Bitstring)
        :return: The fitness value of this phenotype (1 / SSE)
        """

        solution = settings.ONEMAX_SOLUTION
        fitness = 1.0 / (1.0 + sum(phenotype[i] != solution[i] for i in range(settings.GENOME_LENGTH)))

        return fitness

    @staticmethod
    def lolz_prefix(phenotype):
        """
        LOLZ prefix fitness function
        :param phenotype: The phenotype representation of a primitive genotype (bitstring)
        :return: The fitness value of this phenotype (points / genome_length)
        """

        fitness = 1
        z = settings.LOLZ_PREFIX_Z
        prev = phenotype[0]
        for i in range(1, len(phenotype)):
            if phenotype[i] == prev:
                if phenotype[i] == '1':
                    fitness += 1
                elif phenotype[i] == '0' and i < z:
                    fitness += 1
                else:
                    break
                prev = phenotype[i]
            else:
                break

        return fitness / settings.GENOME_LENGTH

    @staticmethod
    def local_surprising_sequence(phenotype):
        """
        Locally surprising sequence fitness function
        :param phenotype: A phenotype representation of a primitive genotype (bitstring)
        :return: The fitness value of this phenotype
        """

        fitness = 0.0

        return fitness

    @staticmethod
    def global_surprising_sequence(phenotype):
        """
        Globally surprising sequence fitness function
        :param phenotype: A phenotype representation of a primitive genotype (bitstring)
        :return: The fitness value of this phenotype
        """

        fitness = 0.0

        return fitness
