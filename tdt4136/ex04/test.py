# -*- encoding: utf-8 -*-

import logging
import time

from datastructures import *

e = EggCarton(5, 5, 2)

t = time.time()

e.create_random_board()

print e

while True:
    neighbors = e.create_neighbors(4)

    temp_max = e.objective()
    temp = e
    for n in neighbors:
        if n.objective() > temp_max:
            temp_max = n.objective()
            temp = e

    if temp is e:
        e.create_random_board()

    if e.objective() == 1:
        break

print e

print "Took %f seconds" % (time.time() - t)
