# -*- coding: utf8 -*-
#
# Created by 'myth' on 3/15/16

import unittest
from copy import deepcopy

import numpy as np
from modules.flatland import (DOWN, EMPTY, FOOD, LEFT, PLAYER, POISON, RIGHT,
                              UP, Agent, FlatLand)
from modules.nnet import ActivationFunction, Layer, NeuralNetwork
from settings import (ACTIVATION_FUNCTIONS, AGENT_START_LOCATION,
                      FLATLAND_COLS, FLATLAND_ROWS, NETWORK_STRUCTURE)

# FlatLand
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

# NeuralNetwork
WEIGHTS = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])


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
        b = Agent(fl)
        self.assertTrue(a.flatland is not b.flatland)
        self.assertTrue(b.flatland is fl)
        self.assertEqual(self.agent.stats[FOOD], 0)
        self.assertEqual(self.agent.stats[POISON], 0)
        self.assertEqual(self.agent.fitness, 0)

    def testRotate(self):
        self.agent._dir_index = 0
        self.assertEqual(self.agent._rotate(-1), 3)
        self.assertEqual(self.agent._rotate(1), 1)
        self.assertEqual(self.agent._rotate(4), 0)
        self.assertEqual(self.agent._rotate(-4), 0)
        self.assertEqual(self.agent._rotate(5), 1)
        self.assertEqual(self.agent._rotate(-5), 3)

    def testDirection(self):
        self.assertEqual(self.agent.direction, UP)
        self.agent.forward()
        self.assertEqual(self.agent.direction, UP)
        self.agent.right()
        self.assertEqual(self.agent.direction, RIGHT)
        self.agent.right()
        self.assertEqual(self.agent.direction, DOWN)
        self.agent.left()
        self.assertEqual(self.agent.direction, RIGHT)
        self.agent.forward()

    def testPosition(self):
        fl = (self.agent.flatland.x, self.agent.flatland.y)
        a = self.agent.position

        self.assertEqual(fl, a)
        self.agent.flatland.x = 3
        self.agent.flatland.y = 2

        fl = (self.agent.flatland.x, self.agent.flatland.y)
        a = self.agent.position

        self.assertEqual(fl, a)

    def testForward(self):
        print(self.agent.flatland.board)

        direction = self.agent.direction
        self.agent.forward()
        self.assertEqual(self.agent.flatland.get(*self.agent.position), PLAYER)
        self.assertEqual(self.agent.direction, direction)

        x, y = self.agent.position
        ox, oy = AGENT_START_LOCATION
        mx, my = direction
        self.assertEqual((x, y), (ox + mx, oy + my))

        print(self.agent.flatland.board)

        self.agent._dir_index = 1

        x, y = self.agent.position
        ox, oy = AGENT_START_LOCATION
        mx, my = direction
        self.assertEqual((x, y), (ox + mx, oy + my))

        print(self.agent.flatland.board)

    def testLeft(self):
        print(self.agent.flatland.board)

        self.agent.left()
        self.assertEqual(self.agent.flatland.get(*self.agent.position), PLAYER)
        self.assertEqual(self.agent.direction, LEFT)

        x, y = self.agent.position
        ox, oy = AGENT_START_LOCATION
        mx, my = LEFT
        self.assertEqual((x, y), (ox + mx, oy + my))

        print(self.agent.flatland.board)

        self.agent.left()
        ox, oy = x, y
        x, y = self.agent.position
        mx, my = DOWN
        self.assertEqual((x, y), (ox + mx, oy + my))

        print(self.agent.flatland.board)

    def testRight(self):
        print(self.agent.flatland.board)

        self.agent.right()
        self.assertEqual(self.agent.flatland.get(*self.agent.position), PLAYER)
        self.assertEqual(self.agent.direction, RIGHT)

        x, y = self.agent.position
        ox, oy = AGENT_START_LOCATION
        mx, my = RIGHT
        self.assertEqual((x, y), (ox + mx, oy + my))

        print(self.agent.flatland.board)

        self.agent.right()
        ox, oy = x, y
        x, y = self.agent.position
        mx, my = DOWN
        self.assertEqual((x, y), (ox + mx, oy + my))

        print(self.agent.flatland.board)

    def testRun(self):
        nnet = NeuralNetwork()
        history = self.agent.run(nnet)
        self.assertEqual(self.agent.steps, 1)
        self.assertEqual(len(history), 1)

        self.agent = Agent()
        history = self.agent.run(nnet, timesteps=60)
        self.assertEqual(self.agent.steps, 60)
        self.assertEqual(len(history), 60)
        for h in history:
            self.assertTrue(h in [self.agent.forward, self.agent.left, self.agent.right])

    def testSense(self):
        print(self.agent.flatland.board)
        sensed = self.agent.sense()
        expected = [0, 0, 0, 1, 1, 0]

        self.assertEqual(expected, sensed)

        self.agent.right()
        print(self.agent.flatland.board)

        sensed = self.agent.sense()
        expected = [0, 1, 1, 1, 0, 0]

        self.assertEqual(expected, sensed)

        # Reset back to direction UP, move to top-left corner
        self.agent._dir_index = 0
        self.agent.flatland.x = 0
        self.agent.flatland.y = 0
        self.agent.flatland.set(0, 0)

        sensed = self.agent.sense()
        expected = [0, 1, 0, 0, 0, 0]

        self.assertEqual(expected, sensed)

        # Move to bottom-right corner
        self.agent.flatland.x = FLATLAND_COLS - 1
        self.agent.flatland.y = FLATLAND_ROWS - 1
        self.agent.flatland.set(0, 0)

        sensed = self.agent.sense()
        expected = [1, 1, 0, 0, 0, 0]

        self.assertEqual(expected, sensed)

    def testUpdateFitness(self):
        print(self.agent.flatland.board)
        self.agent.forward()

        expected = 1 / 31
        expected /= 2

        self.assertEqual(self.agent.fitness, expected)
        self.assertEqual(self.agent.stats[POISON], 1)
        self.assertEqual(self.agent.stats[FOOD], 0)

        self.agent.right()

        expected = 2 / 31
        expected /= 2
        self.assertEqual(self.agent.stats[POISON], 1)
        self.assertEqual(self.agent.stats[FOOD], 1)

        self.assertEqual(self.agent.fitness, expected)

        self.agent.left()

        expected = 2 / 31
        expected /= 3
        self.assertEqual(self.agent.stats[POISON], 2)
        self.assertEqual(self.agent.stats[FOOD], 1)

        self.assertEqual(self.agent.fitness, expected)

    def testReset(self):
        self.agent.forward()
        self.agent.forward()
        self.assertNotEqual(self.agent.steps, 0)
        self.agent.reset()
        self.assertEqual(self.agent.steps, 0)
        self.assertEqual(self.agent.stats[FOOD], 0)
        self.assertEqual(self.agent.stats[POISON], 0)
        self.assertEqual(self.agent.direction, (0, -1))


class LayerTest(unittest.TestCase):

    def setUp(self):
        self.layer = Layer(10, weights=WEIGHTS)

    def testFire(self):
        inputs = [1, 0, 0, 1, 0, 0]
        print(self.layer.tensor)
        self.layer.fire(inputs)
        print(self.layer.tensor)

        # Check 4 decimal places
        for x, y in zip(self.layer.tensor, [.3333] * 10):
            self.assertAlmostEqual(x, y, 4)

        self.layer.weights = np.array([-0.5] * 10, dtype='float')
        self.layer.fire(inputs)

        self.assertEqual(list(self.layer.tensor), [0] * 10)


class NeuralNetworkTest(unittest.TestCase):

    def setUp(self):
        self.agent = Agent(FlatLand(preset=deepcopy(BOARD)))
        self.nn = NeuralNetwork()

    def testInit(self):
        self.assertEqual(len(self.nn._net), len(NETWORK_STRUCTURE))

        for layer, size in zip(self.nn._net, NETWORK_STRUCTURE):
            self.assertEqual(len(layer.tensor), size)

        for layer, af in zip(self.nn._net, ACTIVATION_FUNCTIONS):
            if af is ActivationFunction.softmax:
                self.assertEqual(layer.af, af)
            else:
                self.assertEqual(
                    list(layer.af([.1, .1351, .62642, .2496829])),
                    list(np.vectorize(af)([.1, .1351, .62642, .2496829]))
                )

        net = [2, 4, 2]
        afs = [ActivationFunction.relu, ActivationFunction.relu, ActivationFunction.softmax]

        self.nn = NeuralNetwork(net=net, afs=afs)

        for layer, size in zip(self.nn._net, net):
            self.assertEqual(len(layer.tensor), size)

        for layer, af in zip(self.nn._net, afs):
            if af is ActivationFunction.softmax:
                self.assertEqual(layer.af, af)
            else:
                self.assertEqual(
                    list(layer.af([.1, .1351, .62642, .2496829])),
                    list(np.vectorize(af)([.1, .1351, .62642, .2496829]))
                )

    def testTest(self):
        net = [2, 3, 2]
        afs = [ActivationFunction.relu, ActivationFunction.relu, ActivationFunction.softmax]

        self.nn = NeuralNetwork(net=net, afs=afs)

        results = self.nn.test([1, 1, 0, 0, 1, 0])
        print(results)
        for a, b in zip(results, self.nn._output):
            self.assertEqual(a, b)

    def testSetWeights(self):
        net = [2, 2, 2]
        afs = [ActivationFunction.relu, ActivationFunction.relu, ActivationFunction.softmax]
        weights = [
            np.array([0.5, -0.5]),
            np.array([0.1, -0.3]),
            np.array([-0.2, 0.8])
        ]

        self.nn = NeuralNetwork(net=net, afs=afs)

        self.nn.set_weights(weights)

        for layer, expected in zip(self.nn._net, weights):
            self.assertTrue(layer.weights is expected)
