# -*- encoding: utf-8 -*-

import time
from datastructures import *
from math import exp
from random import random, randint


def sa(board):

    temp = 30*1000
    f_target = 1

    current_f = board.objective()

    while temp > 0:
        t = time.time()
        if current_f >= f_target:
            return current_f

        else:
            nabo = []
            for x in xrange(0, 4):
                b = EggCarton(5, 5, 2)
                nabo.append(b)

            pmax= 0
            for x in nabo:
                if x.objective() > pmax:
                    pmax = x

            q = (pmax.objective()-current_f)/current_f

            p = min(1.0, exp((q*-1)/temp))
            x = random()

            if x > p:
                current_f = pmax

            else:
                current_f = nabo[randint(0, 4)]


            temp = time.time() - t