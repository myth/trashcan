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

        for x in xrange(len(self.matrix[0])):
            colsum = 0
            for y in xrange(len(self.matrix)):
                colsum += self.matrix[y][x]
            cols.append(colsum)

        return cols

    def check_diags(self):
        """
        Returns the delta of eggs in each diagonal compared to K
        """
        return []
        

class PegBoard(AbstractBoard):
    """
    Specialized PegBoard representation
    """

    def __init(self, rows, cols, D, W):
        self.D = D
        self.W = W
        self.create_matrix(rows, cols)
