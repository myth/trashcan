# -*- coding: utf8 -*-
#
# Created by 'myth' on 9/23/15

import time

from tkinter import messagebox

from algorithms import *
from datastructures import Graph
from gui.widgets import *
from gui.render import CanvasRenderer, GraphRenderer
from module1.navigation import *
from module2.vc import *
from module3.nonogram import *


class MainController(object):
    """
    Controller class controlling window components
    """

    def __init__(self):
        self.window = None
        self.references = {}
        self.timers = []
        self.graph = None

    def clear_timers(self):
        """
        Clears all registered timers from the event loop
        """

        for timer in self.timers:
            self.window.parent.after_cancel(timer)
        self.timers = []

    def clear_stats(self):
        """
        Resets stats counters frame
        """

        if 'algorithm_mode' in self.references:
            self.references['algorithm_mode'].set('best')
        if 'path_length' in self.references:
            self.references['path_length'].set('Path length: 0')
        if 'open_set_size' in self.references:
            self.references['open_set_size'].set('OpenSet size: 0')
        if 'closed_set_size' in self.references:
            self.references['closed_set_size'].set('ClosedSet size: 0')
        if 'total_set_size' in self.references:
            self.references['total_set_size'].set('Total set size: 0')
        if 'total_unsatisfied_constraints' in self.references:
            self.references['total_unsatisfied_constraints'].set('Unsatisfied constraints: 0')
        if 'total_missing_assignment' in self.references:
            self.references['total_missing_assignment'].set('Vertices missing assignment: 0')

    def set_window(self, window):
        """
        Sets a reference to the main tkinter window
        """

        self.window = window

    def load_board(self, **kwargs):
        """
        Loads a specific predefined board
        """

        if 'file_path' not in kwargs:
            messagebox.showerror(
                'Missing file path',
                'No file path was provided!'
            )

        if isinstance(self.window.renderer, GraphRenderer):
            self.window.renderer.destruct()
            renderer = CanvasRenderer(self.window.content_area)
            renderer.set_controller(self)
            self.window.set_renderer(renderer)

        # Update panel widgets
        generate_options(self.window.options_area)
        generate_stats(self.window.stats_area)

        self.window.renderer.clear()
        self.window.renderer.set_board(NavigationProblem(kwargs['file_path']))
        self.window.render(math_coords=True)

    def load_graph(self, **kwargs):
        """
        Loads a specific predefined board
        """

        if 'file_path' not in kwargs:
            messagebox.showerror(
                'Missing file path',
                'No file path was provided!'
            )

        if isinstance(self.window.renderer, CanvasRenderer):
            self.window.renderer.destruct()
            renderer = GraphRenderer(self.window.content_area)
            renderer.set_controller(self)
            self.window.set_renderer(renderer)

        # Update panel widgets
        generate_options(self.window.options_area, module=2)
        generate_stats(self.window.stats_area, module=2)

        self.window.renderer.clear()
        # Load the graph from file, and provide networkx graph instance for rendering
        Graph.read_graph_from_file(kwargs['file_path'], networkx_graph=self.window.renderer.graph)

        self.window.renderer.render_graph()

    def load_nonogram(self, **kwargs):
        if 'file_path' not in kwargs:
            messagebox.showerror(
                'Missing file path',
                'No file path was provided!'
            )

        if isinstance(self.window.renderer, GraphRenderer):
            self.window.renderer.destruct()
            renderer = CanvasRenderer(self.window.content_area)
            renderer.set_controller(self)
            self.window.set_renderer(renderer)

        # Update panel widgets
        generate_options(self.window.options_area, module=3)
        generate_stats(self.window.stats_area, module=3)

        t = time.time()
        self.window.renderer.clear()
        self.window.renderer.set_board(NonogramProblem(kwargs['file_path']))
        self.window.render(math_coords=False)
        initial_result = self.window.renderer.board.heuristic(self.window.renderer.board.initial_state)

        if initial_result == 0:
            messagebox.showinfo(
                'Complete!',
                'Found a solution during initial domain filtering loop in %f seconds...' % (time.time() - t)
            )
            log("Found solution for NonogramProblem after first domain filtering loop")
            print("Found solution for NonogramProblem after first domain filtering loop")
            self.solve()

    def solve(self, algorithm='astar'):
        """
        Solves the currently set board with the provided algorithm
        """

        if isinstance(self.window.renderer, CanvasRenderer):
            algorithm = 'astar'
        elif isinstance(self.window.renderer, GraphRenderer):
            algorithm = 'astar_gac'

        # Clear any active rendering timers
        self.clear_timers()

        if algorithm == 'astar':

            if self.window.renderer.board is None:
                messagebox.showerror(
                    'No board data',
                    'You have to load a board or graph before you can run'
                )
                return

            if 'heuristic' in self.references:
                self.window.renderer.board.mode = self.references['heuristic'].get()

            update_interval = GUI_UPDATE_INTERVAL
            if 'update_interval' in self.references:
                try:
                    update_interval = self.references['update_interval'].get()
                    update_interval = int(update_interval)
                except ValueError:
                    messagebox.showerror(
                        'Invalid update interval',
                        'Update interval must be in milliseconds'
                    )
                    return

            a = AStar(
                problem=self.window.renderer.board,
                mode=self.references['algorithm_mode'].get()
            )

            nonogram = None
            if isinstance(a.problem, NonogramProblem):
                nonogram = a.problem

            i = -1
            for step in a.agenda_loop():
                i += 1
                self.timers.append(
                    self.window.parent.after(
                        i * update_interval,
                        lambda path=step['path'],
                        o=len(step['open_set']),
                        c=len(step['closed_set']): self.window.renderer.render_path(
                            path,
                            math_coords=True,
                            open_set_size=o,
                            closed_set_size=c,
                            nonogram=nonogram
                        )
                    )
                )

        elif algorithm == 'astar_gac':

            g = self.window.renderer.graph
            n = g.nodes()
            e = [(x.index, y.index) for x, y in g.edges()]

            k = int(self.references['k_value'].get())
            n = {node.index: set([i for i in range(k)]) for node in n}

            cf = make_func(['x', 'y'], self.references['constraint_formula'].get())
            vc_problem = VCProblem(n, e, cf=cf)
            solver = AStar(problem=vc_problem)

            t = time.time()

            i = -1
            last_node = None
            for step in solver.agenda_loop():
                i += 1
                p = step['path']
                last_node = p[0]
                oss = len(step['open_set'])
                css = len(step['closed_set'])

                vma = sum(0 if len(y) - 1 == 0 else 1 for x, y in last_node.state.nodes.items())
                tuc = sum(1 if len(y) == 0 else 0 for x, y in last_node.state.nodes.items())
                self.references['total_missing_assignment'].set('Vertices missing assignment: %d' % vma)
                self.references['total_unsatisfied_constraints'].set('Unsatisfied constraints: %d' % tuc)

                self.window.renderer.render_path(
                    p=p,
                    open_set_size=oss,
                    closed_set_size=css
                )

                if time.time() - t > TIMEOUT_THRESHOLD:
                    messagebox.showerror(
                        'Timeout!',
                        'Took too much time: %d steps in %f seconds...' % (i, time.time() - t)
                    )
                    break

            if last_node.is_goal:
                messagebox.showinfo(
                    'Complete!',
                    'Found a solution in %f seconds...' % (time.time() - t)
                )
            else:
                messagebox.showerror(
                    'Complete!',
                    'No solution could be found'
                )

    def exit(self):
        """
        Destroys the window
        :return:
        """

        self.window.parent.quit()
