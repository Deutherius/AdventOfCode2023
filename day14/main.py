import time
from functools import cache
from math import floor

def pad(array2d, c="", reps=1):
    if reps < 1: return array2d
    res = [c*(len(array2d[0])+reps*2-1)]
    for _ in range(reps-1):
        res.append(c*(len(array2d[0])+reps*2-1))
    for i, line in enumerate(array2d):
        res.append(c*reps + str(array2d[i]).strip() + c*reps)
    for _ in range(reps):
        res.append(c*(len(array2d[0])+reps*2-1))
    return res

@cache
def gravityFalls(field: tuple[tuple[str]]):
    data = [list(inner) for inner in field]
    for Y, line in enumerate(data):
        if Y == 0 or Y == len(data)-1: continue
        for X, element in enumerate(line):
            if X == 0 or X == len(line)-1: continue
            if element == "O":
                #check above to see if or how far we can move the rock
                tmpY = Y
                while data[tmpY-1][X] == ".":
                    tmpY -= 1
                #tmpY now holds the max Y where we can move the element, move it
                data[tmpY][X], data[Y][X] = data[Y][X], data[tmpY][X]

    return tuple(tuple(a for a in l) for l in data)

@cache
def rotate(field: tuple[tuple[str]]):
    return tuple(zip(*reversed(field)))

def calcLoad(field: tuple[tuple[str]]):
    loads = [[len(field)-i-1 if a == "O" else 0 for a in line] for i,line in enumerate(field)]
    return sum(a for l in loads for a in l)

def solve(data_orig):
    data = pad(data_orig, c="#", reps=1)
    data = [[a for a in line.strip()] for line in data]
    
    BIGLOOPS = 1_000_000_000

    cache = {}
    loop_start = -1
    loop_end = -1

    tot = 0
    tot2 = 0
    data = tuple(tuple(a for a in line) for line in data)

    data = gravityFalls(data)
    tot = calcLoad(data)
    k = 0
    while k < BIGLOOPS:
        for _ in range(4):
            data = gravityFalls(data)
            data = rotate(data)
            
        if cache.get(data):
            #we have seen this
            loop_start = cache[data]
            loop_end = k
            loop_length = loop_end-loop_start
            loopies = (BIGLOOPS-loop_end)/loop_length
            k = loop_end + floor(loopies)*loop_length
            cache = {} #delete cache so we don't get re-hits
        else:
            cache[data] = k
        k += 1

    tot2 = calcLoad(data)
    return tot, tot2

# 
# with open("inp_ex.txt", "r") as inp:
with open("inp.txt", "r") as inp:
    data_orig = inp.readlines()
repeats = 1
now = time.time()
for _ in range(0,repeats):
    if repeats > 1:
        _ = solve(data_orig=data_orig)
    else:
        print(solve(data_orig=data_orig))
then = time.time()
print("Elapsed time for parts 1 and 2: " + str(float(then-now)/repeats) + " s average per run")
