# -*- encoding: utf-8 -*-

import logging
import time
from tools import *

from datastructures import *
i = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
j = ['3']
constrains = [('1', '3'), ('2', '3'), ('4', '3'), ('5', '3'), ('6', '3'), ('7', '3'), ('8', '3'), ('9', '3')]
e = create_sudoku_csp("sudokus/easy.txt")
print e.revise(e, i, j)




#
#{'2-2': ['1', '2', '3', '4', '5', '6', '7', '8', '9'], '4-7': ['1', '2', '3', '4', '5', '6', '7', '8', '9'] Domains
#[('1', '3'), ('2', '3'), ('4', '3'), ('5', '3'), ('6', '3'), ('7', '3'), ('8', '3'), ('9', '3')] Constrains (4-7, 4-0)

# e.create_random_board()
#
# t = time.time()
#
# print e
#
# temp_max = 0
# temp = e
#
# while True:
#
#     neighbors = temp.create_neighbors(6)
#     current = temp
#
#     for n in neighbors:
#         if n.objective() > temp_max:
#             temp = n
#             temp_max = n.objective()
#
#     if temp is not current:
#         print "Found better neighbor... %f" % temp_max
#         print temp
#
#
#     if temp.objective() == 1.0:
#         print temp
#         break
#
# print "Took %f seconds" % (time.time() - t)
