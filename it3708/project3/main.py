# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/18/16

import cProfile
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

    # Create and start the EvolutionLoop
    el = EvolutionLoop()
    el.start()

    # Spawn the Tkinter frame and run the mainloop
    frame = Main()
    frame.controller.set('ea_loop', el)

    def run_flatland(i):
        agent = Agent(flatland=settings.FLATLANDS[i])
        frame.controller.agent = agent
        frame.draw_agent(agent)

        # Define an update function that moves the agent one step forward each UPDATE_INTERVAL
        def move_agent(flatland_index=i):
            move = [agent.forward, agent.left, agent.right][np.argmax(el.nn.test(agent.sense()))]
            move()
            frame.draw_agent(agent)
            if agent.steps < 60:
                frame.after(settings.GUI_UPDATE_INTERVAL, move_agent)
            else:
                flatland_index += 1
                if flatland_index < settings.FLATLAND_SCENARIOS:
                    frame.after(1500, lambda: run_flatland(flatland_index))

        frame.after(settings.GUI_UPDATE_INTERVAL, move_agent)

    run_flatland(0)
    frame.mainloop()


if __name__ == '__main__':
    cProfile.run('main()')
