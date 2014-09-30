# -*- coding: utf-8 -*-

class Board:
    def __init__(self, board):
        self.matrix = self.make_matrix(board)


    def make_matrix(self, board):
        """
        This function returns a matrix of characters based on an input string
        """
        return [list(line) for line in board.split('\n')]



    def get_start(self):
        """
        Returns coordinates for the starting node
        """
        return self.get_point('A')



    def get_goal(self):
        """
        Returns coordinates for det goal node
        """

        return self.get_goal('B')



    def get_point(self, node):
        """
        This function returns det x and y coordinates for a given node
        """
        for x in self.matrix:
            for y in self.matrix[x]:
                if y == node:
                    return (x,y)
                