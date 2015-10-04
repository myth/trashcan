# -*- coding: utf8 -*-
#
# Created by 'myth' on 8/26/15

from tkinter import *
from tkinter import messagebox

from common import log, debug
from gui.render import CanvasRenderer, GraphRenderer


class Main(Frame):
    """
    Main window
    """

    def __init__(self, parent, controller, *args, **kwargs):
        """
        Main window constructor. Takes in a root widget as an argument.
        """

        # Invoke superclass constructor with root widget
        Frame.__init__(self, parent, *args, **kwargs)

        menu = Menu(parent)

        self.parent = parent
        self.menu = menu
        self.renderer = None
        self.controller = controller

        parent.config(menu=menu)

        self.content_area = LabelFrame(self, text='Visualization', name='visualization')
        self.content_area.grid(
            row=0,
            column=0,
            rowspan=2,
            sticky='nsew',
            padx=5,
            pady=5,
            ipadx=0,
            ipady=0
        )

        self.options_area = LabelFrame(self, text='Options', name='options')
        self.options_area.grid(
            row=0,
            column=1,
            sticky='nsew',
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5,
            columnspan=2
        )

        self.stats_area = LabelFrame(self, text='Stats', name='stats')
        self.stats_area.grid(
            row=1,
            column=1,
            sticky='nsew',
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5,
            columnspan=2
        )

        stats_label = Label(self.stats_area, text='')

    def set_window_size(self, x=1280, y=600):
        """
        Sets the dimensions of the main window
        """

        self.parent.geometry('%dx%d+0+0' % (x, y))
        debug('Window size set to: %d x %d' % (x, y))

    def maximize_window(self):
        """
        Maximizes the window size
        """

        self.parent.attributes('-zoomed', True)

    def fullscreen_window(self):
        """
        Enables fullscreen window mode
        """

        self.parent.attributes('-fullscreen', True)

    def set_renderer(self, renderer):
        """
        Sets the active renderer to this window
        """

        debug('Setting renderer to %s' % renderer)

        if self.renderer and renderer is not self.renderer:
            debug('Destroying and replacing old renderer: %s' % self.renderer)
            self.renderer.destruct()
        self.renderer = renderer

    def render(self, *args, **kwargs):
        """
        Renders the main content area, based on a provided render function
        """

        if self.renderer:
            if isinstance(self.renderer, CanvasRenderer):
                self.renderer.render_board(*args, **kwargs)
            elif isinstance(self.renderer, GraphRenderer):
                self.renderer.render_graph(*args, **kwargs)
            debug('Main.render() called')
        else:
            messagebox.showerror(
                'Missing renderer',
                'Main.render() invoked without renderer set'
            )
            log('Main.render() invoked without renderer set')
