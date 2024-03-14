import time
from itertools import product, accumulate
from functools import cache
import os

@cache
def genPerms(string: str, nums: tuple[int]):
    if len(nums) == 0: #no numbers remaining
        if not "#" in string: #but no broken springs in string either, so we are done and this works
            return 1
        else:
            return 0 #some broken springs unaccounted for, this does not work
    
    min_start = 0
    max_start = len(string) - sum(nums) - len(nums) + 1
    #      total length - sum of nums - separators + first num does not need separator

    if "#" in string: #we need to start at worst at a static broken spring if one exists
        max_start = min(string.index("#"), max_start)
    
    num, *numsRest = nums #unpack first number
    retVal = 0 #total possible for current arrangement

    for start in range(min_start, max_start + 1): #sliding window
        end = start + num
        segment = string[start:end]
        #check if
        # 1) all segment characters are either # or ?
        # 2) if the segment terminates before end of string
        # 3) if the char after this segment is ".?" or end of string
        #any of those fail, move on
        matchingChars = all(a in "#?" for a in segment)
        endOfString = end >= len(string)
        segmentTerminated = endOfString or string[end] in ".?"
        if not matchingChars or not segmentTerminated:
            continue
        #passed, valid place to put the segment in

        stringRest = string[end + 1:]

        retVal += genPerms(stringRest, tuple(numsRest))

    return retVal

def solve(data_orig, part2=False):
    tot = 0
    for line in data_orig:

        hashDots, numbers = line.strip().split()
        if part2:
            #join 5x springmap with ?
            hashDots = "?".join(hashDots for _ in range(5))
            numbers = ",".join(numbers for _ in range(5))

        tot += genPerms(hashDots, tuple([int(a) for a in numbers.split(",")]))
   
    return tot


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

now = time.time()
for _ in range(0,repeats):
    if repeats > 1:
        _ = solve(data_orig=data_orig, part2=True)
    else:
        print(solve(data_orig=data_orig, part2=True))
then = time.time()
print("Elapsed time for part 2: " + str(float(then-now)/repeats) + " s average per run")