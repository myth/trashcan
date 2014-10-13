# -*- encoding: utf-8 -*-

import logging
import time

from datastructures import *

e = EggCarton(10, 10, 3)
e.create_random_board()

t = time.time()

print e

temp_max = 0
temp = e

while True:

    neighbors = temp.create_neighbors(4)
    current = temp

    for n in neighbors:
        if n.objective() > temp_max:
            temp = n
            temp_max = n.objective()
    
    if temp is not current:
        print "Found better neighbor... %f" % temp_max
        

    if temp.objective() == 1.0:
        print temp
        break

print "Took %f seconds" % (time.time() - t)
