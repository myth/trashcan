# -*- coding: utf-8 -*-

import random
from numpy import append, array, dot


class Perceptron(object):
    def __init__(self, t=0.2, lrate=0.2, bias=1):
        self.theta = t
        self.learning_rate = 0.2
        self.bias = array([1])
        self.w = array([random.uniform(-0.5, 0.5) for _ in range(3)])

    def train(self, data):
        epoch = 0
        while True:
            epoch += 1
            errors = 0
            for iv, ex in data:
                result = dot(append(self.bias, iv), self.w) > self.theta
                error = ex - result
                if error != 0:
                    errors += 1
                    self.w = array([self.w[i] + self.learning_rate * error * value for i, value in enumerate(append(self.bias, iv))])
                    print('Weight vector changed: %s' % repr(self.w))

            if not errors:
                break

        print('Training complete in %d epochs' % epoch)


def test(p, data):
    for iv, ex in data:
        result = dot(append(p.bias, iv), p.w) >= p.theta
        error = ex - result
        if error != 0:
            print('Classification error on %s with output %d' % (repr(iv), ex))
        else:
            print('Success! on %s with output %d' % (repr(iv), ex))


if __name__ == '__main__':
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

    print('--- Training AND ---------------------')
    p_and = Perceptron(t=0.2, lrate=0.2)
    p_and.train(AND)
    print('--- Training OR --------------------- ')
    p_or = Perceptron(t=0.2, lrate=0.2)
    p_or.train(OR)

    print('--- Testing AND ----------------------')
    test(p_and, AND)
    print('--- Testing OR -----------------------')
    test(p_or, OR)

