# -*- coding: utf8 -*-
#
# Created by 'myth' on 3/1/16

import logging
import numpy as np


class ForwardBackward(object):
    """
    Implementation of the Forward-Backward algorithm
    """

    def __init__(self):
        """
        Constructor
        """

        self._log = logging.getLogger(__name__)
        self._initialize()

        self._log.debug('ForwardBackward initialized')
        self._log.debug('Transition model:\n %s' % self._T)
        self._log.debug('Observation model:\n %s' % self._O)

    def _initialize(self):
        """
        Init helper
        """

        # Transition model
        self._T = np.matrix('.7 .3;.3 .7')
        # Observation model
        self._O = {
            True: np.matrix('.9, 0;0 .2'),
            False: np.matrix('.1 0;0 .8'),
        }

    @staticmethod
    def normalize(vector):
        """
        Normalizes a vector
        :param vector: A numpy vector/array
        :return: A normalized vector
        """

        return vector / sum(vector)

    def forward(self, umb, f):
        """
        Matrix operation for the forward part of the algorithm
        :param umb: True or False (if umbrella was observed or not)
        :param f: Previous state
        :return: Forward message
        """

        # dot the observation model with the transition model, and then the current belief state
        forward = self._O[umb] * self._T * f

        self._log.debug('Forward given umb:%s and f:%s resulting in %s' % (umb, f, forward))

        return forward

    def backward(self, umb, b):
        """
        Matrix operation for the backward part of the algorithm
        :param umb: True of False (if umbrella was observed or not)
        :param b: Current state
        :return: Backward message
        """

        # dot the transition model with the observation model, and then the current state
        backward = self._T * self._O[umb] * b

        self._log.debug('Backward given umb:%s and b:%s resulting in %s' % (umb, b, backward))

        return backward

    def forward_backward(self, ev, prior):
        """
        Smoothing using the Forward-Backward algorithm from Norvig
        :param ev: A list of observation events (umbrella=True or umbrella=False)
        :param prior: An initial probability matrix
        :return: A generator yielding each step in the forward and backward messages
        """

        # Cache the amount of observations available
        days = len(ev)

        fv = [prior]
        sv = []

        # For each observation, store and yield message
        for i in range(days):
            rain = self.forward(ev[i], fv[i])
            fv.append(rain)

            # For debug and documentation purposes, we yield each step
            yield i, self.normalize(rain)

        print(fv)
        self._initialize()

        # For the backwards iteration, we start with (1.0 1.0) probability, as opposed to (0.5 0.5) in the forward.
        b = np.matrix('1;1')

        # For the backwards part, we reverse the observations
        for i in range(days - 1, -1, -1):
            current = self.normalize(np.multiply(fv[i+1], b))
            sv.append(current)
            b = self.normalize(self.backward(ev[i], b))

            # For debug and documentation purposes, we yield each step
            yield i, self.normalize(current)
