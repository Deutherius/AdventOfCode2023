import time
from math import inf


def solve(data_orig, part2=False):
    data = [[] for _ in range(len(data_orig))]
    lstOfGalaxies = []
    for il, line in enumerate(data_orig):
        for ic, char in enumerate(line.strip()):
            if char == "#":
                data[il].append(1)
                lstOfGalaxies.append((il, ic))
            else:
                data[il].append(0)
    
    #calculate space expansion offsets
    rowOffsets = [0] * len(data)
    colOffsets = [0] * len(data[0])

    increment = 1 if not part2 else 999999
    for i, row in enumerate(data):
        if not any(row):        
            rowOffsets[i:] = [offset + increment for offset in rowOffsets[i:]]
    for i, col in enumerate(zip(*data)):
        if not any(col):        
            colOffsets[i:] = [offset + increment for offset in colOffsets[i:]]

    #apply space expansion
    for index, item in enumerate(lstOfGalaxies):
        lstOfGalaxies[index] = ((item[0] + rowOffsets[item[0]], item[1] + colOffsets[item[1]]))

    #shortest distances
    dists = [[inf for _ in lstOfGalaxies] for _ in lstOfGalaxies]
    for i, c1 in enumerate(lstOfGalaxies):
        for i2, c2 in enumerate(lstOfGalaxies):
            if i2 >= i: continue #just lower triangular
            d = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])
            if dists[i][i2] > d:
                dists[i][i2] = d

    return sum([val for i, row in enumerate(dists) for i2, val in enumerate(row) if i > i2]) #sum lower triangular


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
        _ = solve(data_orig=data_orig, part2=True)
    else:
        print(solve(data_orig=data_orig, part2=True))
then = time.time()
print("Elapsed time for part 2: " + str(float(then-now)/repeats) + " s average per run")
