# -*- coding: utf-8 -*-

import sys

from Tkinter import Tk

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
    root.mainloop()
