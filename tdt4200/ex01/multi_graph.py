# -*- coding: utf-8 -*-

import os
import math

PROCESSES = [1, 2, 4, 8]
START = 2
STOP = [100, 1000000, 1000000000]

# Create file if it does not exist
with open('graph_run.sh', 'w') as results:
    for num_cores in PROCESSES:
        for n in STOP:
            for step in range(n // 20, n + n // 20, n // 20):
                results.write('parallel %d %d CORES: %d' % (START, step, num_cores))
                results.write('time -p -a -o results.log mpirun -np %d bin/parallel %d %d >> results.log\n' % (num_cores, START, step))

