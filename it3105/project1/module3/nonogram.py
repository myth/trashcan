# -*- coding: utf8 -*-
#
# Created by 'myth' on 10/3/15

from copy import deepcopy

from algorithms import AStarProblem, GAC
from common import *
from datastructures import AStarState, CSPState


class NonogramProblem(AStarProblem):

    def __init__(self, path):
        """
        Constructor for the NonogramProblem
        Will set up the grid and create all nodes with all possible permutations as domains
        """

        self.nodes = {}
        with open(path) as f:
            cols, rows = map(int, f.readline().split())

            self.grid = [[False]*cols]*rows
            self.total_rows = rows
            self.total_cols = cols

            r_reversed = []
            for row in range(rows):
                r_reversed.append(list(map(int, f.readline().split())))
            for row, counts in enumerate(reversed(r_reversed)):
                self.nodes[row] = [(row, p) for p in self.gen_patterns(counts, cols)]
            for col in range(cols):
                counts = list(map(int, f.readline().split()))
                self.nodes[rows + col] = [(col, p) for p in self.gen_patterns(counts, rows)]

        if DEBUG:
            for x in range(rows + cols):
                print(self.nodes[x])

        self.constraints = {}
        self.generate_constraints()

        def cf(a, b):
            r, domain_a = a
            c, domain_b = b
            return domain_a[c] == domain_b[r]

        self.gac = GAC(cnet=self.constraints, csp_state=CSPState(self.nodes), cf=cf)
        self.gac.initialize()
        self.gac.domain_filtering_loop()
        self.initial_state = AStarState()
        self.initial_state.state = self.gac.csp_state

        log('NonogramProblem initialized with %dx%d grid' % (rows, cols))

    @staticmethod
    def gen_patterns(counts, cols):
        """
        Generates pattern permutations for a given number of segments
        :param counts: A sequence of segment sizes
        :param cols: The number of columns in the matrix
        :return: A pattern matrix
        """

        if len(counts) == 0:
            row = []
            for x in range(cols):
                row.append(False)
            return [row]

        permutations = []

        for start in range(cols - counts[0] + 1):
            permutation = []
            for x in range(start):
                permutation.append(False)
            for x in range(start, start + counts[0]):
                permutation.append(True)
            x = start + counts[0]
            if x < cols:
                permutation.append(False)
                x += 1
            if x == cols and len(counts) == 0:
                permutations.append(permutation)
                break
            sub_start = x
            sub_rows = NonogramProblem.gen_patterns(counts[1:len(counts)], cols - sub_start)
            for sub_row in sub_rows:
                sub_permutation = deepcopy(permutation)
                for x in range(sub_start, cols):
                    sub_permutation.append(sub_row[x - sub_start])
                permutations.append(sub_permutation)
        return permutations

    def generate_constraints(self):
        """
        Generates constraint network for the problem
        In this problem it is implemented as a dictionary with a given row/col index as a key
        The respective value is a list with the index for all possible rows/columns the row/col has constraints against
        More specific this means a list of all intersecting cells between a row and a column.
        """

        for row in range(self.total_rows):
            self.constraints[row] = [i for i in range(self.total_rows, self.total_rows + self.total_cols)]
        for col in range(self.total_cols):
            self.constraints[self.total_rows + col] = [i for i in range(0, self.total_rows)]

    def get_start_node(self):
        """
        Returns the start node for this problem instance
        :return: the initial state in this specific problem
        """
        return self.initial_state

    def heuristic(self, astar_state):
        """
        Calculates the heuristic for a given state
        In this problem the heuristic is calculated from the sum of all domains in the variables list
        :param astar_state: The state to calculate h for
        :return: The h value
        """
        h = sum((len(domains) - 1) for domains in astar_state.state.nodes.values())
        if h == 0:
            astar_state.is_goal = True
        astar_state.h = h
        return h

    def arc_cost(self, node):
        """
        Returns the arc cost for a given node
        :param node: The node to get arc cost for
        :return: The arc cost, 1 in this implementation
        """
        return 1

    def get_goal_node(self):
        """
        Returns the goal node for the problem instance
        Not implemented for this problem
        :return: None in this instance
        """
        return None

    def get_all_successor_nodes(self, astar_state):
        """
        Fetches all successor nodes from a given CSP state
        In this spesific problem that means all states with a domain
        length greater than 1 for a random node
        :return: The generated successor nodes
        """
        csp_state = astar_state.state
        successor_nodes = []

        #  TODO: Is this verified?
        for node, domains in csp_state.nodes.items():
            if len(domains) > 1:
                for d in range(len(domains)):
                    print(node, domains[d])
                    child_state = deepcopy(csp_state)

                    child_state.nodes[node] = [list(domains)[d]]

                    if DEBUG:
                        print("Domain for %s is now %s" % (node, str(child_state.nodes[node])))

                    self.gac.csp_state = child_state
                    self.gac.run_again(node)

                    if not child_state.contradiction:
                        astar_state = AStarState()
                        astar_state.state = child_state
                        successor_nodes.append(astar_state)

                return successor_nodes

    def get_node(self, x, y):
        """
        Returnes a given node in the grid representation
        It used the x and y coordinates to achieve this
        :param x: x-coordinate
        :param y: y-coordinate
        :return:
        """
        a = AStarState(index=0, x=x, y=y)
        a.state = self.grid[y][x]
        return a
