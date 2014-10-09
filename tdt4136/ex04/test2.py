# -*- encoding: utf-8 -*-

a = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
]

def printmatrix(m):
    for line in m:
        print line

printmatrix(a)

n = len(a)

diags = {}

for y in xrange(n):
    for x in xrange(n):
        print x,y

print diags
