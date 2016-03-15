# -*- coding: utf8 -*-
#
# Created by 'myth' on 3/14/16

import logging
import math
import random

import numpy as np
import settings
from modules.flatland import LEFT, RIGHT, UP


class ActivationFunction(object):
    """
    Activation functions
    """

    @staticmethod
    def relu(x):
        """
        Relu
        """

        return max(x, .0)

    @staticmethod
    def softmax(x):
        """
        Softmax
        """

        return np.exp(x) / np.sum(np.exp(x))

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def softplus(x):
        return math.log(1 + math.exp(x))


class Layer(object):
    """
    The Layer contains a weight tensor, activation function and helper methods for processing layer data
    """

    def __init__(self, nodes, activation_function=ActivationFunction.relu):
        """
        Construct a Layer of N nodes, and an optional input reference
        :param nodes: The number of nodes in the layer
        :param activation_function: Which activation function the layer should apply
        """

        self.tensor = np.zeros(nodes, dtype='float')
        self.weights = np.random.uniform(-.5, .5, nodes)
        if activation_function is ActivationFunction.softmax:
            self.af = activation_function
        else:
            self.af = np.vectorize(activation_function)

    def fire(self, tensor):
        """
        Fire signals
        """

        # If we are the input layer
        for i in range(len(self.tensor)):
            self.tensor[i] = tensor.sum() * self.weights[i]

        tot = self.tensor.sum()
        if tot:
            self.tensor /= self.tensor.sum()
        self.tensor = self.af(self.tensor)


class NeuralNetwork(object):
    """
    A NeuralNetwork is a wrapper for a series of layers
    """

    def __init__(self):
        """
        Constructs a NeuralNetwork with the provided structure. The structure argument must be a tuple on the
        following form: (no_input, no_hidden, no_hidden2, ..., no_output)
        """

        self.log = logging.getLogger(__name__)

        structure = settings.NETWORK_STRUCTURE.copy()
        activation_functions = settings.ACTIVATION_FUNCTIONS.copy()
        assert len(structure) == len(activation_functions)

        structure = list(structure)
        inputs = structure.pop(0)
        inputs_af = activation_functions.pop(0)
        outputs = structure.pop()
        outputs_af = activation_functions.pop()

        self._net = []
        self._net.append(Layer(inputs, inputs_af))
        while structure:
            self._net.append(Layer(structure.pop(0), activation_function=activation_functions.pop(0)))
        self._net.append(Layer(outputs, outputs_af))

    def send(self, inputs):
        """
        Send a signal of inputs through the layers
        :param inputs: A list of input values
        :return: A list of output values (the value of the last layer's tensor field)
        """

        inputs = np.array(inputs, dtype='float')
        for i, layer in enumerate(self._net):
            layer.fire(inputs)
            inputs = layer.tensor

    def test(self, agent, timesteps=None, record_run=False):
        """
        Train the network for N epochs
        """

        def run_test():
            if record_run:
                print(agent.flatland.board)
            for t in range(timesteps):
                results = agent.sense()
                direction = [UP, LEFT, RIGHT]

                inputs = np.array(results, dtype='float')
                for i, layer in enumerate(self._net):
                    layer.fire(inputs)
                    inputs = layer.tensor
                if record_run:
                    print(self._output)
                d = direction[np.argmax(self._output)]

                if record_run:
                    print(d)
                    print(agent.flatland.board)

                agent.move(d)

        if not timesteps:
            timesteps = settings.DEFAULT_TRAIN_TIMESTEPS

        run_test()

    def set_weights(self, weights):
        """
        Force the layer weights with the provided array
        :param weights: A list of numpy weight tensors
        """

        assert len(self._net) == len(weights)

        for i, w in enumerate(weights):
            self._net[i].weights = w

    @property
    def _input(self):
        return self._net[0].tensor

    @property
    def _output(self):
        return self._net[-1].tensor
