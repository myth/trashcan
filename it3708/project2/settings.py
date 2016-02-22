# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/18/16

from modules.fitness import Fitness
from modules.operators import Phenotype
from modules.selection import *
import os


# CORE EA PARAMATERS
MAX_GENERATIONS = 100
INITIAL_POPULATION_SIZE = 20
MAX_POPULATION_SIZE = 20
GENOME_LENGTH = 40
GENOME_CROSSOVER_RATE = 0.88
GENOME_CROSSOVER_POINTS = 2
GENOME_MUTATION_RATE = 0.09

# SELECTION
ADULT_SELECTION_CLASS = GenerationalMixing
PARENT_SELECTION_CLASS = TournamentSelection
# SELECTION SPECIFICS
ADULT_SELECTION_MU = 20
ADULT_SELECTION_LAMBDA = 20
TOURNAMENT_SELECTION_K = 4
TOURNAMENT_SELECTION_EPSILON = 0.05

# PROBLEM SPECIFIC
FITNESS_FUNCTION = Fitness.one_max
PHENOTYPE_FUNCTION = Phenotype.bitstring_phenotype
ONEMAX_TARGET_LENGTH = GENOME_LENGTH


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
