import time

def Area(corners): #shoelace from stackoverflow - https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area

def drawOutline(coords: tuple[int, int], instructions: str, part2: bool=False) -> tuple[list[tuple[int, int]], int]:
    dirs = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1),\
            "3": (-1, 0), "1": (1, 0), "2": (0, -1), "0": (0, 1)}
    setOfCoords = [coords]
    x, y = coords
    addon = 0
    for line in instructions:
        dir, dist, hex = line.strip().replace("(", "").replace(")", "").split()
        if not part2:
            dir, dist = dirs[dir], int(dist)
        else:
            dir, dist = dirs[hex[-1]], int("0x0"+hex[1:-1], base=16)

        y, x = y+dir[0]*dist, x+dir[1]*dist
        addon += dist
        setOfCoords.append((y, x))
    return setOfCoords, addon

def solve(data_orig: str, part2: bool=False) -> int:
    setOfCoords, addon = drawOutline(coords=(0, 0), instructions=data_orig, part2=part2)
    return int(Area(setOfCoords) + addon/2 + 1)

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
