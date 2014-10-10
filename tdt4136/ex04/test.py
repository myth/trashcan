# -*- encoding: utf-8 -*-

import logging

from datastructures import *

e = EggCarton(5, 5, 2)

print e
print ""

e.matrix[2][3] = 1
e.matrix[3][4] = 1

print e

e.matrix = [
    [1,0,1,0,0],
    [0,1,0,0,1],
    [0,1,0,1,0],
    [1,0,0,0,1],
    [0,0,1,1,0],
]

print e

e.create_random_board()

print e
