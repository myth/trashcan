#!usr/bin/env python
__author__ = 'Fredrik'
import collections

#MAIN

map_file = open('board-1-1.txt', 'r')
the_map = map_file.read().split('\n')

# MAIN
directions = 4 # number of possible directions to move on the map
if directions == 4:
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]

# map matrix
board = []

for line in the_map:
    board.append(list(line))
    print(line)

row = board.__getitem__(3)
col = row.__getitem__(11)


print(start)
map_file.close()



# def main():
#     # dictionary to store board state
#     # cells contain one of ["black", "white", None]
#
#     board = {}
#     for i in range(1, 11, 1): board[i] = None
#     board[1] = "white"
#     board[6] = "white"
#     board[5] = "black"
#     board[7] = "black"
#     # dictionary defines valid operators (legal moves)
#     moves = { 1: [4, 7],
#               2: [8, 10],
#               3: [9],
#               4: [1, 6, 10],
#               5: [7],
#               6: [4],
#               7: [1, 5],
#               8: [2, 9],
#               9: [8, 3],
#               10: [2, 4] }
#
#     ans, goal = aStarSearch(board, moves)
#     print (ans)

    # reconstruct path
    # if "-p" in sys.argv:
#          if ans == "We've got a winner.":
#             start = Node(board, 0)
#             path = getPath(goal, start)
#             i = 0
#             for node in path:
#                 print "step ", i, ":"
#                 showDiagram(node.contents)
#                 i += 1
#
# if __name__ == "__main__":
#     main()