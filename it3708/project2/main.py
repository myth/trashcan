# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/18/16

from logging import getLogger
from logging.config import dictConfig
from modules.evolution import EvolutionLoop
import settings


def multirun():
    res = []
    if settings.MULTI_RUN:
        for i in range(settings.MULTI_RUN_TOTAL):
            evo_loop = EvolutionLoop()
            res.append(evo_loop.start())

    return res

if __name__ == '__main__':

    dictConfig(config=settings.LOG_CONFIG)
    log = getLogger('main')
    log.info('Starting EA')

    if settings.MULTI_RUN:
        results = multirun()
        log.info('Multi-run complete: %s' % results)
    else:
        el = EvolutionLoop()
        el.start()
