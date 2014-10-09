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
        self.current_file = None
        self.canvas = None
        self.view_level = 0
        self.init_ui()

    def init_ui(self):
        """
        Helper method to set up widgets, customize them and add menu structure
        """
        
        menubar = Menu(self.parent)

        self.parent.config(menu=menubar)
        self.parent.title(u'Simulated Annealing')

        boardsmenu = Menu(menubar, tearoff=0)

        menubar.add_cascade(label=u'Boards', menu=boardsmenu)

        self.canvas = Canvas(self, width=800, height=580)
        self.canvas.config(bg='white')
        self.canvas.pack(fill=BOTH, expand=1)

        self.pack(fill=BOTH, expand=1)

    def createmap(self, f=None):
        """
        Creates a board object with a matrix and adjacency graph given
        by the file parameter.
        :param f: Takes a full path to a board file
        """

        logging.debug('Creating map from %s' % os.path.basename(f))
        self.current_file = f
       
        self.canvas.delete('all')

        # TODO: Map creation logic

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

        # TODO Canvas draw logic
