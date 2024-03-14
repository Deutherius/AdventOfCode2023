import time, os
from collections import deque
from heapq import heapify, heappop, heappush
from functools import cache
from helpers import pad, bcolors as b, repmat
from copy import deepcopy
from math import lcm

seen = set()

def make_step(data, position, stepsRemaining, finalPositions):
    if (position, stepsRemaining) in seen:
        return
    seen.add((position, stepsRemaining))
    if stepsRemaining:
        stepsRemaining -= 1
        #check each direction and if it's not a rock, travel there recursively
        y, x = position
        if data[y-1][x] == ".":
            make_step(data, (y-1, x), stepsRemaining, finalPositions)
        if data[y+1][x] == ".":
            make_step(data, (y+1, x), stepsRemaining, finalPositions)
        if data[y][x-1] == ".":
            make_step(data, (y, x-1), stepsRemaining, finalPositions)
        if data[y][x+1] == ".":
            make_step(data, (y, x+1), stepsRemaining, finalPositions)
    else:
        #final position, update set of possible positions
        finalPositions.add(position)
    return

def solve(data_orig: str, part2: bool=False):
    if part2:
        data = repmat(data_orig, (100, 100))
    finalPositions = set()
    data = pad(data_orig, "#", 1)
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if c == "S":
                startPos = (i,j)
                data[j] = data[j].replace("S", ".")
                break
        else:
            continue
        break
    data = tuple(a for a in data)
    stepsRemaining = 64
    make_step(data, startPos, stepsRemaining, finalPositions)
    return len(finalPositions)

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

# no part 2