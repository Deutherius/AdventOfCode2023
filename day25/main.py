import time, os, sys
from collections import deque, Counter
from heapq import heapify, heappop, heappush
from functools import cache
from helpers import pad, bcolors as b
from copy import deepcopy
from math import lcm
import random

def solve(data_orig: str):
    connections = set()
    nodes = set()
    g = {}
    for line in data_orig:
        left, right = line.split(": ")
        right = right.split()
        for item in right:
            duo = [left, item]
            duo.sort()
            con = (duo[0], duo[1])
            if not con in connections:
                connections.add(con)
            
            g.setdefault(left, set()).add(item)
            g.setdefault(item, set()).add(left)
            nodes.add(item)
            nodes.add(left)
    
    nodeList = list(nodes)
    # monte carlo solution, verified with graphwiz
    ct = Counter(connections)
    
    for _ in range(100):
        r1 = 0
        r2 = 0
        while r1 == r2:
            r1 = random.randint(0, len(nodeList)-1)
            r2 = random.randint(0, len(nodeList)-1)
        #find path between them
        start = nodeList[r1]
        end = nodeList[r2]
        visited = set()
        queue = []
        heappush(queue, (0, start, [start]))
        while queue:
            c, name, thisPath = heappop(queue)
            if name == end:
                resPath = thisPath
                break

            if name in visited:
                continue
            visited.add(name)

            for nextNode in g[name]:
                newPath = thisPath.copy()
                newPath.append(nextNode)
                heappush(queue, (c+1, nextNode, newPath))

        for f, t in zip(resPath[:-1], resPath[1:]):
            duo = [f, t]
            duo.sort()
            con = (duo[0], duo[1])
            ct[con] += 1
    
    for con, _ in ct.most_common(3):
        connections.remove(con)
        g[con[0]].remove(con[1])
        g[con[1]].remove(con[0])
                    
    # figure out how many are in each cluster - pick a random point and floodfill
    nodes2 = set()
    start = nodes.pop()
    nodes2.add(start)
    queue = deque()
    queue.appendleft(start)
    while queue:
        n = queue.pop()
        
        for nn in g[n]:
            if nn in nodes:
                nodes.remove(nn)
                nodes2.add(nn)
                queue.appendleft(nn)


    return len(nodes)*len(nodes2)

# with open("inp_ex.txt", "r") as inp:
with open("inp.txt", "r") as inp:
    data_orig = inp.read().strip().splitlines()
repeats = 1
now = time.time()
for _ in range(0,repeats):
    if repeats > 1:
        _ = solve(data_orig=data_orig)
    else:
        print(solve(data_orig=data_orig))
then = time.time()
print("Elapsed time for part 1: " + str(float(then-now)/repeats) + " s average per run")
