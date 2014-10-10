# -*- coding: utf-8 -*-
"""
This module contains the classes data representation
"""
import logging
from random import shuffle

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

    def get_rows(self):
        """
        List of rows, just return the matrix
        """

        return self.matrix

    def get_cols(self):
        """
        Return a list of colums
        """

        return [[self.matrix[y][x] for y in xrange(self.M)] for x in xrange(self.N)]

    def get_diags(self):
        """
        Returns two lists of diagonals in the matrix. Right-updward and Right-downward.
        This method exploits the fact that all the exercise boards where diagonals are
        relevant are squares and not rectangles.
        """

        up = []
        down = []

        # For the number of adjacent diagonals in a matrix of size self.M * self.M
        for p in xrange(0, self.M * 2 - 1):

            diag_up = []
            diag_down = []

            # Dynamic boundries to prevent indexes off the matrix
            for q in xrange(max(0, p - self.M + 1), min(p, self.M - 1)):
                
                # Add the right-upward diags
                diag_up.append(self.matrix[p - q][q])
                # Add the right-downward diags
                diag_down.append(self.matrix[p - q][self.M - 1 - q])

            # Add them to their respective lists
            up.append(diag_up)
            down.append(diag_down)

        return up, down


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

        return [self.K - sum(col) for col in self.get_cols()]

    def check_diags(self):
        """
        Returns the delta of eggs in each diagonal compared to K
        """

        up, down = self.get_diags()

        # Remove diagonals of size less than K for simplicity,
        # and add diagonal sum to output.
        output = [sum(x) for x in up if len(x) >= self.K]
        output.extend([sum(x) for x in down if len(x) >= self.K])

        return output

    def objective(self):
        """
        Returns a number between 0 and 1 that gives an indication of how close
        this board representation is to an optimal solution
        """

        rows = self.check_rows()
        cols = self.check_cols()
        diags = self.check_diags()
        
        # TODO:

        # The actual value this method returns needs to be modified to give roughly
        # the same score for missing and too many eggs in a row, col or diag.
        # Additionally, if the overall state is invalid, it cannot be set as a
        # solution. Need to give this some more thought.

        # Preemptive check to see if diagonals have too many eggs
        for x in diags:
            if x < 0:
                return 0
        
        # Max potential horiz and vertical board check values
        maximum = self.M * self.K

        # Concat the rows and cols to simplify things
        concat = rows + cols

        # If illegal state, return 0, else add up to see how far away we are from
        # the optimal state, total = 0, which means it is not possible to add more eggs
        # in either row, col or diag.
        available_slots = 0
        for x in concat:
            if x < 0:
                return 0
            available_slots += x

        # If we're at maximum eggs, return that shining numero uno
        if available_slots == 0:
            return 1

        # Define the o value. Need to double the max value to account for overlap
        o = 1.0 - (float(available_slots) / float(maximum * 2))

        # If o creeps below zero, just return zero, else the real deal
        return o if o >= 0 else 0

    def create_random_board(self):
        """
        This method inserts the maximum allowed eggs onto the board
        and shuffles the rows.
        """

        for row in self.matrix:
            for i in xrange(self.K):
                row[i] = 1
            shuffle(row)

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
