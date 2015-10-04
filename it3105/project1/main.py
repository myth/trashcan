# -*- coding: utf8 -*-
#
# Created by 'myth' on 9/23/15

from gui.widgets import *
from common import *
from controller import MainController
from gui.window import Main
from gui.render import CanvasRenderer


if __name__ == '__main__':
    """
    Application start sequence
    """

    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    log('Starting application ...')

    root = Tk()
    root.wm_title('Project 1')
    root.wm_protocol('WM_DELETE_WINDOW', root.quit)

    # Render the main window
    main = Main(root, MainController(), name='main')
    main.controller.set_window(main)

    # Set the initial renderer
    renderer = CanvasRenderer(main.content_area)
    renderer.set_controller(main.controller)
    main.set_renderer(renderer)

    # Register menubar components
    generate_menus(main)

    # Generate stats and options pane
    generate_options(main.options_area)
    generate_stats(main.stats_area)

    # Fill the window with main frame
    main.grid(row=0, column=0)

    # Start application
    root.mainloop()
