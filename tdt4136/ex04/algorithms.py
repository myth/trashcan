# -*- encoding: utf-8 -*-

import time
from datastructures import *
from math import exp
from random import random, randint


def sa(board):

    temp = 30
    f_target = 1.0
    start = board
    current_f = start.objective()
    pmax = start

    while temp > 0:
        #print "this is temp: ", temp
        t = time.time()
        if current_f >= f_target:
            return current_f

        else:
            nabo = start.create_neighbors(4)

            for y in nabo:
                if y.objective() > pmax.objective():
                    pmax = y

            q = ((pmax.objective() - current_f)/current_f)
            print "Dette er q: ", q

            p = min([1, exp((q*-1)/temp)])
            print "Dette er p: ", p

            x = random()
            print "Dette er x: ", x

            if x > p:
                current_f = pmax.objective()
                print "pmax"

            else:
                current_f = nabo[randint(0, 3)]
                current_f = current_f.objective()
                print "Random nabo"

            temp -= time.time() - t
            print "this is current_f", current_f

egg = EggCarton(8, 8, 1)
egg.create_random_board()
sa(egg)