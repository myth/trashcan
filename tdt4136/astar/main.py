# -*- coding: utf-8 -*-

import sys
from algorithms import *
from datastructures import *
import os

from Tkinter import *

from view import Main

def center_window(root):
    """
    Takes in a root widget, and positions the window to center of screen
    """

    width = 800
    height = 600

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - width) / 2
    y = (screen_height - height) / 2

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


if __name__ == '__main__':
    """
    Main run method
    """
    
    root = Tk()
    center_window(root)
    app = Main(root)

    #app.appendtext(aStar(board.matrix, board.get_start(), board.get_goal()))

    root.mainloop()
