# -*- coding: utf-8 -*-

import random
from numpy import append, array, dot

MAX_EPOCHS = 100


# Perceptron object

class Perceptron(object):
    def __init__(self, n=2, t=1, lrate=0.2):
        self.theta = t
        self.learning_rate = 0.2
        self.w = array([random.uniform(-0.5, 0.5) for _ in range(n)])

    def train(self, data):
        epoch = 0
        while True:
            epoch += 1
            errors = 0
            for iv, ex in data:
                result = dot(iv, self.w) > self.theta
                error = ex - result
                if error != 0:
                    errors += 1
                    self.w = array([self.w[i] + self.learning_rate * error * value for i, value in enumerate(iv)])
                    print('Weight vector changed: %s' % repr(self.w))
            if not errors or epoch > MAX_EPOCHS:
                break
        print('Training complete in %d epochs' % epoch)

# Support code

def test(p, data):
    errors = False
    for iv, ex in data:
        result = dot(iv, p.w) > p.theta
        error = ex - result
        if error != 0:
            print('Classification error on %s with output %d' % (repr(iv), ex))
            errors = True
        else:
            print('Success! on %s with output %d' % (repr(iv), ex))
    return not errors


if __name__ == '__main__':

    print('[i] --- PERCEPTRON v1.0 ----------------------')

    TOTAL_TRAINING_SESSIONS = 50
    AND = [
        (array([0, 0]), 0),
        (array([0, 1]), 0),
        (array([1, 0]), 0),
        (array([1, 1]), 1),
    ]
    OR = [
        (array([0, 0]), 0),
        (array([0, 1]), 1),
        (array([1, 0]), 1),
        (array([1, 1]), 1),
    ]

    trains = 0
    and_errors = 0
    or_errors = 0
    while trains < TOTAL_TRAINING_SESSIONS:
        trains += 1
        print('[%d] --- Training AND ---------------------' % trains)
        p_and = Perceptron(t=0.5, lrate=0.1)
        p_and.train(AND)
        print('[%d] --- Training OR --------------------- ' % trains)
        p_or = Perceptron(t=0.0, lrate=0.2)
        p_or.train(OR)

        print('[%d] --- Testing AND ----------------------' % trains)
        if not test(p_and, AND):
            and_errors += 1
        print('[%d] --- Testing OR -----------------------' % trains)
        if not test(p_or, OR):
            or_errors += 1


    print('[i] Mass train and test complete (%d iterations). Errors: AND: %d OR: %d' % (trains, and_errors, or_errors))

