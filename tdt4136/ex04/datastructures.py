# -*- coding: utf-8 -*-
"""
This module contains the classes data representation
"""
import logging

class AbstractBoard(object):
    """
    Abstract board representation
    """

    def __init__(self):
        self.matrix = None
        self.parent = None

    def create_matrix(self, rows, cols):
        """
        Generate an empty matrix of M rows and N cols
        """

        self.matrix = [[0 for col in range(cols)] for row in range(rows)]


class EggCarton(AbstractBoard):
    """
    Specialized EggCarton board representation
    """

    def __init__(self, rows, cols, K):
        self.K = K
        self.create_matrix(rows, cols)

    def check_rows(self):
        """
        Returns the delta of eggs in each row compared to K
        """

        return [self.K - sum(row) for row in self.matrix]

    def check_cols(self):
        """
        Returns the delta of eggs in each row compared to K
        """

        cols = []
        n = len(self.matrix)

        for x in xrange(n):
            colsum = 0
            for y in xrange(n):
                colsum += self.matrix[y][x]
            cols.append(self.K - colsum)

        return cols

    def check_diags(self):
        """
        Returns the delta of eggs in each diagonal compared to K
        """
        diags = []
        n = len(self.matrix)

        for y in xrange(n):
            for x in xrange(n):
                a = 1

        return diags

    def objective(self):
        """
        Returns a number between 0 and 1 that gives an indication of how close
        this board representation is to an optimal solution
        """

        rows = self.check_rows()
        cols = self.check_cols()
        diags = self.check_diags()

        concat = rows + cols + diags
        total = 0
        # Max potential horiz and vertical board check values
        maximum = len(self.matrix) * self.K * 2
        # Max total list sum for right and left diags
        maximum += ((len(self.matrix) * 2 - 1) - ((self.K - 1) * 2)) * 2

        # If illegal state, return 0, else add up to see how far away we are from
        # the optimal state, total = 0, which means it is not possible to add more eggs
        # in either row, col or diag.
        for x in concat:
            if x < 0:
                return 0
            total += x

        print total
        print maximum

        if total == 0:
            return 1

        return 1.0 - (float(total) / float(maximum))

    def __str__(self):
        return repr(self.matrix) + '\n' + repr(self.check_rows()) + '\n' + repr(self.check_cols()) + '\nObjective value: %f' % self.objective()
        

class PegBoard(AbstractBoard):
    """
    Specialized PegBoard representation
    """

    def __init(self, rows, cols, D, W):
        self.D = D
        self.W = W
        self.create_matrix(rows, cols)
