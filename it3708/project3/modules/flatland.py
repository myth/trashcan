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
        self.original_num_food = self.num_food
        self.original_num_poison = self.num_poison

    def move(self, direction):
        self.set(self.x, self.y, EMPTY)
        x, y = self._correct_out_of_bounds(direction)
        item = self.get(x, y)
        self.set(x, y)
        self.x = x
        self.y = y

        return item

    def peek(self, direction):
        x, y = self._correct_out_of_bounds(direction)
        item = self.get(x, y)

        return item

    def get(self, x, y):
        return self.board[y][x]

    def set(self, x, y, val=PLAYER):
        self.board[y][x] = val

    @property
    def num_food(self):
        return sum(len(list(filter(lambda x: x == FOOD, row))) for row in self.board)

    @property
    def num_poison(self):
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
        return DIRECTIONS[self._dir_index]

    def forward(self):
        item = self.flatland.move(self.direction)
        self._update_fitness(item)

        return item

    def left(self):
        self._dir_index = self._rotate(-1)
        item = self.flatland.move(self.direction)
        self._update_fitness(item)

        return item

    def right(self):
        self._dir_index = self._rotate(1)
        item = self.flatland.move(self.direction)
        self._update_fitness(item)

        return item

    def sense(self):
        forward = self.flatland.peek(UP)
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
        self.flatland = FlatLand()
        self.stats = {
            FOOD: 0,
            POISON: 0
        }
        self.fitness = 0
        self._dir_index = 0

    def _make_move(self, direction):
            if direction == UP:
                self.forward()
            elif direction == LEFT:
                self.left()
            else:
                self.right()

    @staticmethod
    def _rotate(i):
        if i > 3:
            return 0
        if i < 0:
            return 3
        return i

    def _update_fitness(self, item):
        if item in (FOOD, POISON):
            self.stats[item] += 1
            self.fitness = self.stats[FOOD] / self.flatland.original_num_food
            self.fitness /= self.stats[POISON] * settings.AGENT_POISON_PENALTY_FACTOR
