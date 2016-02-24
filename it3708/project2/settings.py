# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/18/16

from modules.fitness import Fitness
from modules.operators import Phenotype
from modules.selection import *
import os

# -----------------------------------
# SETTINGS
# -----------------------------------

# General parameters
ENABLE_LOGGING = True
MULTI_RUN = False
MULTI_RUN_TOTAL = 5

# Core EA parameters
MAX_GENERATIONS = 500
MAX_ADULT_POOL_SIZE = 60
MAX_CHILD_POOL_SIZE = 90
GENOME_LENGTH = 100
GENOME_CROSSOVER_RATE = 0.9
GENOME_CROSSOVER_POINTS = 3
GENOME_MUTATION_RATE = 0.2
GENOME_COMPONENT_MUTATION_RATE = 0.15

# Selection parameters
ADULT_SELECTION_CLASS = GenerationalMixing
PARENT_SELECTION_CLASS = TournamentSelection

# Selection class-specific parameters
TOURNAMENT_SELECTION_K = 3
TOURNAMENT_SELECTION_EPSILON = 0.25
BOLTZMANN_SCALING_FACTOR = 1.0

# Problem specific (phenotype / fitness) parameters
FITNESS_FUNCTION = Fitness.lolz_prefix
PHENOTYPE_FUNCTION = Phenotype.bitstring_phenotype
ONEMAX_TARGET_LENGTH = GENOME_LENGTH
ONEMAX_SOLUTION = '1' * ONEMAX_TARGET_LENGTH
LOLZ_PREFIX_Z = 50
SURPRISING_SEQUENCE_S = 10


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
