# -*- coding: utf-8 -*-

class Board:
    def __init__(self, board):
        self.matrix = self.make_matrix(board)


    def make_matrix(self, board):
        """
        This function returns a matrix of characters based on an input string
        """

        matrix = [list(line) for line in board.split('\n')]
        return [[Node(x=x, y=y, c=y) for x in matrix for y in x]]


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
    def __init__(self, h=None, f=None, parents=None, x=None, y=None, c=None):

        #Distance from node to goal node. Using Manhattan to get this value
        self.h = h
        #Movment cost from one node to another node. Values given i exercise
        self.g = 0
        #F-value is G+H
        self.f = f
        #All the neighboring nodes to the current node
        self.parents = parents
        #x coordinate
        self.x = x
        #y coordinate
        self.y = y
        #Char represented in the map, '.', '#', A or B
        self.c = c
        #Is the node walkable
        if self.c == '#':
            self.walkable = False

        else:
            self.walkable = True
            if self.c == 'w':
                self.g = 100
            elif self.c == 'm':
                self.g = 50
            elif self.c == 'f':
                self.g = 10
            elif self.c == 'g':
                self.g = 5
            elif self.c == 'r':
                self.g = 1

    def __eq__(self, other):
        return self.f == other.f

    def __lt__(self, other):
        return self.f < other.f


    def __gt__(self, other):
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




