# -*- coding: utf8 -*-
#
# Created by 'myth' on 10/2/15

from abc import abstractmethod
from itertools import product
from common import *
import abc
import heapq


# --- A* ---

ASTAR_OPTIONS = [
    'best',
    'dfs',
    'bfs'
]
ASTAR_HEURISTIC = [
    'manhattan',
    'euclidean'
]


class AStarProblem(metaclass=abc.ABCMeta):
    """
    Abstract class forcing implementation of the details A* need for perform the general algorithm
    """

    @abstractmethod
    def get_start_node(self):
        pass

    @abstractmethod
    def get_goal_node(self):
        pass

    @abstractmethod
    def get_all_successor_nodes(self, node):
        pass

    @abstractmethod
    def arc_cost(self, node):
        pass

    @abstractmethod
    def heuristic(self, node):
        pass


class AStar(object):
    """
    A general A* algorithm class. Takes the mode and a problem instance as parameters
    :param mode: The mode to run the A* algorithm in
    :param problem: The problem to run A* on
    """

    def __init__(self, mode='best', problem=None):
        """
        Initializing the A* object with the given parameters
        """
        if not isinstance(problem, AStarProblem):
            raise Exception("Problem must be an instance of AStarProblem")
        else:
            log('A* initiated with valid problem instance of type: %s' % type(problem).__name__)

        self.mode = mode
        self.problem = problem

        self.open_set = []
        self.closed_set = set()

        self.start_node = self.problem.get_start_node()
        self.goal_node = None

        self.path = []
        self.parent_of = {}

        if self.mode == 'best':
            heapq.heapify(self.open_set)

        log("A* initiated successfully")

    def agenda_loop(self):
        """
        The implementation of the A* algorithm. This is the main loop for the algorithm
        """
        self.add_node(self.start_node)

        while len(self.open_set):
            node = self.take_node()
            self.closed_set.add(node)

            if node.is_goal:
                log('Reached the goal node for this problem instance')
                yield {
                    'open_set': self.open_set,
                    'closed_set': self.closed_set,
                    'path': self.get_path_from_node([node])
                }
                break

            successors = self.problem.get_all_successor_nodes(node) or []

            for successor in successors:
                node.children.add(successor)
                if successor not in self.closed_set and successor not in self.open_set:
                    self.attach_and_eval(successor, node)
                    self.add_node(successor)
                elif node.g + self.problem.arc_cost(node) < successor.g:
                    self.attach_and_eval(successor, node)  # Returns f value, but is never used
                    if successor in self.closed_set:
                        debug('Reached closed node, propagating path')
                        self.propagate_path(node)

            # Yields the current open- and closed set to the function that called the agenda_loop
            yield {
                'open_set': self.open_set,
                'closed_set': self.closed_set,
                'path': self.get_path_from_node([node])
            }

    def attach_and_eval(self, successor, node):
        self.parent_of[successor] = node
        successor.g = node.g + self.problem.arc_cost(node)
        successor.h = self.problem.heuristic(successor)
        successor.f = successor.g + successor.h

    def propagate_path(self, node):
        for child in node.children:
            if node.g + self.problem.arc_cost(node) < child.g:
                self.parent_of[child] = node
                child.g = node.g + self.problem.arc_cost(node)
                child.h = self.problem.heuristic(child)
                child.f = child.g + child.h
                self.propagate_path(child)

    def add_node(self, node):
        """
        Method to add the node to the open set depending on the mode
        :param node: The node to append to the list
        """
        return {
            'best': lambda: heapq.heappush(self.open_set, node),  # Insert to ascending heap queue
            'bfs': lambda: self.open_set.append(node),  # Insert to back of queue (FIFO)
            'dfs': lambda: self.open_set.insert(0, node)  # Insert to front of queue (LIFO)
        }.get(self.mode)()

    def take_node(self):
        """
        Method to take the right node from the open set depending on the mode
        """
        return {
            'best': lambda: heapq.heappop(self.open_set),  # Get first element in queue
            'bfs': lambda: self.open_set.pop(0),
            'dfs': lambda: self.open_set.pop(0)
        }.get(self.mode)()

    def get_path_from_node(self, path):
        """
        This method returns a list containing a shallow copy of all node objects in the current path
        To be used with for instance the GUI visualisation
        :param path:
        :return:
        """
        while path[-1] != self.problem.get_start_node():
            path.append(self.parent_of[path[-1]])
        return path[::]

# --- Generalized Arc Constraint ---

GAC_DEFAULT_CONSTRAINT = 'x != y'
GAC_DEFAULT_K = 4


class GAC(object):

    def __init__(self, cnet=None, csp_state=None, cf=lambda x, y: x != y):
        """
        Constructor for the GAC algorithm
        :param cnet:
        :param csp_state:
        :return:
        """
        self.csp_state = csp_state
        self.cnet = cnet
        self.cf = cf
        self.queue = []

    def initialize(self):
        """
        Initializes the queue with all constraint permutations
        :return:
        """
        for node, edges in self.cnet.items():
            self.queue.extend((node, edge) for edge in edges)

        log('Queue initialized with %d pairs' % len(self.queue))

    def revise(self, from_node):
        """
        Removes all inconsistent values in a domain for all possible arc from an node
        It also saves to the csp_state if the current state is a contradiction
        :param from_node: The node to run revise from
        :return: Boolean telling whether the domain was revised or not
        """
        to_be_removed = []
        for arc in self.cnet[from_node]:
            for domain in self.csp_state.nodes[from_node]:
                remove = True
                for x, y in product([domain], self.csp_state.nodes[arc]):
                    if self.cf(x, y):
                        remove = False
                        break

                if remove:
                    if DEBUG:
                        print('Removing domain %s from %s' % (str(domain), from_node))
                    to_be_removed.append(domain)

        for domain in to_be_removed:
            if domain in self.csp_state.nodes[from_node]:
                self.csp_state.nodes[from_node].remove(domain)

        if to_be_removed:
            if not self.csp_state.nodes[from_node]:
                self.csp_state.contradiction = True
                if DEBUG:
                    print('Contradiction')
            return True

        return False

    def domain_filtering_loop(self):
        """
        Pops of all todo revise pairs from the queue and runs revise on the from_node
        If the domains is revised it will add all other possible constraints from the from_node to the revise queue to
        check for further domain reductions possible
        """
        while self.queue:
            from_node, to_node = self.queue.pop(0)
            if self.revise(from_node):
                for arc in self.cnet[from_node]:
                    if arc != from_node:
                        self.queue.append((arc, from_node))

    def run_again(self, node):
        """
        A soft-reboot of the domain filtering loop from a given node
        :param node: The node to append to the revise queue
        """
        for arc in self.cnet[node]:
            if node != arc:
                self.queue.append((arc, node))
        self.domain_filtering_loop()
