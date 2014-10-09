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
        self.M = None
        self.N = None

    def create_matrix(self, rows, cols):
        """
        Generate an empty matrix of M rows and N cols
        """
        self.M = rows
        self.N = cols
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

        for x in xrange(self.N):
            colsum = 0
            for y in xrange(self.M):
                colsum += self.matrix[y][x]
            cols.append(self.K - colsum)

        return cols

    def check_diags(self):
        """
        Returns the delta of eggs in each diagonal compared to K
        """

        diags = []
        output = []

        # For the number of diagonals in a matrix of size self.M * self.M
        for p in xrange(0, 2 * self.M - 1):

            diag_up = []
            diag_down = []

            # Dynamic boundries to prevent indexes off the matrix
            for q in xrange(max(0, p - self.M + 1), min(p, self.M - 1)):
                
                # Add the right-upward diags
                diag_up.append(self.matrix[p - q][q])
                # Add the right-downward diags
                diag_down.append(self.matrix[p - q][self.M - 1 - q])

            diags.append(diag_up)
            diags.append(diag_down)

        # Remove diagonals of size less than K for simplicity,
        # and add diagonal sum to output.
        for x in xrange(len(diags)):
            if len(diags[x]) < self.K:
                continue
            else:
                output.append(sum(diags[x]))

        return output

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
        return repr(self.matrix) + '\n' + \
            repr(self.check_rows()) + '\n' + \
            repr(self.check_cols()) + '\n' + \
            repr(self.check_diags()) + '\n' + \
            'Objective value: %f' % self.objective()
        

class PegBoard(AbstractBoard):
    """
    Specialized PegBoard representation
    """

    def __init(self, rows, cols, D, W):
        self.D = D
        self.W = W
        self.create_matrix(rows, cols)
