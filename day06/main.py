import time
import math

def part1(data_orig):
    data = [list(map(int, (" ".join(a.split(":")[1].split()).split(" ")))) for a in data_orig]
    debug = False
    raceTotals = [0] * len(data[0])
    for raceIndex, (raceTime, raceDistance) in enumerate(zip(data[0], data[1])):
        if debug: print(f"Index: {raceIndex}, Time: {raceTime}, distance: {raceDistance}")
        #need to wind up some ms and have more distance, sum how many ways could we do that
        for windUpTime in range(0, raceTime):
            resTime = raceTime-windUpTime
            dist = windUpTime*resTime
            if debug: print(f"Windup of {windUpTime} ms, distance of {dist}, beats {raceDistance}? {'yes' if dist > raceDistance else 'no'}")
            raceTotals[raceIndex] += 1 if dist > raceDistance else 0

    return math.prod(raceTotals)

#part 2
def part2(data_orig):
    data = [int(("".join(a.split(":")[1].split()).split(" ")[0])) for a in data_orig]

    debug = False
    total = 0
    Winning = False
    raceTime, raceDistance = data
    for windUpTime in range(0, raceTime):
        resTime = raceTime-windUpTime
        dist = windUpTime*resTime
        if debug: print(f"Windup of {windUpTime} ms, distance of {dist}, beats {raceDistance}? {'yes' if dist > raceDistance else 'no'}")
        if dist > raceDistance:
            total += 1
            if not Winning:
                Winning = True
            continue
        if total and dist <= raceDistance:
            break
    return total

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