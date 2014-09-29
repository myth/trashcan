# -*- coding: utf-8 -*-

import sys

from Tkinter import Tk

from view import Main

def parse_args(root):

    tasks = ['1']

    try:
        task = sys.argv[1]
    except IndexError:
        print u'Insufficient arguments'
        exit(1)
    if task not in tasks:
        print u'Invalid task. Choose from: %s' % u','.join(tasks)
        exit(1)
    else:
        if task == '1':
            return Main(root)


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
    app = parse_args(root)
    root.mainloop()
