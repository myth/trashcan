# -*- coding=utf-8 -*-

import math
import random


class Node(object):
    """
    Tree node
    """

    def __init__(self, label):
        self.label = label
        self.children = {}

    def __str__(self):
        """
        String representation of the tree from this node as root node
        :return: A PHP SyntaxTree string
        """

        if self.children:
            return '[%s ' % self.label + '%s]' % ''.join(str(self.children[key]) for key in self.children.keys())
        else:
            return '[%s]' % self.label


class DecisionTreeLearner(object):
    """
    Implementation Class for Decision Tree learning algorithm
    """

    def __init__(self):
        """
        Constructor
        """

        self.training = get_data()
        self.testing = get_data(training=False)
        self.root = None
        self.random = False

    def classify(self, example):
        """
        Attempt to classify an example
        :param example: An attribute vector
        :return: A class
        """

        root = self.root
        while root.children:
                root = root.children[example[root.label]]

        return root.label

    def test(self):
        """
        Test on the test set
        """

        return float(sum(map(lambda x: x[-1] == self.classify(x), self.testing))) / len(self.testing)

    def train(self):
        """
        Train on the training set
        :return: A tree root node
        """

        self.root = self._dtl(self.training, list(range(7)), list())

        return self.root

    def _dtl(self, examples, attributes, parent_examples):
        """
        Private helper that performs the recursion
        :param examples:
        :param attributes:
        :param parent_examples:
        :return:
        """

        if not examples:
            return Node(plurality_value(parent_examples))
        elif is_classifiable(examples):
            return Node(examples[0][-1])
        elif not attributes:
            return Node(plurality_value(examples))
        else:
            if self.random:
                a = random.choice(attributes[:-1])
            else:
                a = importance(examples, attributes)

            tree = Node(a)
            attributes.remove(a)

            for n in range(2):
                liste = []
                for e in examples:
                    if e[a] == n:
                        liste.append(e)
                sub_tree = self._dtl(liste, list(attributes), examples)
                tree.children[n] = sub_tree
            return tree


def get_data(training=True):
    """
    Reads the contents of either the training or test data from file
    :param training: Whether or not we are training, as opposed to testing
    :return: A list of attribute-vectors
    """

    if training:
        filename = 'data/training.txt'
    else:
        filename = 'data/test.txt'

    with open(filename) as f:
        return [list(map(lambda x: int(x) - 1, line.strip().split('\t'))) for line in f]


def plurality_value(examples):
    """
    Tie breaker function
    :param examples: A set of example objects
    """

    tot = len(examples)
    pos = sum((o[-1] for o in examples))
    neg = tot - pos

    if pos > neg:
        return 1
    elif neg > pos:
        return 0
    else:
        return random.randint(0, 1)


def is_classifiable(examples):
    """
    Check whether or not a set of examples all are of the same class
    :param examples: A list of attribute vectors
    :return: True if classified, False otherwise
    """

    tot = sum(x[-1] for x in examples)

    if tot == 0 or tot == len(examples):
        return True
    return False


def b(q):
    """
    The B function
    :param q: The input probability
    :return: The B value
    """

    if q == 0:
        return q
    else:
        return -(q * math.log(q, 2) + (1.0 - q) * math.log((1.0 - q), 2))


def importance(examples, attributes):
    """
    Analyze which attribute is of highest importance in order to create a good split
    :param examples: The example set
    :param attributes: The attribute vector
    :return: An attribute index (vector position)
    """

    values = {a: b(sum(x[a] == examples[0][a] for x in examples) / len(examples)) for a in attributes}

    index, val = min(values.items())

    return index


def main():
    """
    Main application method
    """

    dtl = DecisionTreeLearner()
    dtl.random = True
    for x in range(5):
        dtl.train()
        print('Score: %.2f' % (dtl.test() * 100))
    print(dtl.root)

    dtl.random = False
    for x in range(5):
        dtl.train()
        print('Score: %.2f' % (dtl.test() * 100))
    print(dtl.root)

main()
