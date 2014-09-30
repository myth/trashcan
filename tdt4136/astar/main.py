# -*- coding: utf-8 -*-

import sys
import os
import logging
import time
import datetime

from Tkinter import *

from algorithms import *
from datastructures import *
from view import Main

def center_window(root):
    """
    Takes in a root widget, and positions the window to center of screen
    """

    width = 1280
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

    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    logging.debug('Starting program at %s' % datetime.datetime.utcnow().strftime('%H:%M:%S'))
    
    root = Tk()
    center_window(root)
    app = Main(root)

    #app.appendtext(aStar(board.matrix, board.get_start(), board.get_goal()))

    root.mainloop()
