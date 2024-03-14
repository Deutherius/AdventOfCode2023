from math import prod
import time

def part1(data_orig):
    data = [[int(x) for x in " ".join(i.split(":")[1].split()).split(" ")] for i in data_orig]

    raceTotals = [0] * len(data[0])
    for raceIndex, (raceTime, raceDistance) in enumerate(zip(data[0], data[1])):
        for windUpTime in range(0, raceTime):
            dist = windUpTime*(raceTime-windUpTime)
            raceTotals[raceIndex] += 1 if dist > raceDistance else 0

    return prod(raceTotals)
    

def part2(data_orig):
    raceTime, raceDistance = [int("".join(a.split(":")[1].split()).split(" ")[0]) for a in data_orig]

    # binary search
    testTime = round(raceTime/2)
    step = round(raceTime/4)
    while step > 0:
        if testTime*(raceTime-testTime) > raceDistance:
            testTime, step, lastWin = testTime-step, round(step/2), True
        else:
            testTime, step, lastWin = testTime+step, round(step/2), False
    if lastWin:
        testTime += 1
    leftBound = testTime

    testTime = round(raceTime/2)
    step = round(raceTime/4)
    while step > 0:
        if testTime*(raceTime-testTime) > raceDistance:
            testTime, step, lastWin = testTime+step, round(step/2), True
        else:
            testTime, step, lastWin = testTime-step, round(step/2), False
    if not lastWin:
        testTime += 1

    return testTime-leftBound
    

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
print("Elapsed time: " + str((then-now)/repeats) + " s")