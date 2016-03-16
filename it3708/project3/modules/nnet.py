# -*- coding: utf8 -*-
#
# Created by 'myth' on 3/14/16

import logging
import math

import numpy as np
import settings


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

    def __init__(self, nodes, activation_function=ActivationFunction.relu, weights=None):
        """
        Construct a Layer of N nodes, and an optional input reference
        :param nodes: The number of nodes in the layer
        :param activation_function: Which activation function the layer should apply
        """

        self.tensor = np.zeros(nodes, dtype='float')

        # Add weight presets of we have them provided, otherwise uniform random from -0.5 to 0.5
        if weights is not None:
            self.weights = weights
        else:
            self.weights = np.random.uniform(-.5, .5, nodes)

        # Only softmax is a array-wide function
        if activation_function is ActivationFunction.softmax:
            self.af = activation_function
        else:
            self.af = np.vectorize(activation_function)

    def fire(self, incoming):
        """
        Fire signals
        """

        if not isinstance(incoming, np.ndarray):
            incoming = np.array(incoming)

        # Set value of each node as the weighted average of all incoming signals
        for i in range(len(self.tensor)):
            self.tensor[i] = (incoming.sum() / len(incoming)) * self.weights[i]

        self.tensor = self.af(self.tensor)

        return self.tensor


class NeuralNetwork(object):
    """
    A NeuralNetwork is a wrapper for a series of layers
    """

    def __init__(self, net=None, afs=None):
        """
        Constructs a NeuralNetwork with the provided structure. The structure argument must be a tuple on the
        following form: (no_input, no_hidden, no_hidden2, ..., no_output)
        """

        self.log = logging.getLogger(__name__)

        if net is None:
            net = settings.NETWORK_STRUCTURE
        if afs is None:
            afs = settings.ACTIVATION_FUNCTIONS

        structure = net.copy()
        activation_functions = afs.copy()
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

    def test(self, inputs):
        """
        Test the output of
        """

        self._send_signal(inputs)

        return self._output

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

    def _send_signal(self, inputs):
        """
        Send a signal of inputs through the layers
        :param inputs: A list of input values
        """

        inputs = np.array(inputs, dtype='float')
        for i, layer in enumerate(self._net):
            layer.fire(inputs)
            inputs = layer.tensor
