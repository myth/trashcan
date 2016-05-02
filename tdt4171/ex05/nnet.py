# -*- coding: utf-8 -*-

import math
import random


# The transfer function of neurons, g(x)
def log_func(x):
    return 1.0 / (1.0 + math.exp(-x))


# The derivative of the transfer function, g'(x)
def log_func_derivative(x):
    return math.exp(-x) / pow(math.exp(-x) + 1.0, 2)


# Initializes a matrix of all zeros
def make_matrix(i, j):
    return [[0] * j for x in range(i)]


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
        self.prev_input_activations = self.input_activation[:]  # Deepcopy
        for i in range(self.num_inputs - 1):
            self.input_activation[i] = inputs[i]
        self.input_activation[-1] = 1  # Set bias node to -1.

        # hidden activations
        self.prev_hidden_activations = self.hidden_activations[:]  # Deepcopy
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
        """
        Computes the error deltas in the output layer and updates the prev_delta_output and delta_output fields.
        :return: None
        """

        delta = self.prev_output_activation - self.output_activation
        p_ab = log_func(delta)

        self.prev_delta_output = log_func_derivative(self.prev_output_activation) * (1.0 - p_ab)
        self.delta_output = log_func_derivative(self.output_activation) * (1.0 - p_ab)

    def compute_hidden_delta(self):
        """
        Computes the error deltas in the hidden layer and updates the prev_delta_hidden and delta_hidden fields.
        :return: None
        """

        # Apply the update function on each node
        for i in range(self.num_hidden):
            # Update the previous delta array
            self.prev_delta_hidden[i] = log_func_derivative(
                self.prev_hidden_activations[i]
            ) * self.weights_output[i] * (self.prev_delta_output - self.delta_output)

            # Update the last delta array
            self.delta_hidden[i] = log_func_derivative(
                self.hidden_activations[i]
            ) * self.weights_output[i] * (self.prev_delta_output - self.delta_output)

    def update_weights(self):
        """
        Computes new weights based on error deltas and learning rate, and updates the weight arrays.
        :return: None
        """

        for ii in range(self.num_inputs):
            for hi in range(self.num_hidden):
                diff = self.learning_rate * (
                    self.prev_delta_hidden[hi] * self.prev_input_activations[ii] -
                    self.delta_hidden[hi] * self.input_activation[ii]
                )

                self.weights_input[ii][hi] += diff

        for hi in range(self.num_hidden):
            diff = self.learning_rate * (
                self.prev_hidden_activations[hi] * self.prev_delta_output -
                self.hidden_activations[hi] * self.delta_output
            )

            self.weights_output[hi] += diff

    def backpropagate(self):
        """
        Performs the backpropagation algorithm on the current state of the NN
        :return: None
        """

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

    def train(self, patterns, iterations=1, test_patterns=None):
        """
        Trains the network based on the provided patterns
        :param patterns: A list of pairs
        :param iterations: How many iterations of training on the entire pattern list
        :param test_patterns: A list of test pairs to evaluate network performance
        :return: None
        """

        for i in range(1, iterations + 1):
            print('=== Iteration: %d ============================' % i)
            for pair in patterns:
                a, b = pair

                self.propagate(a.features)
                self.propagate(b.features)
                self.backpropagate()

            print('--- Training pattern stats ------------------')
            train_error = self.count_misordered_pairs(patterns)

            if test_patterns:
                print('--- Test pattern stats ----------------------')
                test_error = self.count_misordered_pairs(test_patterns)

                yield train_error, test_error

            else:
                yield train_error

    def count_misordered_pairs(self, patterns):
        """
        Calculate the amount of pairs that are place in incorrect order
        :param patterns: A list of pairs
        :return: The error rate as a fraction 0 <= x <= 1
        """

        miss = 0
        for a, b in patterns:
            if a.rating == b.rating:
                print('Equal rating, panix')

            self.propagate(a.features)
            self.propagate(b.features)

            if self.prev_output_activation > self.output_activation:
                miss += int(a.rating < b.rating)
            else:
                miss += int(b.rating < a.rating)

        print('Misordered pairs: %d' % miss)
        print('Error rate: %.3f' % (miss / len(patterns)))

        return miss / len(patterns)
