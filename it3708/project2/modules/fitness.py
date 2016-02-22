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

        solution = '1' * settings.ONEMAX_TARGET_LENGTH
        shortest = min(len(phenotype), len(solution))

        fitness = 1.0 / (1.0 + sum(phenotype[i] != solution[i] for i in range(shortest)))

        return fitness
