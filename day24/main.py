import time, os
from collections import deque
from heapq import heapify, heappop, heappush
from functools import cache
from helpers import pad, bcolors as b
from copy import deepcopy
from math import lcm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def find_intersection_point(line1, line2):
    #extract points from the lines
    p1, p2 = np.array(line1[0]), np.array(line1[1])
    p3, p4 = np.array(line2[0]), np.array(line2[1])

    #vectors representing the lines (ignoring z-components)
    v1 = p2 - p1
    v2 = p4 - p3

    #cross product of direction vectors
    cross_product = np.cross(v1, v2)

    #check if lines are parallel (cross product magnitude is zero)
    if np.abs(cross_product) < 1e-10:
        return None  # Lines are parallel, no intersection

    #vector from the starting point of line1 to the intersection point
    w = p3 - p1

    #scalar parameters for the intersection point along each line
    s = np.cross(w, v2) / np.cross(v1, v2)

    #calculate the intersection point
    intersection_point = p1 + s * v1

    return intersection_point

def solve(data_orig: str):
    hailstorm = []
    for line in data_orig:
        px, py, pz, vx, vy, vz = map(int, line.replace(" @", ",").split(", "))
        hailstorm.append((px, py, pz, vx, vy, vz))

    TAMin = 200000000000000#7
    TAMax = 400000000000000#27
    hitCt = 0
    for i, h in enumerate(hailstorm):
        for j, h2 in enumerate(hailstorm):
            if i >= j:
                continue
            line1 = ((h[0], h[1]),(h[0]+h[3], h[1]+h[4]))
            line2 = ((h2[0], h2[1]),(h2[0]+h2[3], h2[1]+h2[4]))
            hit = find_intersection_point(line1, line2)
            hitArea = False    
            hitTime = True
            if hit is not None:
                if TAMin <= hit[0] <= TAMax and TAMin <= hit[1] <= TAMax:
                    hitArea = True
                if h[3] < 0:
                    if not hit[0] < h[0]:
                        hitTime = False
                elif h[3] > 0:
                    if not hit[0] > h[0]:
                        hitTime = False
                if h2[3] < 0:
                    if not hit[0] < h2[0]:
                        hitTime = False
                elif h2[3] > 0:
                    if not hit[0] > h2[0]:
                        hitTime = False
                if hitArea and hitTime:
                    hitCt += 1
    return hitCt

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

#did not solve part 2
