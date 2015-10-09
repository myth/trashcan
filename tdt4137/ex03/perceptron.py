# -*- coding: utf-8 -*-

import random


class Input(object):
    """
    A basic input class
    """

    def __init__(self):
        self.idx = None
        self.incoming = {}


class Output(Input):
    """
    A basic output class
    """

    def __init__(self):
        """
        Constructor
        """
        super(Output, self).__init__()

        self.outgoing = set()

    def connect(self, other):
        """
        Connects this output to an input-ready entity
        """

        if self.idx is None:
            raise ValueError('This output entity has no ID and cannot connect to another entity')

        # Add a connection from this output-entity to an input-entity
        self.output.add(other)
        # Add this output entity as a connection on the input-entity with no value
        other.incoming[self.idx] = None


class Neuron(Output):
    """
    A Neuron is a simulated nerve cell
    """

    def __init__(self, idx, theta, activation_function=lambda x: 1 if x >= 0 else 0):
        """
        Constructor
        """
        super(Neuron, self).__init__()

        # IDX is this neurons identifier
        self.idx = idx
        # Theta is the signal threshold and can be used to shift the decision boundary
        self.theta = theta
        # Activation function decides what signal strength the neuron should fire
        self.activation_function = activation_function
        # Weights hold the current weighting factors for each input neuron
        self.weights = {}
        # Maintains the latest output given from this neuron
        self.output = None

    def init_weights(self):
        """
        Sets random weights on all incoming connections (dendrites) for this neuron
        """

        for idx in self.incoming.keys():
            self.weights[idx] = random.uniform(-0.5, 0.5)

    def fire(self):
        """
        Triggers a signal fire evaluation of the incoming values
        """

        self.output = sum(float(value) * self.weights[idx] for idx, value in self.incoming.items())
        self.output = self.output - self.theta
        self.output = self.activation_function(self.output)

        for axon in self.outgoing:
            axon.receive(self, self.output)

    def receive(self, neuron, value):
        """
        Receives a signal from an input neuron
        """

        if neuron.idx not in self.incoming:
            raise KeyError('The specified input neuron is not registered as a dendrite to this neuron')

        self.incoming[neuron.idx] = value

    def __str__(self):
        return 'Neuron %d with weights %s and output %.5f' % (self.idx, ', '.join('%s=%.3f' % (idx, w) for idx, w in self.weights.items()), self.output)


class Perceptron(Neuron):
    """
    The Perceptron is the first and one of the most simple artificial neural network training algorithms
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor
        """

        super(Perceptron, self).__init__(*args, **kwargs)

        self.name = 'Gunnar'

    def train(self, learning_rate=0.1, training_data=[((1, 1), 1)], max_epochs=50):
        """
        Trains the perceptron given the input pairs and expected results given the input pairs.
        Will run for the amount of iterations given in epochs.
        """

        i = 0
        unconverged = True
        while unconverged:

            if i > max_epochs:
                break

            print('[TRAIN] Epoch %d started ... ' % i)

            errors = False

            for inputs, expected in training_data:
                x1, x2 = inputs

                self.incoming['x1'] = x1
                self.incoming['x2'] = x2

                if 'x1' not in self.weights or 'x2' not in self.weights:
                    self.init_weights()

                # Fire neuron
                self.fire()

                for idx, weight in self.weights.items():
                    """
                    The new weight is adjusted by the learning rate times the error corrected original value
                    """

                    diff = float(expected - self.output)
                    if diff != 0:
                        correction = float(learning_rate) * float(self.incoming[idx]) * float(expected - self.output)
                        self.weights[idx] += correction

                # If we detected discrepancies, set error flag
                if self.output != expected:
                    errors = True

            if not errors:
                # If no errors from training set this epoch, we assume convergence
                break
            else:
                # Move on to next epoch
                i += 1


if __name__ == '__main__':
    p_and = Perceptron(1, 0.2)
    p_or = Perceptron(2, 0.2)
    p_xor = Perceptron(3, 0.2)
    p_nand = Perceptron(4, 0.2)

    print('--- TRAINING ----------------------')

    AND = [
        ((0, 0), 0),
        ((1, 0), 0),
        ((0, 1), 0),
        ((1, 1), 1),
    ]

    OR = [
        ((0, 0), 0),
        ((1, 0), 1),
        ((0, 1), 1),
        ((1, 1), 1),
    ]

    XOR = [
        ((0, 0), 0),
        ((1, 0), 1),
        ((0, 1), 1),
        ((1, 1), 0),
    ]

    NAND = [
        ((0, 0), 1),
        ((1, 0), 1),
        ((0, 1), 1),
        ((1, 1), 0),
    ]

    print('Training AND')
    p_and.train(training_data=AND)
    print('Training OR')
    p_or.train(training_data=OR)
    print('Training XOR')
    p_xor.train(training_data=XOR)
    print('Training NAND')
    p_nand.train(training_data=NAND)

    print('--- TESTING -----------------------')

    for p in [p_and, p_or, p_xor, p_nand]:

        if p is p_and:
            td = AND
            print('Testing AND')
        elif p is p_or:
            td = OR
            print('Testing OR')
        elif p is p_xor:
            td = XOR
            print('Testing XOR')
        else:
            td = NAND
            print('Testing NAND')

        for payload in td:
            inputs, expected = payload
            x1, x2 = inputs

            p.incoming['x1'] = x1
            p.incoming['x2'] = x2

            p.fire()

            if p.output == expected:
                print('[i] Inputs %d and %d gave correct result of %f' % (x1, x2, p.output))
            else:
                print('[i] Inputs %d and %d gave incorrect result of %f' % (x1, x2, p.output))

