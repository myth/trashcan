# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/19/16

import settings
from modules.flatland import Agent, FlatLand
from modules.nnet import NeuralNetwork


class Fitness(object):

    @staticmethod
    def one_max(phenotype):
        """
        OneMax problem fitness function
        :param phenotype: The phenotype representation of a primitive genotype (Bitstring)
        :return: The fitness value of this phenotype (correct / optimal)
        """

        solution = settings.ONEMAX_SOLUTION
        fitness = 1 / (1 + sum(phenotype[i] != solution[i] for i in range(settings.GENOME_LENGTH)))

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
                elif phenotype[i] == '0' and i < z:  # if we are on a 0-streak, check for Z boundary
                    fitness += 1
                else:
                    break
                prev = phenotype[i]
            else:
                break

        return fitness / settings.GENOME_LENGTH

    @staticmethod
    def surprising_sequence(phenotype):
        """
        Locally surprising sequence fitness function
        :param phenotype: A phenotype representation of a primitive genotype (bitstring)
        :return: The fitness value of this phenotype
        """

        local = settings.SURPRISING_SEQUENCE_LOCAL
        p = phenotype
        l = len(p)

        # Produce a list of AXB string triplets representing local or global sequences in the provided phenotype
        seq = ['%d-%d-%d' % (p[a], b-a, p[b]) for a in range(0, l) for b in range(a + 1, min(a + 2, l) if local else l)]

        return len(set(seq)) / len(seq)

    @staticmethod
    def flatland_agent(phenotype, agent):
        """
        FlatLand Agent fitness function runs 60 timesteps in the neural network.
        :param phenotype: The phenotype representation (Weight tensor nodes)
        :return: The accumulated fitness of the agent
        """

        nn = NeuralNetwork()
        nn.set_weights(phenotype)

        nn.test(agent, timesteps=settings.DEFAULT_TRAIN_TIMESTEPS)

        return agent.fitness
