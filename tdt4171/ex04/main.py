# -*- coding=utf-8 -*-

import math
from random import randint, random


class Node:
    """
    Node object. You know, like trees
    """

    def __init__(self, label, i=0):
        self.label = label
        self.children = {}
        self.ID = i

    def __str__(self):
        """
        String representation of this node
        :return: This node and its children as a string
        """

        return 'Node[%d] Label: %d' % (self.ID, self.label)

    def __repr__(self):
        """
        Representational form of this Npde
        :return: Delegates to __str__
        """

        return self.__str__()


class DecisionTreeLearning(object):
    """
    Implementation class for DecisionTreeLearning
    """

    def __init__(self):
        self.training = get_data()
        self.testing = get_data(training=False)
        self.random = False
        self.tree = None
        self.id_counter = 0

    def classify(self, obj):
        """
        Attempts to classify an object
        :param obj: An example attribute vector
        :return: The class which the object most likely has
        """

        root = self.tree
        while root.children:
            root = root.children[obj[root.label]]

        return root.label

    def test(self):
        """
        Perform a complete test on the entire test set.
        :return: The correctness score of this test
        """
        total_correct = 0
        for example in self.testing:
            result = self.classify(example)
            correct = result == example[-1]
            if correct:
                total_correct += 1
            print('Classifying %s ... Result: %d, Correct: %s' % (example, result, correct))

        return total_correct / len(self.testing)

    def train(self):
        """
        Train this decision tree
        """

        self.tree = self._dtl(self.training, list(range(1, 8)), list())

        return self.tree

    @staticmethod
    def _check_classifiability(examples):
        """
        Checks if all objects are of same class in example set
        :param examples: A list of example pbjects
        :return: True of all are same class, False otherwise
        """

        tot = sum((o[-1] for o in examples))

        return tot == 0 or tot == len(examples)

    def _dtl(self, examples, attributes, parent_examples):
        """
        Internal algorithm implementation
        :param examples: Example set
        :param attributes: Attribute vector
        :param parent_examples: Parent level example superset
        :return: A tree
        """

        self.id_counter += 1

        if not examples:
            return Node(plurality_value(parent_examples), self.id_counter)
        elif self._check_classifiability(examples):
            return Node(examples[0][-1], self.id_counter)
        elif sum(attributes) == 0:
            return Node(plurality_value(examples), self.id_counter)
        else:
            a = 1 + self._importance(examples, attributes)
            tree = Node(a, self.id_counter)

            for i in range(2):
                subset_examples = list(filter(lambda x: x[a] == i, examples))
                subtree = self._dtl(subset_examples, attributes, examples)
                tree.children[i] = subtree

            return tree

    def _importance(self, examples, attributes):
        """
        Calculate importance from examples and attributes
        :param examples: A list of example objects
        :param attributes: An attribute vector
        :return: The index of the most important attribute
        """

        if self.random:
            return argmax(0 if a == 0 else random() for a in attributes)
        else:
            return argmax(importance(a, examples) for a in attributes)

    def __str__(self):
        """
        String representation of this DecisionTreeLearner
        :return: A string
        """

        output = '--- Decision Tree ---------\n'
        stack = [(self.tree, 0)]
        while stack:
            n, i = stack.pop()
            output += '\t' * i + '- %s\n' % n

            if n.children:
                for x in n.children.values():
                    stack.append((x, i+1))

        return output


def argmax(sequence):
    """
    Returns the index of the highest valued element in the sequence
    :param sequence: An iterable object
    :return: An integer representing the highest value position in the sequence
    """

    top = 0
    best = -float('Inf')
    for i, x in enumerate(sequence):
        if x > best:
            top = i
            best = x

    return top


def b(q):
    """
    Calculate the B value from the book
    :param q: The probability of q
    :return:
    """

    if not q:
        return 0
    if q == 1:
        return 1

    return -(q * math.log2(q) + (1 - q) * math.log2(1 - q))


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


def importance(a, examples):
    """
    Calculate the importance of attribute A, given an example set
    :param examples: A list of example objects
    :param a: An attribute
    :return: A list of importance values
    """

    if a == 0:
        return 0

    tot = len(examples)
    tot_pos = sum(i[-1] for i in examples)
    tot_neg = tot - tot_pos

    j = list(filter(lambda x: x[a], examples))
    k = list(filter(lambda x: not x[a], examples))

    total_entropy = 0
    for obj in (j, k):
        p = len(list(filter(lambda o: o[-1], obj)))
        n = len(list(filter(lambda o: not o[-1], obj)))
        e = (p + n) / (tot_pos + tot_neg)
        total_entropy += e * b(p / (p + n))

    return b(tot_pos / (tot_pos + tot_neg)) - total_entropy


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
        return randint(0, 1)


def hierarchy_pos(G, root, width=1.0, vert_gap=0.05, vert_loc=0, xcenter=0.2, pos=None, parent=None):
    """
    If there is a cycle that is reachable from root, then this will see infinite recursion.
    """
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    neighbors = G.neighbors(root)
    if parent is not None:
        neighbors.remove(parent)
    if len(neighbors) != 0:
        dx = width / len(neighbors)
        nextx = xcenter - width / 2 - dx / 2
    for neighbor in neighbors:
        nextx += dx
        pos = hierarchy_pos(
            G, neighbor, width=dx, vert_gap=vert_gap,
            vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
            parent=root
        )
    return pos


def main():
    """
    Main method
    """

    dtl = DecisionTreeLearning()
    print('Random Importance')
    dtl.random = True
    dtl.train()
    print(dtl)
    score = dtl.test()

    print('\nRandom test score: %.2f\n' % score)

    print('Entropy Importance')
    dtl.random = False
    dtl.train()
    print(dtl)
    score = dtl.test()

    print('\nInformation Gain test score: %.2f\n' % score)

if __name__ == "__main__":
    main()
