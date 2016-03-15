# -*- coding: utf8 -*-
#
# Created by 'myth' on 3/14/16

import random

import numpy as np
import settings

PLAYER = 42
FOOD = 10
POISON = 1
EMPTY = 0
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]


class FlatLand(object):
    """
    Representation of a FlatLand instance
    """

    def __init__(self, preset=None):
        """
        Construct a FlatLand instance
        """

        self.x, self.y = settings.AGENT_START_LOCATION
        if preset is not None:
            self.board = preset
        else:
            self.board = np.zeros((settings.FLATLAND_COLS, settings.FLATLAND_ROWS), dtype='int')
            self._init_board()
        self.original_num_food = self._get_num_food()
        self.original_num_poison = self._get_num_poison()
        self.num_food = self.original_num_food
        self.num_poison = self.original_num_poison

    def move(self, direction):
        """
        Perform a move in the given direction
        :param direction: An (x, y) direction tuple
        :return: The value of the cell at position self.x, self.y + direction
        """

        self.set(self.x, self.y, EMPTY)
        x, y = self._correct_out_of_bounds(direction)
        item = self.get(x, y)
        self.set(x, y)
        self.x = x
        self.y = y

        # Update board statistics
        if item == FOOD:
            self.num_food -= 1
        elif item == POISON:
            self.num_poison -= 1

        return item

    def peek(self, direction):
        """
        Peek at the value in the given direction
        :param direction: An (x, y) direction tuple
        :return: The value at position self.x, self.y + direction
        """
        x, y = self._correct_out_of_bounds(direction)
        item = self.get(x, y)

        return item

    def get(self, x, y):
        """
        Get the value of the cell at coordinate x, y
        :param x: X coordinate
        :param y: Y coordinate
        :return: The value of cell (x, y)
        """
        return self.board[y][x]

    def set(self, x, y, val=PLAYER):
        """
        Set the value of cell (x, y) to val
        :param x: X coordinate
        :param y: Y coordinate
        :param val: The new value for the cell
        """
        self.board[y][x] = val

    def _get_num_food(self):
        """
        Count the number of food objects left on the board
        :return: The amount of food on the board
        """
        return sum(len(list(filter(lambda x: x == FOOD, row))) for row in self.board)

    def _get_num_poison(self):
        """
        Count the number of poison objects left on the board
        :return: The amount of poison on the board
        """
        return sum(len(list(filter(lambda x: x == POISON, row))) for row in self.board)

    def _init_board(self):
        """
        Initialize the board with the player, food and poison
        """

        self.board[self.y][self.x] = PLAYER

        for y in range(settings.FLATLAND_ROWS):
            for x in range(settings.FLATLAND_COLS):
                if self.board[y][x] != EMPTY:
                    continue
                if random.random() < settings.FOOD_PROBABILITY:
                    self.board[y][x] = FOOD

        for y in range(settings.FLATLAND_ROWS):
            for x in range(settings.FLATLAND_COLS):
                if self.board[y][x] != EMPTY:
                    continue
                if random.random() < settings.POISON_PROBABILITY:
                    self.board[y][x] = POISON

    def _correct_out_of_bounds(self, move):
        """
        Given a move, rectify out of bounds violations, and return the corrected coordinate tuple
        """

        x, y = move
        x += self.x
        y += self.y
        if x >= settings.FLATLAND_COLS:
            x -= settings.FLATLAND_COLS
        elif x < 0:
            x += settings.FLATLAND_COLS
        if y >= settings.FLATLAND_ROWS:
            y -= settings.FLATLAND_ROWS
        elif y < 0:
            y += settings.FLATLAND_ROWS

        return x, y


class Agent(object):
    """
    A FlatLand agent is an agent that operates in the FlatLand environment, with
    """

    def __init__(self, flatland=None):
        if flatland is None:
            flatland = FlatLand()
        self.flatland = flatland
        self.fitness = 0
        self.stats = {
            FOOD: 0,
            POISON: 0
        }
        self._dir_index = 0

    @property
    def direction(self):
        """
        Get the current direction
        :return: An (x, y) direction tuple
        """

        return DIRECTIONS[self._dir_index]

    def forward(self):
        """
        Perform a move in the current direction
        :return: The value of the cell that was currently moved to
        """

        item = self.flatland.move(self.direction)
        self._update_fitness(item)

        return item

    def left(self):
        """
        Perform a rotation to the left and move forward
        :return: The value of the cell that was currently moved to
        """

        self._dir_index = self._rotate(-1)
        item = self.flatland.move(self.direction)
        self._update_fitness(item)

        return item

    def right(self):
        """
        Perform a rotation to the right and move forward
        :return: The value of the cell that was currently moved to
        """
        self._dir_index = self._rotate(1)
        item = self.flatland.move(self.direction)
        self._update_fitness(item)

        return item

    def sense(self):
        """
        Perform a peek operation at the current direction, to the left of current and right of current
        :return: A list of length 6 that contains the truth value of food in each of the 3 directions,
        followed by the truth value of poison in each of the 3 directions.
        """

        forward = self.flatland.peek(self.direction)
        left = self.flatland.peek(LEFT)
        right = self.flatland.peek(RIGHT)

        ay = [
            float(forward == FOOD),
            float(left == FOOD),
            float(right == FOOD),
            float(forward == POISON),
            float(left == POISON),
            float(right == POISON)
        ]

        return ay

    def reset(self):
        """
        Reset the state of this Agent, and spawn a new random FlatLand instance
        """

        self.flatland = FlatLand()
        self.stats = {
            FOOD: 0,
            POISON: 0
        }
        self.fitness = 0
        self._dir_index = 0

    def _rotate(self, i):
        """
        Get the direction index of a direction of a rotation to the left (-1) or right (1)
        :param i: The rotation value
        :return: A direction index pointing to the correct direction in the DIRECTION list
        """

        i += self._dir_index
        if i > 3:
            return 0
        if i < 0:
            return 3
        return i

    def _update_fitness(self, item):
        """
        Update the stats and fitness of this agent
        :param item: The item that was consumed (cell value from board)
        """
        
        if item in (FOOD, POISON):
            self.stats[item] += 1
            self.fitness = self.stats[FOOD] / self.flatland.original_num_food
            self.fitness /= self.stats[POISON] * settings.AGENT_POISON_PENALTY_FACTOR
