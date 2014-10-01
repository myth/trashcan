# -*- coding: utf-8 -*-

import os
import logging
import time

from Tkinter import *

from algorithms import *
from datastructures import *


class Main(Frame):
    """
    Main window frame for the GUI
    """

    def __init__(self, parent):
        """
        Initialize the frame, set parent container and initialize the board field
        Also delegates to the initUI method for widget and geometry setup
        """
        Frame.__init__(self, parent, background='white')

        self.parent = parent
        self.board = None
        self.canvas = None
        self.init_ui()

    def init_ui(self):
        """
        Helper method to set up widgets, customize them and add menu structure
        """
        menubar = Menu(self.parent)

        self.parent.config(menu=menubar)
        self.parent.title(u'A-Star')

        filemenu = Menu(menubar)
        filemenu.add_command(label=u'Exit', command=self.on_exit)
        boardsmenu = Menu(menubar)
        menubar.add_cascade(label=u'File', menu=filemenu)
        menubar.add_cascade(label=u'Boards', menu=boardsmenu)
        algorithmmenu = Menu(menubar)
        menubar.add_cascade(label=u'Algorithms', menu=algorithmmenu)
        algorithmmenu.add_command(label=u'Astar', command=self.perform_astar)

        self.add_boards_to_menu(boardsmenu)

        self.canvas = Canvas(self, width=800, height=580)
        self.canvas.config(bg='white')
        self.canvas.pack(fill=BOTH, expand=1)

        self.pack(fill=BOTH, expand=1)

    def createmap(self, f=None):
        """
        Creates a canvas map of colored squares based on the board created
        by the file parameter and the color field of the Node instances.
        :param f: Takes a full path to a board file
        """

        logging.debug('Creating map from %s' % os.path.basename(f))

        with open(f) as board:
            self.board = Board(board.read())

        self.canvas.delete('all')

        for y in xrange(len(self.board.matrix)):
            for x in xrange(len(self.board.matrix[y])):
                coords = (
                    x * 30 + 2,
                    y * 30 + 2,
                    x * 30 + 32,
                    y * 30 + 32,
                )

                self.canvas.create_rectangle(*coords,
                                             fill=self.board.matrix[y][x].color)

        self.board.update_manhattan_distance()

    def add_boards_to_menu(self, menu):
        """
        Dynamically create the boards submenu
        :param menu: Takes in an instance of a top level menu element
        """
        files = [f for f in os.listdir('./boards/') if '.txt' in os.path.basename(f)]
        files = sorted(files)
        for f in files:
            fullpath = os.path.join(os.getcwd(), 'boards', f)
            menu.add_command(label=os.path.basename(f),
                             command=lambda fp=fullpath: self.createmap(f=fp))

    def on_exit(self):
        """
        Close the application
        """
        self.quit()

    def draw_trail(self, trail):
        """
        This helper method draws dots on the nodes visited by a particular algorithm,
        specified by a list if nodes in the order the algorithm visited them.

        :param trail: A list of nodes that are to be drawn onto the map, represented by dots.
        """
        for node in trail:
            coords = (
                node.x * 30 + 2 + 10,
                node.y * 30 + 2 + 10,
                node.x * 30 + 32 - 10,
                node.y * 30 + 32 - 10,
            )
            self.canvas.create_oval(*coords, fill='cyan', width=0)

    def perform_astar(self):
        """
        This command is triggered from the application Algorithm menu, and initiates the a_star algorithm.
        It then calls the draw_trail helper method.
        """
        logging.debug('Start %s' % self.board.get_start())
        logging.debug('Dest %s' % self.board.get_goal())

        trail = a_star(self.board.graph, self.board.get_start(), self.board.get_goal())
        self.draw_trail(trail)
