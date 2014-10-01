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
        self.view_level = 0
        self.init_ui()

    def init_ui(self):
        """
        Helper method to set up widgets, customize them and add menu structure
        """
        
        menubar = Menu(self.parent)

        self.parent.config(menu=menubar)
        self.parent.title(u'A-Star')

        boardsmenu = Menu(menubar, tearoff=0)
        algorithmmenu = Menu(menubar, tearoff=0)
        optionsmenu = Menu(menubar, tearoff=0)

        menubar.add_cascade(label=u'Boards', menu=boardsmenu)
        menubar.add_cascade(label=u'Algorithms', menu=algorithmmenu)
        menubar.add_cascade(label=u'Options', menu=optionsmenu)
       
        algorithmmenu.add_command(label=u'Astar', command=self.perform_astar)

        optionsmenu.add_command(label=u'Show trail only', state=DISABLED, command=self.only_show_trail)
        optionsmenu.add_command(label=u'Show all states', command=self.show_all_states)

        self.add_boards_to_menu(boardsmenu)

        self.canvas = Canvas(self, width=800, height=580)
        self.canvas.config(bg='white')
        self.canvas.pack(fill=BOTH, expand=1)

        self.pack(fill=BOTH, expand=1)

        self.optionsmenu = optionsmenu

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

        self.board.create_h_values()

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

    def draw_markers(self, nodes, icon):
        """
        This helper method draws dots on the nodes visited by a particular algorithm,
        specified by a list if nodes in the order the algorithm visited them.

        :param trail: A list of nodes that are to be drawn onto the map, represented by dots.
        """
        for node in nodes:
            coords = (
                node.x * 30 + 2 + 10,
                node.y * 30 + 2 + 10,
                node.x * 30 + 32 - 10,
                node.y * 30 + 32 - 10,
            )
            if icon == 'path':
                self.canvas.create_oval(*coords, fill='cyan', width=0)
            elif icon == 'open':
                self.canvas.create_oval(*coords, fill='black', width=0)
            elif icon == 'closed':
                self.canvas.create_line(*coords)
                self.canvas.create_line(coords[2], coords[1], coords[0], coords[3])

    def perform_astar(self):
        """
        This command is triggered from the application Algorithm menu, and initiates the a_star algorithm.
        It then calls the draw_markers helper method to draw trail, openset and closedset depending on view_level.
        """
        logging.debug('Start %s' % self.board.get_start())
        logging.debug('Dest %s' % self.board.get_goal())

        trail, openlist, closedlist = a_star(self.board.graph, self.board.get_start(), self.board.get_goal())
        self.draw_markers(trail, 'path')
        if self.view_level > 0:
            self.draw_markers(openlist, 'open')
            for node in trail:
                if node in closedlist:
                    closedlist.remove(node)
            self.draw_markers(closedlist, 'closed')

    def only_show_trail(self):
        """
        Set the view level to only show the path taken
        """
        self.optionsmenu.entryconfig(0, state=DISABLED)
        self.optionsmenu.entryconfig(1, state=NORMAL)
        self.view_level = 0

    def show_all_states(self):
        """
        Set the view level to show both path taken, openset and closedset
        """
        self.optionsmenu.entryconfig(0, state=NORMAL)
        self.optionsmenu.entryconfig(1, state=DISABLED)
        self.view_level = 1
