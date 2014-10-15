# -*- encoding: utf-8 -*-

import time
from datastructures import *
from math import exp
from random import random, randint


def sa(board):

    temp = 4096
    f_target = 1.0
    start = board
    current_f = start.objective()
    pmax = start
    best = pmax

    while temp > 0:
        #print "this is temp: ", temp
        t = time.time()
        if current_f >= f_target:
            return pmax

        else:
            nabo = pmax.create_neighbors(6)

            for y in nabo:
                if y.objective() > pmax.objective():
                    pmax = y

            try:

                q = ((pmax.objective() - current_f)/current_f)

            except ZeroDivisionError:
                q = pmax.objective()

            p = min([1, exp((q*-1)/temp)])

            x = random()

            if x > p:
                current_f = pmax.objective()
                if current_f > best.objective():
                    best = pmax

            else:
                current_f = nabo[randint(0, 5)]
                if current_f > best.objective():
                    best = current_f
                    current_f = current_f.objective()


        temp = temp - 1


    return best
