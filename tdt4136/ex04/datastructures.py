# -*- coding: utf-8 -*-
"""
This module contains the classes data representation
"""
import logging
from random import shuffle, randint
from copy import deepcopy

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

        left_up = []
        right_up = []

        # For the number of adjacent diagonals in a matrix of size self.M * self.M
        for p in xrange(0, self.M * 2 - 1):

            diag_left = []
            diag_right = []

            # Dynamic boundries to prevent indexes off the matrix
            for q in xrange(max(0, p - self.M + 1), min(p, self.M - 1) + 1):
                
                # Add the right-up diags
                diag_right.append(self.matrix[p - q][q])
                # Add the left-up diags
                diag_left.append(self.matrix[p - q][self.M - 1 - q])

            # Add them to their respective lists
            if diag_left:
                left_up.append(diag_left)
            if diag_right:
                right_up.append(diag_right)

        return left_up, right_up


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
        output = [self.K - sum(x) for x in up if len(x) >= self.K]
        output.extend([self.K - sum(x) for x in down if len(x) >= self.K])

        return output

    def objective(self):
        """
        Returns a number between 0 and 1 that gives an indication of how close
        this board representation is to an optimal solution
        """

        rows = self.check_rows()
        cols = self.check_cols()
        diags = self.check_diags()
        
        # Max potential horiz and vertical board check values
        maximum = self.M * self.K

        # Concat the rows and cols to simplify things
        concat = rows + cols

        # Check axes with available slots. Also check axes that overflow
        # Sum up to a total value.
        available_slots = 0
        overflow = 0
        for x in concat:
            if x < 0:
                overflow += x
            else:
                available_slots += x

        available_slots = available_slots + abs(overflow)

        # Check for overflow in diagonals
        diag_overflow = 0
        for x in diags:
            if x < 0:
                diag_overflow += x

        # If we're at maximum eggs, return that shining numero uno
        if available_slots == 0 and diag_overflow == 0:
            return 1.0

        # Define the o value. Need to double the max value to account for overlap
        o = 1.0 - (float(available_slots) / float(maximum * 2))

        # Penalize if there are diagonal overflows
        if diag_overflow != 0:
            if abs(diag_overflow) == 1:
                o = o - 0.1
            else:
                o = o * (1.0 / abs(diag_overflow) * 0.67)

        return o

    def create_random_board(self):
        """
        This method inserts the maximum allowed eggs onto the board
        and shuffles the rows.
        """
        
        # Create a clean baord
        self.create_matrix(self.M, self.N)

        # Add some random eggs in there
        for row in self.matrix:
            for i in xrange(self.K):
                row[i] = 1
            shuffle(row)

    def create_neighbors(self, n):
        """
        Returns a list of n neighbor boards
        """

        # Create empty neighbor list
        neighbors = []

        neighbor = deepcopy(self)

        # Yield a range of 0,n-1
        for x in xrange(0, n):

            # If we have reached the desired neighbor number, exit the loop
            if len(neighbors) == n:
                break

            # Deepcopy the current neighbor
            neighbor = deepcopy(neighbor)

            rows = neighbor.get_rows()
            cols = neighbor.get_cols()

            # Flag to check if there has been any shuffles
            modifications = False

            # Iterate through, and potentially shuffle rows
            row_overflow = []
            row_underflow = []
            for i, row in enumerate(rows):
                if sum(row) > self.K:
                    # If we have overflow in a row, extract coords that affect it
                    indexes = []
                    for j, val in enumerate(row):
                        if val == 1:
                            indexes.append(j)
                    index = randint(0, len(indexes) - 1)
                    row_overflow.append((i, index))
                elif sum(row) < self.K:
                    indexes = []
                    for j, val in enumerate(row):
                        if val == 0:
                            indexes.append(j)
                    index = randint(0, len(indexes) - 1)
                    row_underflow.append((i, index))
            
            # Swap overflows with underflows
            if row_overflow:
                y, x = row_overflow[randint(0, len(row_overflow) - 1)]
                dy, dx = row_underflow[randint(0, len(row_underflow) - 1)]
                neighbor.matrix[y][x] = 0
                neighbor.matrix[dy][dx] = 1
                modifications = True
                neighbors.append(neighbor)

            # If there has not been modifications to fix row overflow, check column overflow
            if not modifications:
                for i, col in enumerate(cols):
                    if sum(col) > 2:
                        temp_indexes = []
                        for j, val in enumerate(col):
                            if val == 1:
                                temp_indexes.append(j)
                        shuffle_index = randint(0, len(temp_indexes) - 1)
                        shuffle(neighbor.matrix[shuffle_index])
                        neighbors.append(neighbor)
                        modifications = True
                        break
            
            # If there has not been any modifications to the current neighbor, meaning
            # that we only have overflows in diagonals, just return add a random board
            if not modifications:
                neighbor.create_random_board()
                neighbors.append(neighbor)
                modifications = True

        return neighbors

    def pretty_matrix(self):
        return '\n'.join([repr(row) for row in self.matrix])

    def __str__(self):
        return '### Board\n' + self.pretty_matrix() + '\n\n' + \
            repr(self.check_rows()) + '\n' + \
            repr(self.check_cols()) + '\n' + \
            repr(self.check_diags()) + '\n' + \
            'Objective value: %f' % self.objective() + '\n'
        

class PegBoard(AbstractBoard):
    """
    Specialized PegBoard representation
    """

    def __init(self, rows, cols, D, W):
        self.D = D
        self.W = W
        self.create_matrix(rows, cols)
