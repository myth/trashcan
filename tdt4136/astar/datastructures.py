# -*- coding: utf-8 -*-

class Board:
    def __init__(self, board):
        """
        Initialize the board by creating the matrix
        """
        self.matrix = self.make_matrix(board)


    def make_matrix(self, board):
        """
        This function returns a matrix of Nodes based on an input string
        """
        
        # Create the initial character matrix
        matrix = [list(line) for line in board.split('\n')]

        # Transform to Node matrix
        for y in xrange(len(matrix)):
            for x in xrange(len(matrix[y])):
                matrix[y][x] = Node(x=x, y=y, c=matrix[y][x])

        return matrix


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
        This function returns det x and y coordinates for a given node
        """
        for x in xrange(len(self.matrix)):
            for y in xrange(len(self.matrix[x])):
                if y == node:
                    return x, y




class Node:
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
                self.color = 'lime'
            elif self.c == 'r':
                self.g = 1
                self.color = 'brown'

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

        xDest, yDest = board.get_goal()

        xd = xDest - self.x
        yd = yDest - self.y

        return abs(xd) + abs(yd)

