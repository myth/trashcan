# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/18/16

import os

from modules.nnet import ActivationFunction as ActFunc
from modules.operators import Phenotype
from modules.selection import *

# -----------------------------------
# NEURAL NET SETTINGS
# -----------------------------------

NETWORK_STRUCTURE = [6, 10, 3]
ACTIVATION_FUNCTIONS = [ActFunc.relu, ActFunc.softmax, ActFunc.softmax]
DEFAULT_TRAIN_TIMESTEPS = 60
WEIGHT_GRANULARITY = 32
FLATLAND_ROWS = 10
FLATLAND_COLS = 10
FLATLAND_SCENARIOS = 1
FLATLAND_DYNAMIC = True
FOOD_PROBABILITY = 0.33
POISON_PROBABILITY = 0.33
AGENT_START_LOCATION = (6, 8)
AGENT_POISON_PENALTY_FACTOR = 1.0
AGENT_UNREASONABLENESS = 0.1

# -----------------------------------
# EA SETTINGS
# -----------------------------------

# General parameters
ENABLE_LOGGING = True
MULTI_RUN = False
MULTI_RUN_TOTAL = 5

# Core EA parameters
MAX_GENERATIONS = 50
MAX_ADULT_POOL_SIZE = 10
MAX_CHILD_POOL_SIZE = 30
GENOME_LENGTH = sum(NETWORK_STRUCTURE)
GENOME_CROSSOVER_RATE = 0.1
GENOME_CROSSOVER_POINTS = 1
GENOME_MUTATION_RATE = 0.2
GENOME_MUTATION_INTENSITY = 1
GENOME_COMPONENT_MUTATION_RATE = 0.08

# Selection parameters
ADULT_SELECTION_CLASS = GenerationalMixing
PARENT_SELECTION_CLASS = TournamentSelection

# Selection class-specific parameters
TOURNAMENT_SELECTION_K = 5
TOURNAMENT_SELECTION_EPSILON = 0.3
BOLTZMANN_SCALING_FACTOR = 1.0

# Problem specific (phenotype / fitness) parameters
FITNESS_FUNCTION = Fitness.flatland_agent
PHENOTYPE_FUNCTION = Phenotype.nnet_weight_tensor
ONEMAX_TARGET_LENGTH = GENOME_LENGTH
ONEMAX_SOLUTION = '1' * ONEMAX_TARGET_LENGTH
LOLZ_PREFIX_Z = 30
SURPRISING_SEQUENCE_S = 9
SURPRISING_SEQUENCE_LOCAL = False
FLATLAND_GRANULARITY = 32


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
            'level': 'INFO',
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
