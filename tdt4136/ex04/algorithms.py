# -*- encoding: utf-8 -*-

import time
from datastructures import *
from math import exp
from random import random, randint


def sa(board):

    temp = 30*1000
    f_target = 1.0
    start = board
    current_f = start.objective()
    pmax = start

    while temp > 0:
        print "this is temp: ", temp
        t = time.time()
        if current_f >= f_target:
            return current_f

        else:
            nabo = start.create_neighbors(4)

            for x in nabo:
                if x.objective() > pmax.objective():
                    pmax = x

            q = (pmax.objective()-current_f)/current_f

            p = min(1.0, exp((q*-1)/temp))
            x = random()

            if x > p:
                current_f = pmax.objective()

            else:
                current_f = nabo[randint(0, 3)]
                current_f = current_f.objective()

            temp -= time.time() - t

egg = EggCarton(5, 5, 2)
egg.create_random_board()

sa(egg)