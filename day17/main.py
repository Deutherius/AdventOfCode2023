import time, os
from heapq import heappush, heappop

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    BCKGGREEN = '\x1b[6;30;42m'
    BCKRED = '\x1b[0;31;41m'
    ENDBCKG = '\x1b[0m'
    ENDC = '\033[0m'

def pad(array2d: list[list[str]], c="", reps=1):
    if reps < 1: return array2d
    res = [c*(len(array2d[0])+reps*2-1)]
    for _ in range(reps-1):
        res.append(c*(len(array2d[0])+reps*2-1))
    for i, line in enumerate(array2d):
        res.append(c*reps + str(array2d[i]).strip() + c*reps)
    for _ in range(reps):
        res.append(c*(len(array2d[0])+reps*2-1))
    return res

def sign(x):
    if (x==0): return 0
    else: return x/abs(x)

def solve(data_orig: str, ultra: bool=False, vis: bool=False):
    dataPadded = pad(data_orig,"f",reps=1)
    grid = [[float("inf") if a == "f" else float(a) for a in line.strip()] for line in dataPadded]
    queue = []
    seen = set()
    costs = {(1, 1, 1, 0): 0, (1, 1, 0, 1): 0}

    heappush(queue, (0, (1, 1), (0, 0)))

    end = (len(grid)-2, len(grid[0])-2)

    neighborDirections = ((0,1), (-1,0), (0,-1), (1,0))
    tmp = []
    if ultra:
        for n in neighborDirections:
            for i in range(4,11):
                tmp.append((n[0]*i, n[1]*i))
        neighborDirections = tmp.copy()
    else:
        for n in neighborDirections:
            for i in range(1,4):
                tmp.append((n[0]*i, n[1]*i))
        neighborDirections = tmp.copy()

    while queue:
        c, (y, x), (dy, dx) = heappop(queue)
        if (y,x) == end:
            break
        #prevent cycles
        if ((y, x), (sign(dy), sign(dx))) in seen:
            continue
        seen.add(((y, x), (sign(dy), sign(dx))))

        for (ndy, ndx) in neighborDirections:
            ny, nx = y + ndy, x + ndx #new coordinates if this neighbor passes

            #this neighbor can only be valid if it's within the grid
            if not ((1 <= ny <= len(grid)-2) and (1 <= nx <= len(grid[0])-2)):
                continue

            #this would be continuing, we do not want that
            if sign(dx) == sign(ndx) and sign(dy) == sign(ndy):
                continue
            #this neighbor can only be valid if the cart is not turning back
            if (sign(dy) == -1*sign(ndy) and sign(dx) == sign(ndx)) or (sign(dy) == sign(ndy) and sign(dx) == -1*sign(ndx)):
                continue

            #cost is now moving through all the nodes at once
            nCost = c
            if ndy > 0:
                nCost += sum(row[x] for row in grid[y+1:ny+1])
            elif ndy < 0:
                nCost += sum(row[x] for row in grid[ny:y])
            elif ndx > 0:
                nCost += sum(grid[y][x+1:nx+1])
            elif ndx < 0:
                nCost += sum(grid[y][nx:x])

            nNode = ((ny, nx), (ndy, ndx))
            if not nNode in costs or costs[nNode] > nCost:
                #it's uncalculated or the cost is greater than we can provide, change it
                costs[nNode] = nCost
                #push this new node to the queue
                heappush(queue, (nCost, *nNode))
    #queue is empty - check anything that has coordinates of the end node
    scores = []
    for k,v in costs.items():
        if k[0] == end:
            scores.append(v)
    return int(min(scores))

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
print("Elapsed time for part 1: " + str(float(then-now)/repeats) + " s average per run")

now = time.time()
for _ in range(0,repeats):
    if repeats > 1:
        _ = solve(data_orig=data_orig, ultra=True)
    else:
        print(solve(data_orig=data_orig, ultra=True))
then = time.time()
print("Elapsed time for part 2: " + str(float(then-now)/repeats) + " s average per run")
