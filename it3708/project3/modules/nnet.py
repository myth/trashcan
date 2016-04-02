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


class Neuron(object):
    """
    The Neuron contains a set of input weights for all incoming axions
    """

    def __init__(self, weights, activation_function=ActivationFunction.relu):
        """
        Construct a Neuron with weights
        :param weights: A numpy array of weights, also indicating the number of incoming connections
        """

        self.weights = weights
        self.output = 0

        # Only softmax is a array-wide function
        if activation_function is ActivationFunction.softmax:
            self.af = activation_function
        else:
            self.af = np.vectorize(activation_function)

    def fire(self, incoming):
        """
        Fire a signal from this neuron, base on incoming axions
        :param incoming: An array of signals coming into this Neuron
        """

        # Set value of each node as the weighted average of all incoming signals
        self.output = self.af(np.sum(self.weights * incoming))

    def __str__(self):
        """
        String representation of this neuron
        """

        return 'Neuron output: %.3f Weights: %s' % (self.output, self.weights)


class Layer(object):
    """
    Base class for Layer objects
    """

    def __init__(self):
        """
        Constructor
        """

        self.neurons = []

    def __str__(self):
        """
        String representation of this layer
        """

        return '--- Layer ---\n%s' % ('\n'.join(str(n) for n in self.neurons))


class InputLayer(Layer):
    """
    This layer has no weigts on the neurons
    """

    def __init__(self, nodes):
        """
        Construct a Layer of N nodes, and an optional input reference
        :param nodes: The number of nodes in the layer
        """

        super(InputLayer, self).__init__()

        # Create dem neurons
        for n in range(nodes):
            self.neurons.append(Neuron(None))

    @staticmethod
    def fire(incoming):
        """
        Fire a signal to all the neurons in this layer (Assumes full connectivity).
        :param incoming: An array of signals coming into this layer
        """

        return np.array(incoming)


class StandardLayer(Layer):
    """
    The Layer contains neurons and a fire method for processing neurons
    """

    def __init__(self, nodes, incoming, activation_function=ActivationFunction.relu):
        """
        Construct a Layer of N nodes, and an optional input reference
        :param nodes: The number of nodes in the layer
        :param incoming: The number of incoming axions to each node
        :param activation_function: Which activation function the layer should apply
        """

        super(StandardLayer, self).__init__()

        # Only softmax is a array-wide function
        if activation_function is not ActivationFunction.softmax:
            activation_function = np.vectorize(activation_function)

        # Create dem neurons
        for n in range(nodes):
            weights = np.random.uniform(-.5, .5, incoming)
            self.neurons.append(Neuron(weights, activation_function=activation_function))

    def fire(self, incoming):
        """
        Fire a signal to all the neurons in this layer (Assumes full connectivity).
        :param incoming: An array of signals coming into this layer
        """

        return np.array([neuron.fire(incoming) for neuron in self.neurons], dtype='float')


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

        self._net = []

        inputs = structure.pop(0)
        self._net.append(InputLayer(inputs))
        while structure:
            outputs = structure.pop(0)
            inputs_af = activation_functions.pop(0)
            self._net.append(
                StandardLayer(
                    outputs,
                    len(self._net[-1].neurons),
                    activation_function=inputs_af
                )
            )

        # Store the final layer activation functions
        self._output_af = activation_functions.pop(0)
        if self._output_af is not ActivationFunction.softmax:
            self._output_af = np.vectorize(self._output_af)

    def test(self, inputs):
        """
        Test the output of a set of input signals
        :param inputs: An array of input signals
        """

        return self._send_signal(inputs)

    def set_weights(self, weights):
        """
        Force the layer weights with the provided array
        :param weights: A numpy array of weights
        """

        start = 0
        for layer in self._net[1:]:
            for neuron in layer.neurons:
                step = len(neuron.weights)
                neuron.weights = weights[start:start + step]
                start += step

    def _send_signal(self, inputs):
        """
        Send a signal of inputs through the layers
        :param inputs: A list of input values
        """

        for layer in self._net:
            inputs = layer.fire(inputs)

        return self._output_af(inputs)

    def __str__(self):
        """
        String representation of this Neural Network
        """

        return '=== NeuralNetwork ===\n%s' % '\n'.join(layer for layer in self._net)
