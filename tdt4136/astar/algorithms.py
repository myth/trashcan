# -*- coding: utf-8 -*-
"""
This file contains different graph algorithms
"""

import logging
import time
from heapq import *


def a_star(graph, current, end):
    """
    the A* algorithm. Takes in a graph, current position and destination
    :param graph: The matrix of nodes
    :param end: The instance of the goal node
    :param current: The node representing the starting point
    """

    logging.debug('Starting A*')
    start_time = time.time()

    openlist = []
    heapify(openlist)
    closedlist = set()
    path = []

    def retracepath(c):
        """
        retracepath steps back through the visit-tree and creates the path from start to end
        :param c:
        :return:
        """
        if c.parent is not None:
            logging.debug('Retrace on %d, %d with parent %s' % (c.x, c.y, str(c.parent)))
        path.insert(0, c)
        if c.parent is None:
            logging.debug('A* took %f seconds to run.' % (time.time() - start_time))
            return
        retracepath(c.parent)

    heappush(openlist, current)
    while openlist:
        current = heappop(openlist)

        if current is end:
            logging.debug('Reached destination')
            logging.debug('A* took %f seconds to run.' % (time.time() - start_time))
            return retracepath(current)

        closedlist.add(current)
        for tile in graph[current]:
            if tile not in closedlist:
                tile.h = (abs(end.x - tile.x)+abs(end.y - tile.y))*10
                if tile not in openlist:
                    openlist.append(tile)
                logging.debug('Adding %s as parent of %s' % (current, tile))
                tile.parent = current

    logging.debug('A* took %f seconds to run.' % (time.time() - start_time))
    return path


def dfs(graph, start):
    """
    Depth-First-Search.

    :param graph: A graph/matrix of nodes
    :param start: The starting position
    :return: Reurns a set of nodes in the order they were visited
    """

    logging.debug('Starting DFS')
    start_time = time.time()

    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)

    logging.debug('A* took %f seconds to run.' % (time.time() - start_time))
    return visited


def bfs(graph, start, visited=None):
    """
    Breadth-First-Search

    :param graph: A graph/matrix of nodes
    :param start: The starting position
    :param visited: Recursive pass-through variable that tracks visited nodes
    :return: Resutns a set of nodes in the order they were visited
    """

    logging.debug('Starting BFS')
    start_time = time.time()

    if visited is None:
        visited = set()
    visited.add(start)
    for next_node in graph[start] - visited:
        dfs(graph, next_node, visited)

    logging.debug('A* took %f seconds to run.' % (time.time() - start_time))
    return visited
