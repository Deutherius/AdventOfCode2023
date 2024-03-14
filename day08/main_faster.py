import time
from collections import deque
from math import lcm

def solve(data_orig, ghost=False):
    path = data_orig[0]
    p = deque()
    for char in path.strip():
        p.append(0 if char == 'L' else 1)
    nodesLookup = {}
    nodeStarts = []
    for line in data_orig[2:]:
        src, dstL, dstR = line.strip().replace("= ", "").replace("(", "").replace(",", "").replace(")", "").split()
        nodesLookup[src] = (dstL, dstR)
        if str.endswith(src, 'A'):
            nodeStarts.append(src)

    if not ghost: #part 1
        node = 'AAA'
        total = 0
        while not node == 'ZZZ':
            # do a move
            node = nodesLookup[node][p[0]]
            p.rotate(-1)
            total += 1
    else: #part 2
        loopLens = [[] for _ in range(len(nodeStarts))]
        
        for i in range(len(nodeStarts)):
            pp = p.copy()
            ct = 0
            node = nodeStarts[i]
            while True:
                ct += 1
                node = nodesLookup[node][pp[0]]
                pp.rotate(-1)
                if str.endswith(node, 'Z'):
                    loopLens[i] = ct
                    break
        total = lcm(*loopLens)

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

repeats = 1
now = time.time()
for _ in range(0,repeats):
    if repeats > 1:
        _ = solve(data_orig=data_orig, ghost=True)
    else:
        print(solve(data_orig=data_orig, ghost=True))
then = time.time()
print("Elapsed time for part 2: " + str(float(then-now)/repeats) + " s average per run")