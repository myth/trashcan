# -*- coding: utf-8 -*-

from Tkinter import Frame, Menu, BOTH
from ScrolledText import ScrolledText

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
        menubar.add_cascade(label=u'File', menu=file_menu)

        self.txt = ScrolledText(self.parent, undo=False)
        self.txt['font'] = ('consolas', '12')
        self.txt.pack(expand=True, fill=BOTH)

        self.pack(fill=BOTH, expand=1)

    def onExit(self):
        self.quit()
