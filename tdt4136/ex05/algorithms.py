# -*- encoding: utf-8 -*-

from datastructures import *
# -*- coding: utf-8 -*-
"""
This module contains the classes data representation
"""

import logging
import copy
import itertools

def backtracking_search(board):
    """This functions starts the CSP solver and returns the found
    solution.
    """
    # Make a so-called "deep copy" of the dictionary containing the
    # domains of the CSP variables. The deep copy is required to
    # ensure that any changes made to 'assignment' does not have any
    # side effects elsewhere.
    assignment = copy.deepcopy(board.domains)

    # Run AC-3 on all constraints in the CSP, to weed out all of the
    # values that are not arc-consistent to begin with
    board.inference(assignment, board.get_all_arcs())

    # Call backtrack with the partial assignment 'assignment'
    return backtrack(board, assignment)

def backtrack(board, assignment):
    """The function 'Backtrack' from the pseudocode in the
    textbook.

    The function is called recursively, with a partial assignment of
    values 'assignment'. 'assignment' is a dictionary that contains
    a list of all legal values for the variables that have *not* yet
    been decided, and a list of only a single value for the
    variables that *have* been decided.

    When all of the variables in 'assignment' have lists of length
    one, i.e. when all variables have been assigned a value, the
    function should return 'assignment'. Otherwise, the search
    should continue. When the function 'inference' is called to run
    the AC-3 algorithm, the lists of legal values in 'assignment'
    should get reduced as AC-3 discovers illegal values.

    IMPORTANT: For every iteration of the for-loop in the
    pseudocode, you need to make a deep copy of 'assignment' into a
    new variable before changing it. Every iteration of the for-loop
    should have a clean slate and not see any traces of the old
    assignments and inferences that took place in previous
    iterations of the loop.
    """
    # TODO: IMPLEMENT THIS
    pass
