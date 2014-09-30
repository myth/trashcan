# -*- coding: utf-8 -*-
"""
This file contains different graph algorithms
"""

import logging
import time


def a_star(graph, current, end):
    """
    the A* algorithm. Takes in a graph, current position and destination
    :param graph: The matrix of nodes
    :param end: The instance of the goal node
    :param current: The node representing the starting point
    """

    logging.debug('Starting A* with: %s' % repr(graph))
    start_time = time.time()

    openlist = []
    closedlist = []
    path = []

    def retracepath(c):
        """
        retracepath steps back through the visit-tree and creates the path from start to end
        :param c:
        :return:
        """
        path.insert(0, c)
        if c.parent is None:
            logging.debug('A* took %d seconds to run.' % time.time() - start_time)
            return
        retracepath(c.parent)

    openlist.append(current)
    while len(openlist) is not 0:
        current = min(openlist, key=lambda inst: inst.h)
        if current == end:
            logging.debug('A* took %d seconds to run.' % time.time() - start_time)
            return retracepath(current)
        openlist.remove(current)
        closedlist.append(current)
        for tile in graph[current]:
            if tile not in closedlist:
                tile.h = (abs(end.x - tile.x)+abs(end.y - tile.y))*10
                if tile not in openlist:
                    openlist.append(tile)
                tile.parent = current

    logging.debug('A* took %d seconds to run.' % time.time() - start_time)
    return path


def dfs(graph, start):
    """
    Depth-First-Search.

    :param graph: A graph/matrix of nodes
    :param start: The starting position
    :return: Reurns a set of nodes in the order they were visited
    """

    logging.debug('Starting A* with: %s' % repr(graph))
    start_time = time.time()

    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)

    logging.debug('A* took %d seconds to run.' % time.time() - start_time)
    return visited


def dfs(graph, start, visited=None):
    """
    Breadth-First-Search

    :param graph: A graph/matrix of nodes
    :param start: The starting position
    :param visited: Recursive pass-through variable that tracks visited nodes
    :return: Resutns a set of nodes in the order they were visited
    """

    logging.debug('Starting A* with: %s' % repr(graph))
    start_time = time.time()

    if visited is None:
        visited = set()
    visited.add(start)
    for next_node in graph[start] - visited:
        dfs(graph, next_node, visited)

    logging.debug('A* took %d seconds to run.' % time.time() - start_time)
    return visited
