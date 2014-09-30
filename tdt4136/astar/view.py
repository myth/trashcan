# -*- coding: utf-8 -*-

import os

from Tkinter import *
from tkFont import Font
from ScrolledText import ScrolledText

from algorithms import *

class Main(Frame):
    
    def __init__(self, parent):

        Frame.__init__(self, parent, background='white')

        self.parent = parent

        self.initUI()

    def initUI(self):
        
        menubar = Menu(self.parent)

        self.parent.config(menu=menubar)
        self.parent.title(u'A-Star')

        file_menu = Menu(menubar)
        file_menu.add_command(label=u'Exit', command=self.onExit)
        boards_menu = Menu(menubar)
        menubar.add_cascade(label=u'File', menu=file_menu)
        menubar.add_cascade(label=u'Boards', menu=boards_menu)

        self.add_boards(boards_menu)

        self.txt = Text(self)
        self.scrollbar = Scrollbar(self)
        
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.txt.pack(side=LEFT, fill=Y)
        self.scrollbar.config(command=self.txt.yview)
        self.txt.config(yscrollcommand=self.scrollbar.set)
        self.txt['font'] = ('Liberation Mono', 12, 'normal')

        self.pack(fill=BOTH, expand=1)

    def settext(self, text='', file=None):
        if file:
            with open(file, 'r') as fil:
                text = fil.read()
                fil.close()
        self.txt.delete('1.0', END)
        self.txt.insert('1.0', text)
        self.txt.mark_set(INSERT, '1.0')
        self.txt.focus()

    def appendtext(self, text='', file=None):
        if file:
            with open(file, 'r') as fil:
                text = fil.read()
                fil.close()
        self.txt.insert(END, text)
        self.txt.mark_set(INSERT, END)
        self.txt.focus()

    def add_boards(self, file_menu):
        files = [f for f in os.listdir('./boards/') if '.txt' in os.path.basename(f)]
        files = sorted(files)
        for f in files:
            full_path = os.path.join(os.getcwd(), 'boards', f)
            print full_path
            file_menu.add_command(label=os.path.basename(f), command=lambda full_path=full_path: self.settext(file=full_path))

    def onExit(self):
        self.quit()
