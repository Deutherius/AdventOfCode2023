import time
from collections import Counter
import os

now = time.time()
# with open("inp_ex.txt", "r") as inp:
with open("inp.txt", "r") as inp:
    data = inp.readlines()


debug = False
seeds = []
maps = [[] for _ in range(0,7)]
#parse maps
for line in data:
    if line.startswith("seeds:"):
        seeds = [int(n) for n in line.lstrip("seeds: ").strip().split(" ")]
        continue
    if line.startswith("seed-to-soil map:"):
        parsingIndex = 0
        continue
    if line.startswith("soil-to-fertilizer map:"):
        parsingIndex = 1
        continue
    if line.startswith("fertilizer-to-water map:"):
        parsingIndex = 2
        continue
    if line.startswith("water-to-light map:"):
        parsingIndex = 3
        continue
    if line.startswith("light-to-temperature map:"):
        parsingIndex = 4
        continue
    if line.startswith("temperature-to-humidity map:"):
        parsingIndex = 5
        continue
    if line.startswith("humidity-to-location map:"):
        parsingIndex = 6
        continue
    if not line or line == "\n":
        continue    
    #now the line can only contain numbers
    maps[parsingIndex].append([int(n) for n in line.strip().split(" ")])

#part 1
locNums = []
#go through seeds and map to location
for seed in seeds:
    tmpNum = seed
    if debug: print(f"New seed {tmpNum}")
    for stageIndex, stage in enumerate(maps):
        if debug: print(f"Now doing stage {stageIndex}")
        transformedWithStage = False
        for substage in stage:
            #first number is destination, second is source, third is range
            if tmpNum >= substage[1] and tmpNum <= substage[1] + substage[2]:
                #number is within this substage range, transform it to destination number
                offset = tmpNum-substage[1]
                if debug: print(f"tmpNum {tmpNum} falls within substage range {substage[1]} - {substage[1] + substage[2]}, transforming to {substage[0] + offset}")
                if debug: print(substage)
                if debug: print(offset)
                tmpNum = substage[0] + offset
                transformedWithStage = True
                # os.system("pause")
                break
        if not transformedWithStage:
            if debug: print(f"{tmpNum} does not fall within any range, stays the same")
    locNums.append(tmpNum)
#figure out the smallest location number
result = min(locNums)
print(f"Smallest loc number is {result}")

then = time.time()
print("Elapsed time: " + str(then-now) + " s")

now2 = time.time()
#part 2, brute force reverse search (interval splitting is faster but less fun)
locNum = 0
# locNum = 9600000
stopped = False
while not stopped:
    locNum += 1
    tmpNum = locNum
    toc = time.time()
    if locNum % 1000000 == 0:
        print(f"Doing loc {locNum/1000000} mil, elapsed time so far is {toc-now} seconds for {locNum/float(toc-now)} iterations/sec")
    for stageIndex, stage in reversed(list(enumerate(maps))):
        transformedWithStage = False
        for substage in stage:
            #zeroth number is destination, first is source, second is range
            if tmpNum >= substage[0] and tmpNum < substage[0] + substage[2]:
                #number is within this substage range, transform it to destination number
                offset = tmpNum-substage[0]
                if debug: print(f"tmpNum {tmpNum} falls within substage range {substage[0]} - {substage[0] + substage[2]}, transforming to {substage[1] + offset}")
                if debug: print(substage)
                if debug: print(offset)
                tmpNum = substage[1] + offset
                transformedWithStage = True
                break
        if not transformedWithStage:
            if debug: print(f"{tmpNum} does not fall within any range, stays the same")
    #fully reverse transformed, check if it's in seeds range
    for index, number in enumerate(seeds):
        if index % 2 == 0:
            #even, base number for the range
            if tmpNum >= number and tmpNum <= (number + seeds[index+1]):
                print(F"Found our result! Location {locNum} is the smallest location!")
                stopped = True
                break

then = time.time()
print("Elapsed time: " + str(then-now2) + " s")