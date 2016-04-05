# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/18/16

import os

from modules.nnet import ActivationFunction as ActFunc
from modules.operators import Phenotype
from modules.selection import *

# General parameters
ENABLE_LOGGING = True
VERBOSE_DEBUG = False
GUI_UPDATE_INTERVAL = 250


def reduce(iterable, i=0):
    """
    reduce was removed in python3, reintroducing
    :param iterable: An iterable of any kind
    :param i: Iterator variable
    """
    if i + 1 < len(iterable):
        item = iterable[i]
        return item * reduce(iterable, i=i+1)
    return iterable[i]

# -----------------------------------
# NEURAL NET SETTINGS
# -----------------------------------

NETWORK_STRUCTURE = [6, 3]
ACTIVATION_FUNCTIONS = [ActFunc.relu, ActFunc.softmax]
FLATLAND_TIMESTEPS = 60
WEIGHT_GRANULARITY = 48
FLATLAND_ROWS = 10
FLATLAND_COLS = 10
FLATLAND_SCENARIOS = 1
FLATLAND_DYNAMIC = False
FLATLANDS = []
FOOD_PROBABILITY = 0.33
POISON_PROBABILITY = 0.33
AGENT_START_LOCATION = (6, 8)
AGENT_POISON_PENALTY_FACTOR = 1.5

# -----------------------------------
# EA SETTINGS
# -----------------------------------

# Core EA parameters
MAX_GENERATIONS = 15
MAX_ADULT_POOL_SIZE = 20
MAX_CHILD_POOL_SIZE = 30
GENOME_LENGTH = reduce(NETWORK_STRUCTURE)
GENOME_CROSSOVER_RATE = 0.8
GENOME_CROSSOVER_POINTS = 1
GENOME_MUTATION_RATE = 0.7
GENOME_MUTATION_INTENSITY = 1
GENOME_COMPONENT_MUTATION_RATE = 0.15

# Selection parameters
ADULT_SELECTION_CLASS = GenerationalMixing
PARENT_SELECTION_CLASS = TournamentSelection
ELITISM_LEVEL = 2

# Selection class-specific parameters
TOURNAMENT_SELECTION_K = 3
TOURNAMENT_SELECTION_EPSILON = 0.2
BOLTZMANN_SCALING_FACTOR = 1.0

# Problem specific (phenotype / fitness) parameters
PHENOTYPE_FUNCTION = Phenotype.nnet_weight_tensor


# -----------------------------------
# LOGGING
# -----------------------------------
LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': os.path.join(os.path.dirname(__name__), 'debug.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 1,
        }
    },
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s %(name)s.%(funcName)s:%(lineno)d %(message)s'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
