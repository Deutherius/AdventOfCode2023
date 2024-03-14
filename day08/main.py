import time
from collections import deque
from math import lcm

def solve(data_orig, ghost=False):
    path = data_orig[0]
    p = deque()
    for char in path.strip():
        p.append(0 if char == 'L' else 1)
    data = {}
    gS = []
    for line in data_orig[2:]:
        src, dstL, dstR = line.strip().replace("= ", "").replace("(", "").replace(",", "").replace(")", "").split()
        data[src] = (dstL, dstR)
        if str.endswith(src, 'A'):
            gS.append(src)

    if not ghost: #part 1
        node = 'AAA'
        total = 0
        while not node == 'ZZZ':
            # do a move
            node = data[node][p[0]]
            p.rotate(-1)
            total += 1
    else: #part 2
        loopLens = [[] for _ in range(len(gS))]
        offsets = [0] * len(gS)

        ct = 0
        while any(len(a) < 2 for a in loopLens): #loop until we find all loop lengths
            ct += 1
            # do a move
            gS = [data[gS[i]][p[0]] for i in range(len(gS))]
            p.rotate(-1)
            #if we get a Z anywhere, log its index for analysis
            z = [str.endswith(n, 'Z') for n in gS]
            if any(z):
                for i in range(len(gS)):
                    if z[i]:
                        if not offsets[i]:
                            offsets[i] = ct
                        loopLens[i].append(ct)
        #get loop length for each path
        for i in range(len(gS)):
            tmp = []
            for j, _ in enumerate(loopLens[i]):
                if j:
                    tmp.append(loopLens[i][j]-loopLens[i][j-1])
            if all(a == tmp[0] for a in tmp): #sanity check
                loopLens[i] = tmp[0]

        total = 1
        for i in loopLens:
            total = lcm(total, i)

    return total

# with open("inp_ex.txt", "r") as inp:
# with open("inp_ex2.txt", "r") as inp:
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


# with open("inp_ex3.txt", "r") as inp:
with open("inp.txt", "r") as inp:
    data_orig = inp.readlines()
repeats = 1
now = time.time()
for _ in range(0,repeats):
    if repeats > 1:
        _ = solve(data_orig=data_orig, ghost=True)
    else:
        print(solve(data_orig=data_orig, ghost=True))
then = time.time()
print("Elapsed time for part 2: " + str(float(then-now)/repeats) + " s average per run")