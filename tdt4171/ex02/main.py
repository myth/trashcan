# -*- coding: utf8 -*-
#
# Created by 'myth' on 3/1/16

from algorithm import ForwardBackward
import logging
import logging.config as logconf
import numpy as np
import settings


def task_b(observations):
    """
    Demonstrates filtering using Forward
    :param observations: A list of True/False statements indicating whether or not umbrella was observed that day
    :return: A generator yielding each forward message in the given series of observation events in 'obs'
    """

    # Create a new ForwardBackward class (since it retains the matrix values)
    fb = ForwardBackward()

    # Start with a 50% chance of rain
    rain = np.matrix('.5;.5')

    # For each observation, yield forward message
    for umbrella in observations:
        rain = fb.forward(umbrella, rain)
        yield fb.normalize(rain)  # Normalize the vector


def task_c(observations):
    """
    Demonstrates filtering using Forward
    :param observations: A list of True/False statements indicating whether or not umbrella was observed that day
    :return: A generator yielding each forward message in the given series of observation events in 'obs'
    """

    # Create a new ForwardBackward class (since it retains the matrix values)
    fb = ForwardBackward()
    return fb.forward_backward(observations, np.matrix('.5;.5'))


if __name__ == '__main__':

    # Set up some logging
    logconf.dictConfig(settings.LOG_CONFIG)
    log = logging.getLogger('main')
    log.info('Starting assignment 2')

    # Predefine the list of observations
    obs = [True, True, False, True, True]

    log.info('--- Executing task B ---')
    # Fire up ye 'ole workhorse (Task B with umbrella observed on Day1 and Day2
    log.info('Executing task B with obs=[True, True]')
    for step, t in enumerate(task_b(obs[:2])):
        log.info('Day %d:\n%s' % (step + 1, t))

    # Fire up ye 'ole workhorse (Task B with umbrella observed on Day1&2, not on Day3, but again on Day4&5.
    log.info('Executing task B with obs=[True, True, False, True, True]')
    for step, t in enumerate(task_b(obs)):
        log.info('Day %d:\n%s' % (step + 1, t))

    log.info('--- Executing task C ---')
    log.info('Executing task C with obs=[True, True]')
    for day, t in task_c(obs[:2]):
        log.info('Day %d:\n%s' % (day + 1, t))

    log.info('Executing task C with obs=[True, True, False, True, True]')
    for day, t in task_c(obs):
        log.info('Day %d:\n%s' % (day + 1, t))
