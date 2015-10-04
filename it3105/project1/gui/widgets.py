# -*- coding: utf8 -*-
#
# Created by 'myth' on 8/26/15

from tkinter import *

from algorithms import ASTAR_OPTIONS, ASTAR_HEURISTIC, GAC_DEFAULT_K, GAC_DEFAULT_CONSTRAINT
from common import *


def generate_menus(window):
    """
    Takes in the window main menu bar and registers the submenus and
    their commands
    :param window: The main application window
    """

    # Define menu labels and their commands here
    menus = [
        (u'File', [
            (u'Exit', window.controller.exit)
        ]),
        (u'Boards', sorted([
            (os.path.basename(board),
             lambda fp=board: window.controller.load_board(file_path=fp))
            for board in fetch_files_from_dir(rootdir='module1/boards/')
        ])),
        (u'Graphs', sorted([
            (os.path.basename(board),
             lambda fp=board: window.controller.load_graph(file_path=fp))
            for board in fetch_files_from_dir(rootdir='module2/graphs/')
        ])),
        (u'Nonograms', sorted([
            (os.path.basename(board),
             lambda fp=board: window.controller.load_nonogram(file_path=fp))
            for board in fetch_files_from_dir(rootdir='module3/nonograms/')
        ])),
        (u'Run', [
            (u'GO!', window.controller.solve),
        ]),
    ]

    # Iterate over the main menu components and their actions
    for name, actions in menus:
        menu = Menu(window.menu, tearoff=0)
        window.menu.add_cascade(label=name, menu=menu)

        # Register commands
        for label, cmd in actions:
            menu.add_command(label=label, command=cmd)


def generate_options(frame, module=1):
    """
    Generates options for
    :param frame: Stats and options frame reference
    """

    # Clear all widgets for consistency
    for child_widget in frame.winfo_children():
        child_widget.destroy()

    mode_label = Label(frame, text='Algorithm mode:')
    mode_label.grid(row=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')

    mode_var = StringVar(master=frame, value=ASTAR_OPTIONS[0], name='algorithm_mode')
    frame.master.controller.references['algorithm_mode'] = mode_var
    options = OptionMenu(frame, mode_var, *ASTAR_OPTIONS)
    options.grid(row=0, column=1, sticky='E')

    heuristic_label = Label(frame, text='Heuristic:')
    heuristic_label.grid(row=1, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')

    if module == 1:
        heuristic_var = StringVar(master=frame, value=ASTAR_HEURISTIC[0], name='heuristic')
        h_options = OptionMenu(frame, heuristic_var, *ASTAR_HEURISTIC)
    else:
        heuristic_var = StringVar(master=frame, value='minimum_domain_sum', name='heuristic')
        h_options = OptionMenu(frame, heuristic_var, 'minimum_domain_sum')
    frame.master.controller.references['heuristic'] = heuristic_var
    h_options.grid(row=1, column=1, sticky='E')

    if module == 1 or module == 3:
        update_interval_label = Label(frame, text='Update interval (ms):')
        update_interval_label.grid(row=2, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')

        update_interval = Entry(frame)
        update_interval.insert(0, str(GUI_UPDATE_INTERVAL))
        update_interval.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky='E')
        frame.master.controller.references['update_interval'] = update_interval

    elif module == 2:
        k_value_label = Label(frame, text='K value:')
        k_value_label.grid(row=3, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')
        k_value = Entry(frame)
        k_value.insert(0, str(GAC_DEFAULT_K))
        k_value.grid(row=3, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky='E')
        frame.master.controller.references['k_value'] = k_value

        constraint_formula_label = Label(frame, text='Constraint formula:')
        constraint_formula_label.grid(row=4, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')

        constraint_formula = Entry(frame)
        constraint_formula.insert(0, GAC_DEFAULT_CONSTRAINT)
        constraint_formula.grid(row=4, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky='E')
        frame.master.controller.references['constraint_formula'] = constraint_formula


def generate_stats(frame, module=1):
    """
    Generates and fills the Statistics LabelFrame
    """

    # Clear all widgets for consistency
    for child_widget in frame.winfo_children():
        child_widget.destroy()

    path_length = StringVar(frame)
    path_length.set('Path length: 0')
    path_length_label = Label(frame, textvariable=path_length)
    frame.master.controller.references['path_length'] = path_length
    path_length_label.grid(row=0, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')

    open_set_size = StringVar(frame)
    open_set_size.set('OpenSet size: 0')
    open_set_size_label = Label(frame, textvariable=open_set_size)
    frame.master.controller.references['open_set_size'] = open_set_size
    open_set_size_label.grid(row=1, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')

    closed_set_size = StringVar(frame)
    closed_set_size.set('ClosedSet size: 0')
    closed_set_size_label = Label(frame, textvariable=closed_set_size)
    frame.master.controller.references['closed_set_size'] = closed_set_size
    closed_set_size_label.grid(row=2, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')

    total_set_size = StringVar(frame)
    total_set_size.set('Total set size: 0')
    total_set_size_label = Label(frame, textvariable=total_set_size)
    frame.master.controller.references['total_set_size'] = total_set_size
    total_set_size_label.grid(row=3, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')

    if module == 2:
        total_unsatisfied_constraints = StringVar(frame)
        total_unsatisfied_constraints.set('Unsatisfied constraints: 0')
        total_unsatisfied_constraints_label = Label(frame, textvariable=total_unsatisfied_constraints)
        frame.master.controller.references['total_unsatisfied_constraints'] = total_unsatisfied_constraints
        total_unsatisfied_constraints_label.grid(row=4, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')

        total_missing_assignment = StringVar(frame)
        total_missing_assignment.set('Vertices missing assignment: 0')
        total_missing_assignment_label = Label(frame, textvariable=total_missing_assignment)
        frame.master.controller.references['total_missing_assignment'] = total_missing_assignment
        total_missing_assignment_label.grid(row=5, padx=5, pady=5, ipadx=5, ipady=5, sticky='W')
