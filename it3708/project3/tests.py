# -*- coding: utf8 -*-
#
# Created by 'myth' on 3/15/16

import unittest
from copy import deepcopy

import numpy as np
from modules.flatland import (DOWN, EMPTY, FOOD, LEFT, PLAYER, POISON, RIGHT,
                              UP, Agent, FlatLand)
from settings import AGENT_START_LOCATION, FLATLAND_COLS, FLATLAND_ROWS

BOARD = np.array([
    [1,  0, 10, 10,  0,  0,  1, 10,  0, 10],
    [0,  1, 10,  0,  0,  0, 10,  0,  0, 10],
    [0,  0, 10,  0,  0,  0, 10,  1,  1, 10],
    [0,  1,  1,  0,  1,  1,  0,  0,  0,  0],
    [0, 10, 10, 10,  0, 10, 10, 10,  0,  0],
    [0,  1,  0, 10,  0,  0,  0,  0,  1,  1],
    [0, 10,  0, 10, 10, 10,  1,  1,  1,  0],
    [0, 10,  0,  0,  0,  0,  1, 10,  0, 10],
    [10,  0,  0,  0,  0,  1, 42,  0,  1, 10],
    [0,  0, 10,  1,  0,  0, 10, 10, 10,  0]
])


class FlatLandTest(unittest.TestCase):

    def setUp(self):
        self.flatland = FlatLand(preset=deepcopy(BOARD))

    def testBoardPreset(self):
        for y in range(FLATLAND_ROWS):
            for x in range(FLATLAND_COLS):
                with self.subTest(y=y, x=x):
                    fixture = BOARD[y][x]
                    fl = self.flatland.board[y][x]
                    self.assertEqual(fixture, fl)

    def testGet(self):
        for y in range(FLATLAND_ROWS):
            for x in range(FLATLAND_COLS):
                with self.subTest(y=y, x=x):
                    fixture = BOARD[y][x]
                    fl = self.flatland.get(x, y)
                    self.assertEqual(fixture, fl)

    def testCorrectOutOfBounds(self):
        self.flatland.x = FLATLAND_COLS - 1
        self.flatland.y = FLATLAND_ROWS - 1
        x, y = self.flatland._correct_out_of_bounds(RIGHT)
        self.assertEqual(x, 0)
        self.assertEqual(y, FLATLAND_ROWS - 1)

        self.flatland.x = FLATLAND_COLS - 1
        self.flatland.y = FLATLAND_ROWS - 1
        x, y = self.flatland._correct_out_of_bounds(DOWN)
        self.assertEqual(x, FLATLAND_COLS - 1)
        self.assertEqual(y, 0)

        self.flatland.x = 0
        self.flatland.y = 0
        x, y = self.flatland._correct_out_of_bounds(UP)
        self.assertEqual(x, 0)
        self.assertEqual(y, FLATLAND_ROWS - 1)

        self.flatland.x = 0
        self.flatland.y = 0
        x, y = self.flatland._correct_out_of_bounds(LEFT)
        self.assertEqual(x, FLATLAND_COLS - 1)
        self.assertEqual(y, 0)

        self.flatland.x = 5
        self.flatland.y = 5
        x, y = self.flatland._correct_out_of_bounds(LEFT)
        self.assertEqual(x, 4)
        self.assertEqual(y, 5)
        x, y = self.flatland._correct_out_of_bounds(RIGHT)
        self.assertEqual(x, 6)
        self.assertEqual(y, 5)
        x, y = self.flatland._correct_out_of_bounds(UP)
        self.assertEqual(x, 5)
        self.assertEqual(y, 4)
        x, y = self.flatland._correct_out_of_bounds(DOWN)
        self.assertEqual(x, 5)
        self.assertEqual(y, 6)

    def testSet(self):
        self.assertEqual(self.flatland.board[0][0], POISON)
        self.flatland.set(0, 0, EMPTY)
        self.assertEqual(self.flatland.board[0][0], EMPTY)
        self.flatland.set(2, 2, FOOD)
        self.assertEqual(self.flatland.board[2][2], FOOD)

    def testPlayerInit(self):
        x, y = AGENT_START_LOCATION
        self.assertEqual(self.flatland.x, x)
        self.assertEqual(self.flatland.y, y)
        self.assertEqual(self.flatland.board[y][x], PLAYER)

    def testPeekLeft(self):
        val = self.flatland.peek(LEFT)
        self.assertEqual(val, POISON)

    def testPeekRight(self):
        val = self.flatland.peek(RIGHT)
        self.assertEqual(val, EMPTY)

    def testPeekUp(self):
        val = self.flatland.peek(UP)
        self.assertEqual(val, POISON)

    def testPeekDown(self):
        val = self.flatland.peek(DOWN)
        self.assertEqual(val, FOOD)

    def testMoveLeft(self):
        val = self.flatland.move(LEFT)
        self.assertEqual(val, POISON)
        x, y = (self.flatland.x, self.flatland.y)
        self.assertEqual(self.flatland.get(x, y), PLAYER)
        self.assertEqual(self.flatland.get(x + 1, y), 0)

    def testMoveRight(self):
        val = self.flatland.move(RIGHT)
        self.assertEqual(val, EMPTY)
        x, y = (self.flatland.x, self.flatland.y)
        self.assertEqual(self.flatland.get(x, y), PLAYER)
        self.assertEqual(self.flatland.get(x - 1, y), 0)

    def testMoveUp(self):
        val = self.flatland.move(UP)
        self.assertEqual(val, POISON)
        x, y = (self.flatland.x, self.flatland.y)
        self.assertEqual(self.flatland.get(x, y), PLAYER)
        self.assertEqual(self.flatland.get(x, y + 1), 0)

    def testMoveDown(self):
        val = self.flatland.move(DOWN)
        self.assertEqual(val, FOOD)
        x, y = (self.flatland.x, self.flatland.y)
        self.assertEqual(self.flatland.get(x, y), PLAYER)
        self.assertEqual(self.flatland.get(x, y - 1), 0)

    def testNumFood(self):
        food = self.flatland.num_food
        self.assertEqual(food, 30)

    def testNumPoison(self):
        poison = self.flatland.num_poison
        self.assertEqual(poison, 19)

    def testOriginalNumFood(self):
        food = self.flatland.num_food
        self.assertEqual(food, 30)
        self.flatland.move(DOWN)
        self.assertEqual(self.flatland.num_food, 29)
        self.assertEqual(self.flatland.original_num_food, 30)

    def testOriginalNumPoison(self):
        poison = self.flatland.num_poison
        self.assertEqual(poison, 19)
        self.flatland.move(UP)
        self.assertEqual(self.flatland.num_poison, 18)
        self.assertEqual(self.flatland.original_num_poison, 19)


class AgentTest(unittest.TestCase):

    def setUp(self):
        self.agent = Agent(FlatLand(deepcopy(BOARD)))

    def testFlatLandReference(self):
        for y in range(FLATLAND_ROWS):
            for x in range(FLATLAND_COLS):
                with self.subTest(y=y, x=x):
                    fixture = BOARD[y][x]
                    fl = self.agent.flatland.board[y][x]
                    self.assertEqual(fixture, fl)

    def testInit(self):
        a = Agent()
        fl = FlatLand()
        a = Agent(fl)
        self.assertTrue(a.flatland is fl)
        self.assertEqual(self.agent.stats[FOOD], 0)
        self.assertEqual(self.agent.stats[POISON], 0)
        self.assertEqual(self.agent.fitness, 0)
