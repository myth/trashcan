# -*- coding: utf-8 -*-

class Board:
    def __init__(self, board):
        self.matrix = self.make_matrix(board)


    def make_matrix(self, board):
        """
        This function returns a matrix of characters based on an input string
        """
        return [list(line) for line in board.split('\n')]



    def get_startpoint(self):
        """
        This function returns det x and y coordinates for the starting position A.
        """
        for x in self.matrix:
            for y in self.matrix[x]:
                if y == 'A':
                    return (x,y)