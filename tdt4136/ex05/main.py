# -*- coding: utf-8 -*-
"""
This is the main program file for the A* application

Authors: Fredrik B. Tørnvall & Aleksander Skraastad
"""
import datetime
import logging

from Tkinter import *

from algorithms import *
from view import Main


def center_window(r):
    """
    Takes in a r widget, and positions the window to center of screen
    :param r: Takes the root window widget as an argument
    """

    width = 1280
    height = 600

    screen_width = r.winfo_screenwidth()
    screen_height = r.winfo_screenheight()

    x = (screen_width - width) / 2
    y = (screen_height - height) / 2

    r.geometry('%dx%d+%d+%d' % (width, height, x, y))


if __name__ == '__main__':
    """
    Main run method
    """

    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    logging.debug('Starting program at %s' % datetime.datetime.utcnow().strftime('%H:%M:%S'))

    root = Tk()
    center_window(root)
    app = Main(root)

    root.mainloop()
