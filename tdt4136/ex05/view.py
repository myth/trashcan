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

        self.canvas = Canvas(self, width=800, height=580)
        self.canvas.config(bg='white')
        self.canvas.pack(fill=BOTH, expand=1)

        boardsmenu = Menu(menubar, tearoff=0)

        menubar.add_cascade(label=u'Boards', menu=boardsmenu)

        self.pack(fill=BOTH, expand=1)

    def createmap(self):
        """
        Creates a board object with a matrix and adjacency graph given
        by the file parameter.
        """
       
        self.canvas.delete('all')

        for y in xrange(len(self.board.matrix)):
            for x in xrange(len(self.board.matrix)):
                coords = (
                    x * 30 + 2,
                    y * 30 + 2,
                    x * 30 + 32,
                    y * 30 + 32,
                )

                self.canvas.create_rectangle(*coords,
                                             fill="gray")

