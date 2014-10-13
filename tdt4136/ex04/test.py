# -*- encoding: utf-8 -*-

import logging
import time

from datastructures import *

e = EggCarton(5, 5, 2)
e.create_random_board()

t = time.time()

print e

temp_max = 0
temp = e

while True:
    
    current = temp

    neighbors = temp.create_neighbors(4)

    for n in neighbors:
        if n.objective() >= temp_max:
            temp = n
            temp_max = n.objective()

    if temp is current:
        e.create_random_board()
        print "Created random board"
    else:
        print "Used neighbor"

    if temp.objective() == 1.0:
        print temp
        break

print "Took %f seconds" % (time.time() - t)
