# -*- encoding: utf-8 -*-

import logging
import time

from datastructures import *

e = EggCarton(7, 7, 3)

t = time.time()

e.create_random_board()

print e

neighbors = e.create_neighbors(4)

for n in neighbors:
    print n

print "Took %f seconds" % (time.time() - t)
