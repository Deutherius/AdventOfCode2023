import time, os
from collections import deque
from heapq import heapify, heappop, heappush
from functools import cache
from helpers import pad, bcolors as b
from copy import deepcopy
from math import lcm

def solve2(data_orig: str):
    maze = pad(data_orig, "#")
    #delete slopes
    newMaze = []
    for line in maze:
        newMaze.append(line.replace("v", ".").replace("^", ".").replace("<", ".").replace(">", "."))
    maze = newMaze
    start = (1, 2)
    end = (len(maze)-2, len(maze[0])-3)   

    junctions = set()
    visited = set()
    queue = deque()

    #simple BFS floodfill to find all the paths
    queue.appendleft(start)
    while queue:
        y, x = queue.pop()
        
        if (y, x) in visited:
            continue
        visited.add((y,x))

        paths = 0
        if maze[y-1][x] == ".":
            paths += 1
            queue.appendleft((y-1,x))
        if maze[y+1][x] == ".":
            paths += 1
            queue.appendleft((y+1,x))
        if maze[y][x-1] == ".":
            paths += 1
            queue.appendleft((y,x-1))
        if maze[y][x+1] == ".":
            paths += 1
            queue.appendleft((y,x+1))
        if paths > 2:
            junctions.add((y,x))
        
    #for each junction, BFS all ways to find pathways between junctions (and start and end)
    junctions.add(start)
    junctions.add(end)
    js = {} #tuple(y,x): [tuple(y,x)]
    for junction in junctions:
        queue.appendleft((junction, 0))
        visited = set()
        while queue:
            (y, x), s = queue.pop()
            
            if (y, x) in visited:
                continue
            visited.add((y,x))

            if (y, x) in junctions and not (y, x) == junction:
                js.setdefault(junction, []).append(((y,x),s))
                continue
            
            if maze[y-1][x] == ".":
                queue.appendleft(((y-1,x), s+1))
            if maze[y+1][x] == ".":
                queue.appendleft(((y+1,x), s+1))
            if maze[y][x-1] == ".":
                queue.appendleft(((y,x-1), s+1))
            if maze[y][x+1] == ".":
                queue.appendleft(((y,x+1), s+1))

    end, endAddSteps = js[end][0][0], js[end][0][1] #only one junction connects to the end, so it becomes the new end

    state = [0, set([start]), start]
    queue.appendleft(state)
    results = []
    visited = {start: 0}
    while queue:
        state = queue.pop()
        pathSoFar = state[1]
        (y, x) = state[2]

        if (y, x) == end:
            results.append(state)
            continue
        
        for nextJunction in js[(y,x)]:
            nJname, nJsteps = nextJunction
            if not nJname in pathSoFar: #not visited before
                newState = deepcopy(state)
                newState[0] += nJsteps
                newState[1].add(nJname)
                newState[2] = nJname
                queue.appendleft(newState)
        
    results.sort(key=lambda x: x[0])

    return results[-1][0] + endAddSteps

def solve(data_orig: str):
    maze = pad(data_orig, "#")
    start = (1, 2)
    end = (len(maze)-2, len(maze[0])-3)    
    #BFS
    queue = deque()
    state = [0, deque([start])]
    queue.appendleft(state)

    results = []

    while queue:
        state = queue.pop()
        (y, x), lastTile = state[1][0], maze[state[1][0][0]][state[1][0][1]]
        if (y, x) == end:
            results.append(state)
            continue
           #can walk there         and   we were not there yet and last tile did not force other moves
        if maze[y-1][x] in ".>^v<" and not (y-1,x) in state[1] and not lastTile in "v<>":
            newState = deepcopy(state)
            newState[1].appendleft((y-1,x))
            newState[0] += 1
            queue.appendleft(newState)
        if maze[y+1][x] in ".>^v<" and not (y+1,x) in state[1] and not lastTile in "^<>":
            newState = deepcopy(state)
            newState[1].appendleft((y+1,x))
            newState[0] += 1
            queue.appendleft(newState)
        if maze[y][x-1] in ".>^v<" and not (y,x-1) in state[1] and not lastTile in "^v>":
            newState = deepcopy(state)
            newState[1].appendleft((y,x-1))
            newState[0] += 1
            queue.appendleft(newState)
        if maze[y][x+1] in ".>^v<" and not (y,x+1) in state[1] and not lastTile in "^v<":
            newState = deepcopy(state)
            newState[1].appendleft((y,x+1))
            newState[0] += 1
            queue.appendleft(newState)
    return results[-1][0]


#WARNING - very inefficient. DFS with optimizations would have been a better algo to use

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

now = time.time()
for _ in range(0,repeats):
    if repeats > 1:
        _ = solve2(data_orig=data_orig)
    else:
        print(solve2(data_orig=data_orig))
then = time.time()
print("Elapsed time for part 2: " + str(float(then-now)/repeats) + " s average per run")
