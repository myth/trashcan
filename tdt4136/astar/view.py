# -*- coding: utf-8 -*-

from Tkinter import Frame, Menu, Text, Scrollbar, BOTH

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

        self.parent.grid_propagate(False)
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        self.txt = Text(self, borderwidth=3, relief='sunken')
        self.txt.config(font=('consolas', 12), undo=True, wrap='word')
        self.txt.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)

        scrollbar = Scrollbar(self, command=self.txt.yview)
        scrollbar.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollbar.set

        self.pack(fill=BOTH, expand=1)

    def onExit(self):
        self.quit()
