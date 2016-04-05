# -*- coding: utf8 -*-
#
# Created by 'myth' on 3/17/16

import logging
import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np
import settings
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modules.evolution import EvolutionLoop
from modules.flatland import FOOD, PLAYER, POISON, Agent


class Controller(object):
    """
    View controller for the Tkinter frame
    """

    def __init__(self, main_frame):
        """
        Constructor that takes a reference to the main Tkinter frame
        :param main_frame: The Main Tkinter frame
        """

        self._log = logging.getLogger(__name__)
        self.frame = main_frame
        self.options_menu = None
        self.scenarios_menu = None
        self.agent = None
        self._options = {
            'scenarios': settings.FLATLAND_SCENARIOS,
            'dynamic': settings.FLATLAND_DYNAMIC
        }

    def run(self):
        """
        Run an agent through the FlatLand scenario(s) given current settings
        """

        frame = self.frame
        el = EvolutionLoop()
        self.set('ea_loop', el)

        # Define EA generational statistics plot function
        def update_plot(results):
            """
            Update the Matplotlib plot with history up until the current generation
            :param results: History of results so far
            """

            self._log.debug('Updating plot with results: %s' % results)

            gen = []
            avg_fit = []
            std_dev = []
            max_fit = []
            for r in results:
                g, a, s, m = r
                gen.append(g)
                avg_fit.append(a)
                std_dev.append(s)
                max_fit.append(m)

            # Grab our canvas plot references and clear 'em
            fig, ax1, ax2 = frame.fig, frame.ax1, frame.ax2
            ax1.clear()
            ax2.clear()

            ax1.plot(gen, max_fit, '-', color='g', label='MaxFit')
            ax1.plot(gen, avg_fit, '--', color='b', label='Avg.Fit')
            ax1.set_xlabel('Generation', color='black')
            ax1.set_ylabel('Fitness', color='blue')
            for tl in ax1.get_yticklabels():
                tl.set_color('b')

            ax2.plot(gen, std_dev, '--', color='r', label='Std.Dev')
            ax2.set_ylabel('Std.Dev', color='r')
            for tl in ax2.get_yticklabels():
                tl.set_color('r')

            ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), mode='expand', ncol=3, loc=3, borderaxespad=0.)
            frame.plot.draw()

        # Yield through each generation and update plot accordingly
        for res in el.start():
            update_plot(res)

        # Define flatland demo display function
        def run_flatland(i):
            """
            Async function that runs an agent through one FlatLand instance while drawing progress
            """
            agent = Agent(flatland=settings.FLATLANDS[i])
            self.agent = agent
            frame.draw_agent(agent)

            # Define an update function that moves the agent one step forward each UPDATE_INTERVAL
            def move_agent(flatland_index=i):
                """
                Async function that moves an agent one step forward in the recommended direction (from NNet)
                and draws the changes onto the canvas
                """

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

        # Start the agent on the first FlatLand instance
        run_flatland(0)

    def set(self, key, val):
        """
        Sets an option on this controller
        :param key: The key of the option
        :param val: The value of the option
        """

        self._options[key] = val

    def get(self, key):
        """
        Retrieve the value of an option on this controller
        :param key: The key of the option
        :return: The value of the option, or None if the key does not exist
        """

        return self._options.get(key)

    def set_dynamic(self):
        """
        Sets the run mode of the FlatLand to dynamic
        """

        om = self.options_menu
        om.entryconfig(0, state=tk.NORMAL)
        om.entryconfig(1, state=tk.DISABLED)

        self.set('dynamic', True)
        settings.FLATLAND_DYNAMIC = True
        self.get('mode_stringvar').set('Mode: dynamic')
        self._log.info('Dynamic mode enabled')

    def set_static(self):
        """
        Sets the run mode of the FlatLand to static
        """

        om = self.options_menu
        om.entryconfig(0, state=tk.DISABLED)
        om.entryconfig(1, state=tk.NORMAL)

        self.set('dynamic', False)
        settings.FLATLAND_DYNAMIC = False
        self.get('mode_stringvar').set('Mode: static')
        self._log.info('Static mode enabled')

    def set_one_scenario(self):
        """
        Sets the run mode of the FladLand to 1 scenario
        """

        sm = self.scenarios_menu
        sm.entryconfig(0, state=tk.DISABLED)
        sm.entryconfig(1, state=tk.NORMAL)

        self.set('scenarios', 1)
        settings.FLATLAND_SCENARIOS = 1
        self.get('scenarios_stringvar').set('Scenarios: %d' % 1)
        self._log.info('Number of scenarios set to 1')

    def set_five_scenarios(self):
        """
        Sets the run mode of the FlatLand to 5 scenarios
        """

        sm = self.scenarios_menu
        sm.entryconfig(0, state=tk.NORMAL)
        sm.entryconfig(1, state=tk.DISABLED)

        self.set('scenarios', 5)
        settings.FLATLAND_SCENARIOS = 5
        self.get('scenarios_stringvar').set('Scenarios: %d' % 5)
        self._log.info('Number of scenarios set to 5')

    def handle_arrow_up(self, event):
        """
        Event handler for arrow up key
        :param event: Event object
        """

        self._log.debug('Event: %s' % event)
        self.agent.forward()
        self.frame.draw_agent(self.agent)

    def handle_arrow_left(self, event):
        """
        Event handler for arrow up key
        :param event: Event object
        """

        self._log.debug('Event: %s' % event)
        self.agent.left()
        self.frame.draw_agent(self.agent)

    def handle_arrow_right(self, event):
        """
        Event handler for arrow up key
        :param event: Event object
        """

        self._log.debug('Event: %s' % event)
        self.agent.right()
        self.frame.draw_agent(self.agent)


class Main(tk.Frame):
    """
    Frame wrapper for the main
    """

    def __init__(self, master=None):
        super(Main, self).__init__(master=master)

        self._log = logging.getLogger(__name__)
        self.game = None
        self.canvas = None
        self.controller = Controller(self)

        self._init_gui()

    def draw_agent(self, agent):
        """
        Render the state of the provided agent and flatland instance
        :param agent: The Agent, with a contained FlatLand instance
        """

        if not self.canvas:
            return

        # Just clear everything, since we are lazy
        self.canvas.delete('object')

        board = agent.flatland.board
        position = agent.position
        direction = agent.direction

        rows = settings.FLATLAND_ROWS
        cols = settings.FLATLAND_COLS

        # Draw the initial grid
        for y in range(rows):
            for x in range(cols):
                # Move to next cell if empty
                if not board[y][x]:
                    continue

                # Cell bounds
                coords = (
                    x * 40 + 15,
                    y * 40 + 15,
                    x * 40 + 25,
                    y * 40 + 25
                )

                item = board[y][x]
                if item == PLAYER:
                    color = 'green'
                elif item == FOOD:
                    color = 'blue'
                else:
                    color = 'red'

                # Draw a circle
                self.canvas.create_oval(
                    *coords,
                    fill=color,
                    tags='object',
                    width=0,
                )

        # Draw a direction line for the player
        x, y = position
        dx, dy = direction
        self.canvas.create_line(
            x * 40 + 20,
            y * 40 + 20,
            (x + dx) * 40 + 20 - (20 * dx),
            (y + dy) * 40 + 20 - (20 * dy),
            tags='object'
        )

        # Update the statistics
        self.controller.get('fitness').set('Fitness: %.3f' % agent.fitness)
        self.controller.get('food').set('Food: %d' % agent.stats[FOOD])
        self.controller.get('poison').set('Poison: %d' % agent.stats[POISON])
        self.controller.get('steps').set('Steps: %d' % agent.steps)

        nn = self.controller.get('ea_loop').nn
        sensations = agent.sense()
        net_results = nn.test(sensations)
        recommended = np.argmax(net_results)

        self.controller.get('recommended').set(
            'Recommended: %s' % ['Forward', 'Left', 'Right'][recommended]
        )

    def _init_gui(self):
        """
        Initializes the GUI
        """

        # Start by setting up the menu structure
        menubar = tk.Menu(self.master)

        self.master.config(menu=menubar)
        self.master.title('FlatLand')

        options_menu = tk.Menu(menubar, tearoff=0)
        scenarios_menu = tk.Menu(menubar, tearoff=0)

        menubar.add_cascade(label='Options', menu=options_menu)
        menubar.add_cascade(label='Scenarios', menu=scenarios_menu)

        options_menu.add_command(label='Static', command=self.controller.set_static, state=tk.DISABLED)
        options_menu.add_command(label='Dynamic', command=self.controller.set_dynamic, state=tk.NORMAL)
        scenarios_menu.add_command(label='1', command=self.controller.set_one_scenario, state=tk.DISABLED)
        scenarios_menu.add_command(label='5', command=self.controller.set_five_scenarios, state=tk.NORMAL)

        # Attach the submenu trees to the controller for easy reference
        self.controller.options_menu = options_menu
        self.controller.scenarios_menu = scenarios_menu

        # Set up the canvas
        self._init_canvas()

        # Set up the sidebar
        self._init_sidebar()

        # Set up plot
        self._init_plot()

        # Set up listeners for arrow keys
        self._init_event_listeners()

        # Pack this frame
        self.pack(fill=tk.BOTH, expand=1)

    def _init_canvas(self):
        """
        Sets up the Canvas for this frame, and destroys potential previous canvas before initializing
        """

        if self.canvas:
            self.canvas.destroy()

        # Set up the canvas
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.config(bg='white')

        rows = settings.FLATLAND_ROWS
        cols = settings.FLATLAND_COLS

        # Draw the initial grid
        for y in range(rows):
            for x in range(cols):
                coords = (
                    x * 40,
                    y * 40,
                    x * 40 + 40,
                    y * 40 + 40
                )

                self.canvas.create_rectangle(
                    *coords,
                    fill='gray',
                    tags='cell'
                )

        self.canvas.pack(side=tk.LEFT)

    def _init_sidebar(self):
        """
        Sets up the sidebar frame for the master frame.
        """

        self.sidebar = tk.Frame(self, width=200, height=400)

        # Add mode text field
        mode_stringvar = tk.StringVar()
        mode_label = tk.Label(self.sidebar, textvariable=mode_stringvar, width=20)
        mode = self.controller.get('dynamic')
        mode_stringvar.set('Mode: %s' % ('dynamic' if mode else 'static'))
        mode_label.config(anchor='nw')
        mode_label.pack(fill=tk.X)
        self.controller.set('mode_stringvar', mode_stringvar)

        # Add scanarios text field
        scenarios_stringvar = tk.StringVar()
        scenarios_label = tk.Label(self.sidebar, textvariable=scenarios_stringvar, width=20)
        scenarios = self.controller.get('scenarios')
        scenarios_stringvar.set('Scenarios: %d' % scenarios)
        scenarios_label.config(anchor='nw')
        scenarios_label.pack(fill=tk.X)
        self.controller.set('scenarios_stringvar', scenarios_stringvar)

        # Add spacing
        separator = tk.Frame(self.sidebar, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, padx=2, pady=10)

        # Add fitness text field
        fitness_stringvar = tk.StringVar()
        fitness_label = tk.Label(self.sidebar, textvariable=fitness_stringvar, width=20)
        fitness = 0
        fitness_stringvar.set('Fitness: %d' % fitness)
        fitness_label.config(anchor='nw')
        fitness_label.pack(fill=tk.X)
        self.controller.set('fitness', fitness_stringvar)

        # Add food text field
        food_stringvar = tk.StringVar()
        food_label = tk.Label(self.sidebar, textvariable=food_stringvar, width=20)
        food = 0
        food_stringvar.set('Food: %d' % food)
        food_label.config(anchor='nw')
        food_label.pack(fill=tk.X)
        self.controller.set('food', food_stringvar)

        # Add poison text field
        poison_stringvar = tk.StringVar()
        poison_label = tk.Label(self.sidebar, textvariable=poison_stringvar, width=20)
        poison = 0
        poison_stringvar.set('Poison: %d' % poison)
        poison_label.config(anchor='nw')
        poison_label.pack(fill=tk.X)
        self.controller.set('poison', poison_stringvar)

        # Add steps text field
        steps_stringvar = tk.StringVar()
        steps_label = tk.Label(self.sidebar, textvariable=steps_stringvar, width=20)
        steps = 0
        steps_stringvar.set('Steps: %d' % steps)
        steps_label.config(anchor='nw')
        steps_label.pack(fill=tk.X)
        self.controller.set('steps', steps_stringvar)

        # Add recommended text field
        recommended_stringvar = tk.StringVar()
        recommended_label = tk.Label(self.sidebar, textvariable=recommended_stringvar, width=20)
        recommended = 'Forward'
        recommended_stringvar.set('Recommended: %s' % recommended)
        recommended_label.config(anchor='nw')
        recommended_label.pack(fill=tk.X)
        self.controller.set('recommended', recommended_stringvar)

        # Add run button
        go_button = tk.Button(master=self.sidebar, text='Run!', command=lambda: self.controller.run())
        go_button.pack(fill=tk.X)

        # Pack the entire sidebar
        self.sidebar.pack(side=tk.LEFT, padx=15, pady=15, ipadx=15, ipady=15, fill=tk.BOTH, expand=1)

    def _init_plot(self):
        """
        Sets up the MatPlotLib frame
        """

        self.fig, self.ax1 = plt.subplots()
        self.ax2 = self.ax1.twinx()
        self.plot = FigureCanvasTkAgg(self.fig, master=self)
        self.plot.get_tk_widget().config(width=500, height=400)
        self.plot.get_tk_widget().pack(side=tk.RIGHT)
        self.controller.set('plot', self.plot)
        plt.subplots_adjust(right=0.85)

    def _init_event_listeners(self):
        """
        Binds event listeners to the arrow keys
        """

        self.master.bind('<Up>', self.controller.handle_arrow_up)
        self.master.bind('<Left>', self.controller.handle_arrow_left)
        self.master.bind('<Right>', self.controller.handle_arrow_right)
