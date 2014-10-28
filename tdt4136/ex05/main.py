# -*- encoding: utf-8 -*-

import logging
import time
from tools import *

from datastructures import *
print 'Starting Easy'
start_time = time.time()
e = create_sudoku_csp("sudokus/easy.txt")
print_sudoku_solution(e.backtracking_search())
print 'Took %d seconds to run' % (time.time() - start_time)
print '\nStarting Medium'
start_time = time.time()
e = create_sudoku_csp("sudokus/medium.txt")
print_sudoku_solution(e.backtracking_search())
print 'Took %d seconds to run' % (time.time() - start_time)
print '\nStarting Hard'
start_time = time.time()
e = create_sudoku_csp("sudokus/hard.txt")
print_sudoku_solution(e.backtracking_search())
print 'Took %d seconds to run' % (time.time() - start_time)
print '\nStarting Very Hard'
start_time = time.time()
e = create_sudoku_csp("sudokus/veryhard.txt")
print_sudoku_solution(e.backtracking_search())
print 'Took %d seconds to run' % (time.time() - start_time)
print '\nStarting Evil'
start_time = time.time()
e = create_sudoku_csp("sudokus/evil.txt")
print_sudoku_solution(e.backtracking_search())
print 'Took %d seconds to run' % (time.time() - start_time)
