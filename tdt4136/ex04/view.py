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
        boardsmenu.add_command(label=u'5x5 K2', command=lambda: self.createboard(5,5,2))
        boardsmenu.add_command(label=u'6x6 K2', command=lambda: self.createboard(6,6,2))
        boardsmenu.add_command(label=u'8x8 K1', command=lambda: self.createboard(8,8,1))
        boardsmenu.add_command(label=u'10x10 K3', command=lambda: self.createboard(10,10,3))

        runmenu = Menu(menubar, tearoff=0)
        runmenu.add_command(label=u'Go!', command=lambda: self.perform_sa())

        menubar.add_cascade(label=u'Boards', menu=boardsmenu)
        menubar.add_cascade(label=u'Run', menu=runmenu)

        self.pack(fill=BOTH, expand=1)

    def createboard(self, m, n, k):
        """
        Initiate a clean board
        """
        self.board = EggCarton(m, n, k)
        self.createmap()

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

    def perform_sa(self):
        """
        This runs the Simulated Annealing algorithm on the current board
        """

        self.createmap()

        if self.board:
            best = sa(self.board)
            self.draw_markers(best)
        else:
            return

    def draw_markers(self, board):
        """
        This helper method draws dots on the nodes visited by a particular algorithm,
        specified by a list if nodes in the order the algorithm visited them.

        :param trail: A list of nodes that are to be drawn onto the map, represented by dots.
        """
        color = 'red'
        if board.objective() == 1.0:
            color = 'green'
        for y in xrange(len(board.matrix)):
            for x in xrange(len(board.matrix[y])):
                if board.matrix[y][x] == 1:
                    coords = (
                        x * 30 + 2 + 10,
                        y * 30 + 2 + 10,
                        x * 30 + 32 - 10,
                        y * 30 + 32 - 10,
                    )
                    self.canvas.create_oval(*coords, fill=color, width=0)
