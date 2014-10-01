# -*- coding: utf-8 -*-
"""
This file contains different graph algorithms
"""

import logging
import time
from heapq import *


def a_star(neighbors, current, end):
    """
    The A* algorithm. Takes in a graph, current position and destination

    Our implementation was written by ourselves for the most part, with
    inspiration gathered from Wikipedias Excellent A* article

    :param graph: The matrix of nodes
    :param end: The instance of the goal node
    :param current: The node representing the starting point
    """

    def retracepath(c, path=[]):
        """
        Path retrace function

        :param c: An instance of Node
        :param path: The backtrack list
        :return: The complete path
        """

        path.insert(0, c)

        if c.parent is None:
            return path
        else:
            return retracepath(c.parent, path)

    logging.debug('Starting A*')
    start_time = time.time()

    openset = []
    heapify(openset)
    closedset = set()

    # Add the starting node to the heap
    heappush(openset, current)

    # As long as there are nodes left in the min-heap queue
    while openset:

        # Get the first element from the queue (The one with the lowest G-value)
        current = heappop(openset)

        # If we have reached the end node, perform the traceback,
        # reverse the list and break out
        if current is end:
            logging.debug('Reached destination %s.' % current)
            return retracepath(current), openset, closedset

        # Since we've now visited the current node, we add it to the closed set
        closedset.add(current)

        # For each adjacent neighbor to the current node
        for neighbor in neighbors[current]:

            # If node has already been checked out, continue
            if neighbor in closedset:
                continue

            # What will the cost be with turrent path
            temp_cost = current.g + neighbor.arc_cost

            # Set G value, update F value, set parent and
            # add to openset if not already in openset
            if neighbor not in openset:
                neighbor.set_g(temp_cost)
                neighbor.update_f()
                neighbor.parent = current
                heappush(openset, neighbor)

            # If the node is in the openset, but this path is better, then
            # update parent, G value and recalculate F value
            elif temp_cost < neighbor.g:
                neighbor.parent = current
                neighbor.set_g(temp_cost)
                neighbor.update_f()
        
        # Order the heap based on the changed values (Uncertain if we have to do this)
        openset.sort()

    logging.debug('A* took %f seconds to run.' % (time.time() - start_time))

    # Algo failed, returning path and sets for drawing mainly for debug purposes
    return retracepath(current), openset, closedset


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
