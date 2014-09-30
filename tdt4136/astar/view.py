# -*- coding: utf-8 -*-

import os
from random import randint
import logging

from Tkinter import *
from tkFont import Font

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

        self.initUI()

    def initUI(self):
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

        self.add_boards_to_menu(boardsmenu)

        self.canvas = Canvas(self, width=800, height=580)
        self.canvas.config(bg='white')
        self.canvas.pack(fill=BOTH, expand=1)

        self.pack(fill=BOTH, expand=1)

    def createmap(self, file=None):
        """
        Creates a canvas map of colored squares based on the board created
        by the file parameter and the color field of the Node instances.
        """

        logging.debug('Creating map from %s' % os.path.basename(file))

        with open(file, 'r') as board:
            self.board = Board(board.read())

        self.canvas.delete('all')

        for y in xrange(len(self.board.matrix)):
            for x in xrange(len(self.board.matrix[y])):
                coords = (
                    x*30 + 2,
                    y*30 + 2,
                    x*30 + 32,
                    y*30 + 32,
                )

                self.canvas.create_rectangle(*coords,
                    fill=self.board.matrix[y][x].color)

    def add_boards_to_menu(self, filemenu):
        """
        Dynamically create the boards submenu
        """
        files = [f for f in os.listdir('./boards/') if '.txt' in os.path.basename(f)]
        files = sorted(files)
        for f in files:
            fullpath = os.path.join(os.getcwd(), 'boards', f)
            filemenu.add_command(label=os.path.basename(f),
                command=lambda fullpath=fullpath: self.createmap(file=fullpath))

    def on_exit(self):
        """
        Close the application
        """
        self.quit()
