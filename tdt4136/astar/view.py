# -*- coding: utf-8 -*-

from Tkinter import Frame, Menu, BOTH

class Main(Frame):
    
    def __init__(self, parent):

        Frame.__init__(self, parent, background='white')

        self.parent = parent

        self.initUI()

    def initUI(self):
        
        menubar = Menu(self.parent)

        self.parent.config(menu=menubar)
        self.parent.title('A-Star')

        file_menu = Menu(menubar)
        file_menu.add_command(label='Exit', command=self.onExit)
        menubar.add_cascade(label='File', menu=file_menu)

        self.pack(fill=BOTH, expand=1)

    def onExit(self):
        self.quit()
