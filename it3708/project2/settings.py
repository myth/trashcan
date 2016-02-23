# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/18/16

from modules.fitness import Fitness
from modules.operators import Phenotype
from modules.selection import *
import os


# GENERAL PARAMATERS
ENABLE_LOGGING = True
MULTI_RUN = False
MULTI_RUN_TOTAL = 5
# CORE EA PARAMETERS
MAX_GENERATIONS = 200
INITIAL_POPULATION_SIZE = 20
MAX_POPULATION_SIZE = 20
GENOME_LENGTH = 40
GENOME_CROSSOVER_RATE = 0.85
GENOME_CROSSOVER_POINTS = 1
GENOME_MUTATION_RATE = 0.15
# SELECTION
ADULT_SELECTION_CLASS = FullGenerationalReplacement
PARENT_SELECTION_CLASS = TournamentSelection
# SELECTION CLASS SPECIFICS
OVER_PRODUCTION_FACTOR = 1.5
TOURNAMENT_SELECTION_K = 4
TOURNAMENT_SELECTION_EPSILON = 0.1

# PROBLEM SPECIFIC
FITNESS_FUNCTION = Fitness.one_max
PHENOTYPE_FUNCTION = Phenotype.bitstring_phenotype
ONEMAX_TARGET_LENGTH = GENOME_LENGTH
ONEMAX_SOLUTION = '1' * ONEMAX_TARGET_LENGTH


# Logging settings
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
