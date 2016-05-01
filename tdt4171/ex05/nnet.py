# -*- coding: utf-8 -*-

import math
import random
import copy


# The transfer function of neurons, g(x)
def log_func(x):
    return 1.0 / (1.0+math.exp(-x))


# The derivative of the transfer function, g'(x)
def log_func_derivative(x):
    return math.exp(-x)/(pow(math.exp(-x)+1, 2))


# Initializes a matrix of all zeros
def make_matrix(i, j):
    m = []
    for x in range(i):
        m.append([0] * j)
    return m


class NN(object):
    """
    NeuralNetwork implementation class
    """

    def __init__(self, num_inputs, num_hidden, learning_rate=0.001):
        # Inputs: number of input and hidden nodes. Assuming a single output node.
        # +1 for bias node: A node with a constant input of 1. Used to shift the transfer function.
        self.num_inputs = num_inputs + 1
        self.num_hidden = num_hidden

        # Current activation levels for nodes (in other words, the nodes' output value)
        self.input_activation = [1.0] * self.num_inputs
        self.hidden_activations = [1.0] * self.num_hidden
        self.output_activation = 1.0  # Assuming a single output.
        self.learning_rate = learning_rate

        # create weights
        # A matrix with all weights from input layer to hidden layer
        self.weights_input = make_matrix(self.num_inputs, self.num_hidden)

        # A list with all weights from hidden layer to the single output neuron.
        self.weights_output = [0 for i in range(self.num_hidden)]  # Assuming single output

        # set them to random vaules
        for i in range(self.num_inputs):
            for j in range(self.num_hidden):
                self.weights_input[i][j] = random.uniform(-0.5, 0.5)
        for j in range(self.num_hidden):
            self.weights_output[j] = random.uniform(-0.5, 0.5)

        # Data for the backpropagation step in RankNets.
        # For storing the previous activation levels (output levels) of all neurons
        self.prev_input_activations = []
        self.prev_hidden_activations = []
        self.prev_output_activation = 0

        # For storing the previous delta in the output and hidden layer
        self.prev_delta_output = 0
        self.prev_delta_hidden = [0 for i in range(self.num_hidden)]
        # For storing the current delta in the same layers
        self.delta_output = 0
        self.delta_hidden = [0 for i in range(self.num_hidden)]

    def propagate(self, inputs):
        if len(inputs) != self.num_inputs - 1:
            raise ValueError('wrong number of inputs')

        # input activations
        self.prev_input_activations = copy.deepcopy(self.input_activation)
        for i in range(self.num_inputs - 1):
            self.input_activation[i] = inputs[i]
        self.input_activation[-1] = 1  # Set bias node to -1.

        # hidden activations
        self.prev_hidden_activations = copy.deepcopy(self.hidden_activations)
        for j in range(self.num_hidden):
            tot = 0.0
            for i in range(self.num_inputs):
                # print self.ai[i] ," * " , self.wi[i][j]
                tot += self.input_activation[i] * self.weights_input[i][j]
            self.hidden_activations[j] = log_func(tot)

        # output activations
        self.prev_output_activation = self.output_activation
        tot = 0.0
        for j in range(self.num_hidden):
            tot += self.hidden_activations[j] * self.weights_output[j]
        self.output_activation = log_func(tot)

        return self.output_activation

    def compute_output_delta(self):
        # TODO: Implement the delta function for the output layer (see exercise text)

        pass

    def compute_hidden_delta(self):
        # TODO: Implement the delta function for the hidden layer (see exercise text)

        pass

    def update_weights(self):
        # TODO: Update the weights of the network using the deltas (see exercise text)

        pass

    def backpropagate(self):
        self.compute_output_delta()
        self.compute_hidden_delta()
        self.update_weights()

    # Prints the network weights
    def weights(self):
        print('Input weights:')
        for i in range(self.num_inputs):
            print(self.weights_input[i])
        print()
        print('Output weights:')
        print(self.weights_output)

    def train(self, patterns, iterations=1):
        # TODO: Train the network on all patterns for a number of iterations.
        # To measure performance each iteration: Run for 1 iteration, then count misordered pairs.
        # TODO: Training is done  like this (details in exercise text):
        # - Propagate A
        # - Propagate B
        # - Backpropagate

        pass

    def count_misordered_pairs(self, patterns):
        # TODO: Let the network classify all pairs of patterns. The highest output determines the winner.
        # for each pair, do
        # Propagate A
        # Propagate B
        # if A>B: A wins. If B>A: B wins
        # if rating(winner) > rating(loser): numRight++
        # else: numMisses++
        # end of for

        # TODO: Calculate the ratio of correct answers:
        # errorRate = numMisses/(numRight+numMisses)

        pass
