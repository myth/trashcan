# -*- coding: utf-8 -*-

from common import *


class Node(object):
    """
    Basic Node object that keeps the foundational properties of a Node
    that might be used in some sort of state or graph representation
    """

    def __init__(self, index=None, x=None, y=None):
        """
        Constructor
        """

        self.index = index
        self.x = x
        self.y = y
        self.parent = None
        self.children = set()

    def __str__(self):
        return 'N' + str(self.index)

    def __repr__(self):
        """
        String representation of the BasicNode object
        """

        return 'Node %d (%d, %d)' % (self.index, self.x, self.y)


class Graph(object):
    """
    Jazzing the graph since 1985
    """

    @staticmethod
    def read_all_graphs():
        return [Graph.read_graph_from_file(fp) for fp in fetch_files_from_dir()]

    @staticmethod
    def read_graph_from_file(file_path, networkx_graph=None, lightweight=False):
        """
        Reads input data from a file and generates a linked set of nodes
        :param file_path: Path to the file that is to be read into memory
        :return: A set of nodes
        """

        node_cache = {}
        edge_set = []

        # Read contents from specified file path
        with open(file_path) as g:
            # Retrieve the node and edge count from first line of file
            nodes, edges = map(int, g.readline().split())
            if networkx_graph:
                debug('NetworkX Graph instance provided, adding nodes directly to graph.')

            # Retrieve all node coordinates
            for node in range(nodes):
                i, x, y = map(float, g.readline().split())
                n = Node(index=int(i), x=x, y=y)
                node_cache[int(i)] = n

                # Add the node to the networkx graph
                if networkx_graph is not None:
                    networkx_graph.add_node(n)

            # Connect all nodes together based on edge declarations in file
            for edge in range(edges):
                from_node, to_node = map(int, g.readline().split())
                node_cache[from_node].children.add(node_cache[to_node])
                node_cache[to_node].children.add(node_cache[from_node])

                # This is nice to have
                edge_set.append((from_node, to_node))

                # Add the edge in the networkx graph
                if networkx_graph is not None:
                    networkx_graph.add_edge(node_cache[from_node], node_cache[to_node])

        if lightweight:
            return [n.index for n in node_cache.values()], edge_set
        else:
            return node_cache.values(), edge_set


class CSPState(object):
    """
    This class represent a state in a GAC problem, and contains
    only the current domain sets for all the nodes in the problem.

    A contradiction flag can be set during iteration
    """

    def __init__(self, nodes={}):
        """
        Constructor, takes in dict mapping from node to domain set
        """

        self.nodes = nodes
        self.contradiction = False


class AStarState(Node):
    """
    The AstarNode is a specialization of a Node, that in addition keeps track of arc-cost, start and goal flags,
    as well as F, G and H values.
    """

    def __init__(self, index=None, x=None, y=None):
        super(AStarState, self).__init__(index=index, x=x, y=y)
        self.is_start = None
        self.is_goal = None
        self.state = None
        self.arc_cost = 1
        self.g = 0
        self.h = 0
        self.f = 0
        self.walkable = True
        self.full_repr_mode = True

    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f

    def __gt__(self, other):
        if self.f == other.f:
            return self.h > other.h
        return self.f > other.f

    def __repr__(self):
        if self.full_repr_mode:
            return 'A*Node(%d, %d, F: %d, G: %d, H: %d)' % (self.x, self.y, self.f, self.g, self.h)
        else:
            return 'A*Node(%d (%d, %d))' % (self.index, self.x, self.y)
