# -*- coding: utf8 -*-
#
# Created by 'myth' on 2/18/16

from logging import getLogger
from logging.config import dictConfig
from modules.evolution import EvolutionLoop
import settings
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


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

        run = []
        for res in results:
            gen = []
            avg_fit = []
            std_dev = []
            max_fit = []
            for r in res:
                g, a, s, m = r
                gen.append(g)
                avg_fit.append(a)
                std_dev.append(s)
                max_fit.append(m)
            run.append((gen, max_fit, avg_fit, std_dev))

        for gen, max_fit, avg_fit, std_dev in run:
            plt.plot(gen, max_fit, '-', color='g', label='MaxFit')
            plt.plot(gen, avg_fit, '--', color='b', label='Avg.Fit')
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), mode='expand', ncol=4, loc=3, borderaxespad=0.)
        plt.show()

    else:
        el = EvolutionLoop()
        results = el.start()

        gen = []
        avg_fit = []
        std_dev = []
        max_fit = []
        for r in results:
            g, a, s, m = r
            gen.append(g)
            avg_fit.append(a)
            std_dev.append(s)
            max_fit.append(m)

        fig, ax1 = plt.subplots()
        ax1.plot(gen, max_fit, '-', color='g', label='MaxFit')
        ax1.plot(gen, avg_fit, '--', color='b', label='Avg.Fit')
        ax1.set_xlabel('Generation', color='black')
        ax1.set_ylabel('Fitness', color='blue')
        for tl in ax1.get_yticklabels():
            tl.set_color('b')

        ax2 = ax1.twinx()
        ax2.plot(gen, std_dev, '--', color='r', label='Std.Dev')
        ax2.set_ylabel('Std.Dev', color='r')
        for tl in ax2.get_yticklabels():
            tl.set_color('r')

        ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), mode='expand', ncol=3, loc=3, borderaxespad=0.)
        plt.show()
