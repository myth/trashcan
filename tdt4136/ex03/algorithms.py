# -*- coding: utf-8 -*-
"""
This file contains different graph algorithms
"""

import logging
import time
from heapq import *


def retracepath(c):
    """
    Path retrace function

    :param c: An instance of Node
    :param path: The backtrack list
    :return: The complete path
    """

    path = [c]

    while c.parent is not None:
        c = c.parent
        path.insert(0, c)

    return path

def a_star(neighbors, current, end):
    """
    The A* algorithm. Takes in a graph, current position and destination

    Our implementation was written by ourselves for the most part, with
    inspiration gathered from Wikipedias Excellent A* article

    :param graph: The matrix of nodes
    :param end: The instance of the goal node
    :param current: The node representing the starting point
    """

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
            logging.debug('A* took %f seconds to run.' % (time.time() - start_time))
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


def bfs(neighbors, start, end):
    """
    Breadth-First-Search

    :param graph: A graph/matrix of nodes
    :param start: The starting position
    :return: Resutns a set of nodes in the order they were visited
    """

    logging.debug('Starting BFS')
    start_time = time.time()

    # Create the openset (queue) and closedset (visited)
    visited = set()
    visited.add(start)
    queue = [start]

    # As long as there are items in queue
    while queue:
        
        # Get the first one
        current = queue.pop(0)

        # Hooray, we found the end node
        if current is end:
            logging.debug('Reached destination.')
            logging.debug('BFS took %f seconds to run.' % (time.time() - start_time))
            return retracepath(current), queue, visited

        # For all adjacent nodes to current
        for node in neighbors[current]:

            # If they have not been visited yet, update the parent
            # add to visited, and throw the node into the queue
            if node not in visited:
                node.parent = current
                visited.add(node)
                queue.append(node)

    
    logging.debug('BFS took %f seconds to run.' % (time.time() - start_time))

    # Return paths for debug purposes if algorithm fails
    return retracepath(current), queue, visited

def dijkstra(graph, start, end):
    """
    Dijkstras algorithm. We are re-using the base Node class for the priority queue.
    All H-values are set to zero, so the G values will be representing the total cost.
    Nodes are compared by F-value, which in this case will be the same as G.

    :param graph: A graph dict of nodes and their neighbors
    :param start: The starting position
    :return: Resutns a set of nodes in the order they were visited  
    """

    logging.debug('Starting Dijkstra')
    start_time = time.time()

    visited = set()
    queue = []
    heapify(queue)

    for node, neighbors in graph.items():
        node.h = 0
        if node is start:
            node.g = 0
            node.update_f()
        else:
            node.g = 1000000
            node.update_f()
        heappush(queue, node)

    while queue:
        current = heappop(queue)
        visited.add(current)

        logging.debug('Current node %s with Q %s' % (current, repr(queue)))

        if current is end:
            logging.debug('Reached destination.')
            logging.debug('Dijkstra took %f seconds to run.' % (time.time() - start_time))
            return retracepath(current), queue, visited

        for node in graph[current]:
            if node not in visited:
                temp_cost = current.g + node.arc_cost
                if temp_cost < node.g:
                    node.set_g(temp_cost)
                    node.update_f()
                    node.parent = current

        queue.sort()

    logging.debug('Dijkstra took %f seconds to run.' % (time.time() - start_time))

    # Return paths for debug purposes if algorithm fails
    return retracepath(current), queue, visited
