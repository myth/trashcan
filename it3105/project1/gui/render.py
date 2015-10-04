# -*- coding: utf8 -*-
#
# Created by 'myth' on 8/26/15

import matplotlib
matplotlib.use('tkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import networkx as nx
import numpy as np

from tkinter import Canvas, BOTH, messagebox

from common import debug, COLORMAP, BOARD_CELL_SIZE


class AbstractRenderer(object):
    """
    Abstract base class for renderer objects
    """

    def __init__(self, window):
        """
        Constructor
        :param window: Reference to the main window instance
        """
        self.window = window
        self.board = None
        self.board_height = 0
        self.controller = None

    def set_board(self, board):
        """
        Sets a board
        :param board: Sets an active board to the renderer object
        """

        self.board = board
        self.board_height = len(self.board.grid)

    def destruct(self):
        """
        Destroys this renderer
        """

        pass

    def set_controller(self, controller):
        """
        Sets a reference to the controller object
        """

        self.controller = controller

    @staticmethod
    def rgb_to_color(r, g, b):
        """
        Transforms an RGB color value to HEX
        """

        return '#%02x%02x%02x' % (r, g, b)


class CanvasRenderer(AbstractRenderer):
    """
    The CanvasRenderer can draw figures and grids on a canvas
    """

    def __init__(self, window):
        """
        Constructor
        :param window: Reference to the main window instance
        """

        super().__init__(window)

        self.canvas = Canvas(self.window)
        self.canvas.grid(row=0, column=0, padx=BOARD_CELL_SIZE, ipadx=10, ipady=10, sticky='nsew')
        self.path_sprites = set()

    def render_board(self, math_coords=False):
        """
        Renders the data
        """

        debug('CanvasRenderer.render_board() called')

        if not self.board:
            messagebox.showerror(
                'No Board',
                'No board has been selected, cannot render'
            )

        self.clear()
        payload = self.board.grid

        row_range = range(0, self.board_height)
        # If we are drawing using mathematical coordinates (Y-axis reversed)
        if math_coords:
            row_range = range(self.board_height - 1, -1, -1)

        # Iterate through all nodes, create sprite coords and determine fill color
        for y in row_range:
            for x in range(len(payload[y])):

                draw_y = y
                if math_coords:
                    draw_y = self.board_height - y

                coords = (
                    x * BOARD_CELL_SIZE + 1,
                    draw_y * BOARD_CELL_SIZE + 1,
                    x * BOARD_CELL_SIZE + BOARD_CELL_SIZE + 1,
                    draw_y * BOARD_CELL_SIZE + BOARD_CELL_SIZE + 1,
                )

                node = self.board.get_node(x, y)
                fill_color = '#FFFFFF'
                if not node.walkable:
                    fill_color = '#000000'
                elif node.is_start:
                    fill_color = '#4040FF'
                elif node.is_goal:
                    fill_color = '#40FF40'

                self.canvas.create_rectangle(
                    *coords,
                    fill=fill_color
                )

    def render_path(self, path, math_coords=False, **kwargs):
        """
        Renders path nodes on top of the map, after clearing previously rendered path nodes
        :param path: A list of Node objects
        """

        open_set = kwargs['open_set_size']
        closed_set = kwargs['closed_set_size']

        # Remove all previously rendered path sprites from canvas
        for sprite in self.path_sprites:
            self.canvas.delete(sprite)

        self.path_sprites.clear()

        if 'nonogram' in kwargs and kwargs['nonogram'] is not None:
            p = kwargs['nonogram']
            for y in range(p.total_rows):
                for x in range(len(p.nodes[y][0][1])):
                    coords = (
                        x * BOARD_CELL_SIZE + 1,
                        y * BOARD_CELL_SIZE + 1,
                        x * BOARD_CELL_SIZE + BOARD_CELL_SIZE + 1,
                        y * BOARD_CELL_SIZE + BOARD_CELL_SIZE + 1
                    )

                    fill_color = '#FFFFFF'

                    if p.nodes[y][0][1][x]:
                        fill_color = '#22EE22'

                    # Create sprite and add to path sprite cache
                    self.path_sprites.add(
                        self.canvas.create_rectangle(
                            *coords,
                            fill=fill_color
                        )
                    )

            self.window.master.controller.references['path_length'].set(
                'Path length: %d' % (len(path) - 1)
            )
            self.window.master.controller.references['open_set_size'].set(
                'OpenSet size: %d' % open_set
            )
            self.window.master.controller.references['closed_set_size'].set(
                'ClosedSet size: %d' % (closed_set - 1)
            )
            self.window.master.controller.references['total_set_size'].set(
                'Total set size: %d' % (open_set + closed_set - 1)
            )

        else:
            # Add sprites for current path
            for node in reversed(path[:-1]):
                # If we are drawing using mathematical coordinates (y-reversed)
                y = node.y
                if math_coords:
                    y = self.board_height - node.y

                # Create the coordinates and dimension tuple
                coords = (
                    node.x * BOARD_CELL_SIZE + 1,
                    y * BOARD_CELL_SIZE + 1,
                    node.x * BOARD_CELL_SIZE + BOARD_CELL_SIZE + 1,
                    y * BOARD_CELL_SIZE + BOARD_CELL_SIZE + 1
                )

                fill_color = '#994499'

                # Create sprite and add to path sprite cache
                self.path_sprites.add(
                    self.canvas.create_rectangle(
                        *coords,
                        fill=fill_color
                    )
                )

                self.window.master.controller.references['path_length'].set(
                    'Path length: %d' % (len(path) - 1)
                )
                self.window.master.controller.references['open_set_size'].set(
                    'OpenSet size: %d' % open_set
                )
                self.window.master.controller.references['closed_set_size'].set(
                    'ClosedSet size: %d' % closed_set
                )
                self.window.master.controller.references['total_set_size'].set(
                    'Total set size: %d' % (open_set + closed_set)
                )

    def clear(self):
        """
        Clears the content area
        """

        self.canvas.delete('all')
        self.window.master.controller.clear_timers()
        self.window.master.controller.clear_stats()

    def destruct(self):
        """
        Destroys this canvas
        """

        self.window.master.controller.clear_timers()
        self.window.master.controller.clear_stats()
        self.canvas.destroy()


class GraphRenderer(AbstractRenderer):
    """
    GraphRenderer
    """

    def __init__(self, window, figsize=(8, 7)):
        super(GraphRenderer, self).__init__(window)

        # Settings for the renderer
        self.show_labels = False

        # Hook up a matplotlib figure and subplot for networkx and FigureCanvas to talk to
        self.figure = plt.figure(figsize=figsize)
        self.axis = self.figure.add_subplot(111)
        plt.axis('off')
        self.figure.tight_layout()

        # Initialize a networkx graph
        self.graph = nx.Graph()
        self.pos = None

        # Initialize the FigureCanvas
        self.canvas = FigureCanvasTkAgg(self.figure, master=window)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, window)
        self.toolbar.update()
        self.toolbar.pack()

        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        self.canvas.show()

        # This will eventually hold a matplotlib.collections.PathCollection of vectors
        # that can be re-drawns after using a new colors array
        self.sprites = None

    def add_nodes_to_graph(self, nodes):
        """
        Helper method that takes in our node objects and injects it into the networkx graph object
        """

        debug('Adding %d nodes to NetworkX Graph instance' % len(nodes))

        self.graph.add_nodes_from(nodes)
        for node in nodes:
            for child in node.children:
                self.graph.add_edge(node, child)

    def clear(self):
        """
        Clears the canvas
        """

        self.graph.clear()
        self.axis.cla()
        self.window.master.controller.clear_timers()
        self.window.master.controller.clear_stats()

    def destruct(self):
        """
        Detroys this renderer
        """

        self.graph = None
        try:
            self.toolbar.destroy()
        except AttributeError as e:
            debug("AttributeError bug in matplotlib FigureCanvasTkAgg toolbar catched during destroy()")
        self.canvas.get_tk_widget().destroy()

    def generate_layout(self):
        """
        Generates a NetworkX compatible dictionary of node to numpy array mappings for graph layout
        """

        min_x = float('Inf')
        max_x = 0
        min_y = float('Inf')
        max_y = 0

        self.pos = {}

        for node in self.graph.nodes():
            if node.x < min_x:
                min_x = node.x
            if node.x > max_x:
                max_x = node.x
            if node.y < min_y:
                min_y = node.y
            if node.y > max_y:
                max_y = node.y

        for node in self.graph.nodes():
            x = float(node.x) / max_x
            y = float(node.y) / max_y
            self.pos[node] = np.array([x, y])

    def render_graph(self, **kwargs):
        """
        Renders the graph
        """

        self.axis.cla()
        plt.axis('off')

        self.generate_layout()

        if 'nodelist' in kwargs:
            nodelist = kwargs['nodelist']
        else:
            nodelist = self.graph.nodes()

        try:
            debug('Rendering graph. Nodelist length is: %d and of type %s' % (len(nodelist), type(nodelist[0]) or '?'))
        except IndexError:
            pass

        colors = ['black']

        self.sprites = nx.draw_networkx_nodes(
            self.graph,
            pos=self.pos,
            node_size=40,
            with_labels=self.show_labels,
            node_color=colors,
            **kwargs
        )
        nx.draw_networkx_edges(
            self.graph,
            pos=self.pos
        )

        self.canvas.draw()

    def generate_colors(self, astar_state):
        """
        Generates a list of colors that correlate to the nodes in the NetworkX Graph instance
        :return: A list of color strings
        """

        return [
            COLORMAP[list(astar_state.state.nodes[node.index])[0]] if len(astar_state.state.nodes[node.index]) == 1
            else 'black' for node in self.graph.nodes()
        ]

    def render_path(self, **kwargs):

        path = kwargs['p']
        open_set_size = kwargs['open_set_size']
        closed_set_size = kwargs['closed_set_size']

        if len(path) < 2:
            return
        else:
            self.sprites.set_facecolor('black')

        self.window.master.controller.references['path_length'].set(
            'Path length: %d' % len(path)
        )
        self.window.master.controller.references['open_set_size'].set(
            'OpenSet size: %d' % open_set_size
        )
        self.window.master.controller.references['closed_set_size'].set(
            'ClosedSet size: %d' % closed_set_size
        )
        self.window.master.controller.references['total_set_size'].set(
            'Total set size: %d' % (open_set_size + closed_set_size)
        )

        if not self.pos:
            self.pos = nx.random_layout(self.graph)

        colors = self.generate_colors(path[0])
        self.sprites.set_facecolors(colors)
        self.canvas.draw()
