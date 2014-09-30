# -*- coding: utf-8 -*-

def aStar(graph, current, end):
    """
    the A* algorithm. Takes in a graph, current position and destination
    """
    openList = []
    closedList = []
    path = []

    def retracepath(c):
        path.insert(0,c)
        if c.parent is None:
            return
        retracepath(c.parent)

    openList.append(current)
    while len(openList) is not 0:
        current = min(openList, key=lambda inst: inst.h)
        if current == end:
            return retracepath(current)
        openList.remove(current)
        closedList.append(current)
        for tile in graph[current]:
            if tile not in closedList:
                tile.h = (abs(end.x-tile.x)+abs(end.y-tile.y))*10
                if tile not in openList:
                    openList.append(tile)
                tile.parent = current
    return path


def dfs(graph, start):
    """
    Depth-First-Search.

    :param graph: A graph/matrix of nodes
    :param start: The starting position
    :return: Reurns a set of nodes in the order they were visited
    """

    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    return visited


def dfs(graph, start, visited=None):
    """
    Breadth-First-Search

    :param graph: A graph/matrix of nodes
    :param start: The starting position
    :param visited: Recursive pass-through variable that tracks visited nodes
    :return: Resutns a set of nodes in the order they were visited
    """

    if visited is None:
        visited = set()
    visited.add(start)
    for next in graph[start] - visited:
        dfs(graph, next, visited)
    return visited
