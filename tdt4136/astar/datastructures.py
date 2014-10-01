# -*- coding: utf-8 -*-
"""
This module contains the classes for Board and Node objects
"""
from itertools import product
import logging

class Board(object):
    """
    A board is a representation of a text file, and contains a matrix of Node objects
    :param board:
    """

    def __init__(self, board):
        """
        Initialize the board by creating the matrix
        """
        self.matrix = self.make_matrix(board)
        self.graph = self.make_graph(self.matrix)

    @staticmethod
    def make_matrix(board):
        """
        This function returns a matrix of Nodes based on an input string
        :param board:
        """

        # Create the initial character matrix
        matrix = [list(line) for line in board.split('\n')]

        # Transform to Node matrix
        for y in xrange(len(matrix)):
            for x in xrange(len(matrix[y])):
                matrix[y][x] = Node(x=x, y=y, c=matrix[y][x])

        return matrix

    def make_graph(self, matrix):
        """
        Create a dictionary of the nodes in the board matrix
        :param matrix: A two dimensional list of Node objects
        """

        graph = {}

        top = 0
        left = 0
        right = len(matrix[0]) - 1
        bottom = len(matrix) - 1

        logging.debug('Creating graph: %d,%d,%d,%d' % (left, top, right, bottom))

        for y in xrange(top, bottom):
            for x in xrange(left, right):
                graph[matrix[y][x]] = []
                for i, j in product([-1, 0, 1], [-1, 0, 1]):
                    if not (left <= x + i < right): continue
                    if not (top <= y + j < bottom): continue

                    graph[matrix[y][x]].append(matrix[y+j][x+i])

        return graph

    def get_start(self):
        """
        Returns coordinates for the starting node
        """

        return self.get_point('A')

    def get_goal(self):
        """
        Returns coordinates for det goal node
        """

        return self.get_point('B')

    def get_point(self, node):
        """
        This function returns the x and y coordinates for a given node
        :param node: An instance of Node
        """
        for y in xrange(len(self.matrix)):
            for x in xrange(len(self.matrix[y])):
                if self.matrix[y][x].c == node:
                    return self.matrix[y][x]


class Node(object):
    """
    A Node is a representation of a tile on the game grid
    :param h: Distance from this node to goal node
    :param parents: A list of parents to this node used for traversal
    :param x: The X-coordinate of this node
    :param y: The Y-coordinate of this node
    :param c: The character used in the text file to represent this node
    """

    def __init__(self, h=0, parents=None, x=None, y=None, c=None):
        """
        Initialize a Node with the given values, set some inferrable values
        at start.
        """

        # Distance from node to goal node. Using Manhattan to get this value
        self.h = h

        # Movment cost from one node to another node. Values given i exercise
        self.g = 0

        # F-value is G+H
        self.f = self.g + self.h

        # All the neighboring nodes to the current node
        self.parents = parents

        # x coordinate
        self.x = x

        # y coordinate
        self.y = y

        # Char represented in the map, '.', '#', A or B
        self.c = c

        # Is the node walkable
        if self.c == '#':
            self.walkable = False
            self.color = 'black'

        # Add some colors to other states aswell
        elif self.c == '.':
            self.color = 'green'
            self.g = 1
        elif self.c == 'A':
            self.color = 'pink'
        elif self.c == 'B':
            self.color = 'red'
        else:
            self.walkable = True

            # Establish weights and colors
            if self.c == 'w':
                self.g = 100
                self.color = 'blue'
            elif self.c == 'm':
                self.g = 50
                self.color = 'grey'
            elif self.c == 'f':
                self.g = 10
                self.color = 'green'
            elif self.c == 'g':
                self.g = 5
                self.color = 'lime green'
            elif self.c == 'r':
                self.g = 1
                self.color = 'brown'

    def update(self):
        """
        Update the F-value based on the G and H values
        """
        self.f = self.g + self.h

    def __eq__(self, other):
        """
        Comparable function
        """

        return self.f == other.f

    def __lt__(self, other):
        """
        Compareble function
        """

        return self.f < other.f

    def __gt__(self, other):
        """
        Comparable function
        """

        return self.f > other.f

    def manhattan(self, board):
        """
        :param board: is an instance of a board
        :return: Returning the h value for a given node
        """

        x_dest, y_dest = board.get_goal()

        xd = x_dest - self.x
        yd = y_dest - self.y

        return abs(xd) + abs(yd)

    def __unicode__(self):
        return 'Node %d,%d (%s)' % (self.x, self.y, self.c)

