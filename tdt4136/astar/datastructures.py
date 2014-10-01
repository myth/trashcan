# -*- coding: utf-8 -*-
"""
This module contains the classes for Board and Node objects
"""
from itertools import product
from math import sqrt
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

    @staticmethod
    def make_graph(matrix):
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

        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                
                # If it is not walkable, just ignore it
                if not matrix[y][x].walkable:
                    continue
                
                # Initialize an empty neighbor list
                graph[matrix[y][x]] = []

                # Make a cartesian product of adjacent Nodes.
                # Ignores self, out of bounds, diagonals and non-walkables
                for i, j in product([-1, 0, 1], [-1, 0, 1]):
                    if i == 0 and j == 0:
                        continue
                    if not (left <= (x + i) <= right):
                        continue
                    if not (top <= (y + j) <= bottom):
                        continue
                    if abs(i) + abs(j) > 1:
                        continue
                    try:
                        if not matrix[y+j][x+i].walkable:
                            continue
                    except IndexError:
                        continue

                    graph[matrix[y][x]].append(matrix[y+j][x+i])

        return graph

    def create_h_values(self):
        """
        Sets the manhattan distance to the end node
        """

        end = self.get_goal()

        for node in self.graph:
            node.h = sqrt((node.x - end.x)**2 + (node.y - end.y)**2)

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
    :param parent: A list of parents to this node used for traversal
    :param x: The X-coordinate of this node
    :param y: The Y-coordinate of this node
    :param c: The character used in the text file to represent this node
    """

    def __init__(self, h=0, parent=None, x=None, y=None, c=None):
        """
        Initialize a Node with the given values, set some inferrable values
        at start.
        """

        # Distance from node to goal node. Using Manhattan to get this value
        self.h = h

        # Movment cost from one node to another node. Values given i exercise
        self.g = 0

        # Cost to move to this node
        self.arc_cost = 0

        # F-value is G+H
        self.f = self.g + self.h

        # The previous node visited before this one
        self.parent = parent

        # x coordinate
        self.x = x

        # y coordinate
        self.y = y

        # Char represented in the map, '.', '#', A or B
        self.c = c

        self.walkable = True

        # Is the node walkable
        if self.c == '#':
            self.walkable = False
            self.color = 'black'
            self.arc_cost = 100000

        # Add some colors to other states aswell
        elif self.c == '.':
            self.color = 'green'
            self.arc_cost = 1
        elif self.c == 'A':
            self.color = 'pink'
        elif self.c == 'B':
            self.color = 'red'

        else:

            # Establish weights and colors
            if self.c == 'w':
                self.arc_cost = 100
                self.color = 'blue'
            elif self.c == 'm':
                self.arc_cost = 50
                self.color = 'grey'
            elif self.c == 'f':
                self.arc_cost = 10
                self.color = 'green'
            elif self.c == 'g':
                self.arc_cost = 5
                self.color = 'lime green'
            elif self.c == 'r':
                self.arc_cost = 1
                self.color = 'brown'

    def set_g(self, new_g):
        """
        Update the G-value
        """
        self.g = new_g

    def update_f(self):
        """
        Updates the F value of this node
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

    def __unicode__(self):
        return 'Node %d,%d (%s)' % (self.x, self.y, self.f)

    def __repr__(self):
        return 'Node %d,%d (%s)' % (self.x, self.y, self.f)

    def __str__(self):
        return 'Node %d,%d (%s)' % (self.x, self.y, self.f)
