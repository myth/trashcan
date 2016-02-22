# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/18/16

from logging import getLogger
from logging.config import dictConfig
from modules.evolution import EvolutionLoop
import settings

if __name__ == '__main__':

    dictConfig(config=settings.LOG_CONFIG)
    log = getLogger('main')
    log.info('Starting EA')

    el = EvolutionLoop()
    el.start()
