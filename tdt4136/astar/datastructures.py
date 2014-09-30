# -*- coding: utf-8 -*-

def make_matrix(board):
    """
    This function returns a matrix of characters based on an input string
    """

    return [list(line) for line in board.split('\n')]

