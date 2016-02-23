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

        fitness = 1.0 / (1.0 + sum(int(phenotype[i] != solution[i]) for i in range(settings.GENOME_LENGTH)))

        return fitness
