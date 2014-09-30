# -*- coding: utf-8 -*-

import sys
from algorithms import *
from datastructures import *
import os

from Tkinter import *

from view import Main

def center_window(root):

    width = 800
    height = 600

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - width) / 2
    y = (screen_height - height) / 2

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


if __name__ == '__main__':
    
    root = Tk()
    center_window(root)
    app = Main(root)
    app.appendtext('Skeet mcskeet\n')

    with open(os.path.join(os.getcwd(), 'boards', 'board-1-1.txt'), 'r') as text:
        board = Board(text.read())

    app.appendtext(aStar(board.matrix, board.get_start(), board.get_goal()))

    root.mainloop()
