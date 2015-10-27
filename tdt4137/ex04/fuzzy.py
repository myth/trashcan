# -*- coding: utf-8 -*-

# TASK A

"""
Distance: 3.6
Delta: 1.1

                    VS  SM   P    B  VB
Distance fuzzy set: (0, 0.6, 0.1, 0, 0)

                    SF  S   ST    G  GF
Delta    fuzzy set: (0, 0, 0.2, 0.4, 0)

BrakeHard = VS = 0.0
SlowDown = min(0.6, 0.2) = 0.2
None = min(0.6, 0.4) = 0.4
SpeedUp = min(0.1, 0.4) = 0.1
FloorIt = min(0, max(1 - 0.4, 1 - 0.0)) = 0.0


Actions = [0, 0.2, 0.4, 0.1, 0]

(-7 + -6 + -5 + -4 + -3) * 0.2 + (-2 + -1 + 0 + 1 + 2 + 3) * 0.4 + (4 + 5 + 6 + 7) * 0.1
-----------------------------------------------------------------------------------
                       0.1 * 4 + 0.2 * 5 + 0.4 * 6

Centroid = -0.42

ACTION = None

"""

# VALUES ARE INTERPRETED FROM THE GRAPH IN THE FOLLOWING MANNER:

# The number on the x-axis accounts for the center of two marks.
# For example, the mark on the left of 0 in DELTA is -0.25.
# The mark on the right of 0 in DELTA is 0.25.
# Likewise, the start of the Big triangle in DISTANCE is 5.5

# TASK B

# Usage: python fuzzy.py <dist> <delta>

"""

Running fuzzy.py 3.6 1.1 gives the following answer:

0.462809917355 = Action: None

Inputing different intervals gives different actions.

fuzzy.py 5.0 2.0 = 3.93103448276 = Action: SpeedUp (Which corresponds to the Perfect distance and growing
delta rule).

fuzzy.py 3.0 -2.5 = 0.0 = Action: None
This makes no sense, as a small distance and shriking delta should indicate
that we need to slow down. But that rule is missing.
"""


from functools import partial
from pprint import pprint
from sys import argv, exit




def AND(x, y):
    return min(x, y)


def OR(x, y):
    return max(x, y)


def NOT(x):
    return 1.0 - x


def grade(x, y, z, c=None):
    value = 0.0
    if z >= y:
        value = 1.0
    else:
        value = (z - x) / (y - x)
    if c is not None and value > c:
        return c
    return value


def reverse_grade(x, y, z, c=None):
    value = 1.0 - grade(x, y, z, c=c)
    if c is not None and value > c:
        return c
    return value


def triangle(x, y, z, c=None):
    value = 0.0
    center = (y - x) / 2
    if z >= x and z <= center:
        value = (z - x) / (center - x)
    elif z >= center and z <= y:
        value = (y - z) / (y - center)
    if c is not None and value > c:
        return c
    return value


def aggregate_results(rule_results, membership_functions, values):
    collector = []
    pprint(rule_results)
    pprint(membership_functions)
    pprint(values)
    for v in values:
        value = 0.0
        for mf, r in zip(membership_functions, rule_results):
            current = mf(v, r)
            if current > value:
                value = current
        collector.append(value)
    print('Aggregate results:\n')
    pprint(collector)
    return collector


def centroid(data, values):
    try:
        return sum(x*y for x, y in zip(data, values)) / sum(data)
    except ZeroDivisionError:
        return sum(x*y for x, y in zip(data, values)) / 1


def task_b():
    """
    Mamdani reasoner.
    """

    print('-'*20)
    print('Mamdani reasoner')
    print('-'*20)
    print('')

    print('Calculating action...')

    if len(argv) != 3:
        print('Usage: python %s <distance> <delta>' % argv[0])
        exit(0)

    distance = float(argv[1])
    delta = float(argv[2])

    RULES = [
        partial(reverse_grade, 1.5, 4.5)(distance),
        AND(
            partial(triangle, 1.5, 4.5)(distance),
            partial(triangle, -1.5, 1.5)(delta)
        ),
        AND(
            partial(triangle, 1.5, 4.5)(distance),
            partial(triangle, 0.5, 3.5)(delta)
        ),
        AND(
            partial(triangle, 3.5, 6.5)(distance),
            partial(triangle, 0.5, 3.5)(delta)
        ),
        AND(
            partial(grade, 7.5, 9.0)(distance),
            OR(
                NOT(partial(triangle, 0.5, 3.5)(delta)),
                NOT(partial(grade, 2.5, 3.75)(delta))
            )
        )
    ]

    agg = aggregate_results(
        RULES,
        [
            partial(reverse_grade, -8.0, -5.0),
            partial(triangle, -7.0, -1.0),
            partial(triangle, -3.0, 3.0),
            partial(triangle, 1.0, 7.0),
            partial(grade, 5.0, 8.0)
        ],
        range(-10, 10 + 1, 1),
    )

    result = centroid(agg, range(-10, 10 + 1, 1))

    print(result)


if __name__ == '__main__':
    task_b()

