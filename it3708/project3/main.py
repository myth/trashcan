# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/18/16

import numpy as np
from logging import getLogger
from logging.config import dictConfig

import settings
from modules.evolution import EvolutionLoop
from modules.flatland import Agent
from modules.gui import Main


def main():
    """
    Main program for EA+NN FlatLand solution
    """

    # Set up logging
    dictConfig(config=settings.LOG_CONFIG)
    log = getLogger('main')
    log.info('Starting EA')

    # Spawn the Tkinter frame and run the mainloop
    frame = Main()

    def on_closing():
        frame.master.destroy()
        frame.master.quit()

    frame.master.protocol("WM_DELETE_WINDOW", on_closing)
    frame.mainloop()


if __name__ == '__main__':
    main()
