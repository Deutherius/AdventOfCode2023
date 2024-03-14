import time
import math

def part1(data_orig):
    data = [list(map(int, (" ".join(a.split(":")[1].split()).split(" ")))) for a in data_orig]
    raceTotals = [0] * len(data[0])
    for raceIndex, (raceTime, raceDistance) in enumerate(zip(data[0], data[1])):
        for windUpTime in range(0, raceTime):
            dist = windUpTime*(raceTime-windUpTime)
            raceTotals[raceIndex] += 1 if dist > raceDistance else 0

    return math.prod(raceTotals)

def part2(data_orig):
    data = [int("".join(a.split(":")[1].split()).split(" ")[0]) for a in data_orig]

    raceTime, raceDistance = data

    #analytical solution
    lb = math.floor((raceTime - math.sqrt((raceTime**2 - 4 * raceDistance)))/2)
    ub = math.ceil((raceTime + math.sqrt((raceTime**2 - 4 * raceDistance)))/2)

    return (ub - lb - 1)

repeats = 1

now = time.time()
# with open("inp_ex.txt", "r") as inp:
with open("inp.txt", "r") as inp:
    data_orig = inp.readlines()
for _ in range(0,repeats):
    if repeats > 1:
        _ = part1(data_orig=data_orig)
        _ = part2(data_orig=data_orig)
    else:
        print(part1(data_orig=data_orig))
        print(part2(data_orig=data_orig))

then = time.time()
print("Elapsed time: " + str(float(then-now)/repeats) + " s")