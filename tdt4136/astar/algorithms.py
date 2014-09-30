# -*- coding: utf-8 -*-

import logging
import datetime
import time

def aStar(graph, current, end):
    """
    the A* algorithm. Takes in a graph, current position and destination
    """

    logging.debug('Starting A* with: %s' % repr(graph))
    start_time = time.time()

    openList = []
    closedList = []
    path = []

    def retracepath(c):
        path.insert(0,c)
        if c.parent is None:
            logging.debug('A* took %d seconds to run.' % time.time() - start_time)
            return
        retracepath(c.parent)

    openList.append(current)
    while len(openList) is not 0:
        current = min(openList, key=lambda inst: inst.h)
        if current == end:
            logging.debug('A* took %d seconds to run.' % time.time() - start_time)
            return retracepath(current)
        openList.remove(current)
        closedList.append(current)
        for tile in graph[current]:
            if tile not in closedList:
                tile.h = (abs(end.x-tile.x)+abs(end.y-tile.y))*10
                if tile not in openList:
                    openList.append(tile)
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
    for next in graph[start] - visited:
        dfs(graph, next, visited)

    logging.debug('A* took %d seconds to run.' % time.time() - start_time)
    return visited
