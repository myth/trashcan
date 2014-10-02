# -*- coding: utf-8 -*-
"""
Preliminary test file for RushHour
"""

from datastructures import *
from algorithms import *
from itertools import permutations


EASY = [
    (0,2,2,2),
    (0,0,4,3),
    (0,3,4,2),
    (0,4,1,2),
    (1,2,0,2),
    (1,4,2,2)
]

cars = [CarNode(*x) for x in EASY]

board = RushHourBoard(cars=cars)

print 'Cars on board:'
print board.cars
print ''

blocking_test = permutations(board.cars, 2)

for pair in blocking_test:
    if pair[0].blocks(pair[1]):
        print '%s blocks %s' %(pair[0], pair[1])
    else:
        print '%s does not block %s' % (pair[0], pair[1])
