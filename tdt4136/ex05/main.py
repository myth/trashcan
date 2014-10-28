# -*- encoding: utf-8 -*-

import logging
import time
from tools import *

from datastructures import *
e = create_sudoku_csp("sudokus/evil.txt")
print_sudoku_solution(e.backtracking_search())
