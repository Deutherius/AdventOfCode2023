if __name__=="__main__":
    import time, os
    from collections import deque
    from heapq import heapify, heappop, heappush
    from functools import cache
    from helpers import pad, bcolors as b
    from copy import deepcopy
    from math import lcm
    import cProfile

    def isIntersecting(interval1, interval2):
        (startX, endX), (startY, endY), (startZ, endZ) = interval1
        (startX2, endX2), (startY2, endY2), (startZ2, endZ2) = interval2

        # Check if the intervals overlap
        return max(startX, startX2) <= min(endX, endX2) and max(startY, startY2) <= min(endY, endY2) and max(startZ, startZ2) <= min(endZ, endZ2)

    def runGravity(falling_orig:list[list[int, int], list[int, int], list[int, int]]):
        falling = deepcopy(falling_orig)
        resting = []
        numFell = 0
        fallingTmp = falling.copy()
        for b in fallingTmp:
            if b[2][0] == 1:
                #resting on the ground, can't move
                falling.pop(falling.index(b))
                resting.append(b)
                continue
            # brick is not on the ground - figure out if letting it fall one round makes it intersect any other brick
            # or hit the ground - if not, let it fall until it does
            bTmp = deepcopy(b)
            while True:
                #fall one step
                bTmp[2][0], bTmp[2][1] = bTmp[2][0]-1, bTmp[2][1]-1
                #check intersection with resting bricks
                for b2 in reversed(resting): #reversed because probably gonna hit one of the last added resting
                    if isIntersecting(bTmp, b2):
                        break
                else:
                    #did not break, i.e. not intersecting
                    # check ground
                    if bTmp[2][0] == 1:
                        numFell += 1
                        #resting on the ground, can't move
                        falling.pop(falling.index(b))
                        resting.append(bTmp)
                        break
                    #not on the ground, let fall
                    continue
                #did break at resting pieces - is intersecting, move back up
                bTmp[2][0], bTmp[2][1] = bTmp[2][0]+1, bTmp[2][1]+1
                #and since it can't fall down due to other pieces, it is now resting
                if not bTmp == b:
                    numFell += 1
                falling.pop(falling.index(b))
                resting.append(bTmp)
                break
                

        return resting, numFell

    def solve(data_orig: str, part2: bool=False):
        fallingBricks = []
        
        for line in data_orig:
            xmin, ymin, zmin, xmax, ymax, zmax = map(int, line.replace("~", ",").split(","))
            fallingBricks.append([[xmin, xmax], [ymin, ymax], [zmin, zmax]])

        fallingBricks.sort(key=lambda x: x[2][0])

        restingBricks = []

        tic = time.time()
        restingBricks, numFell = runGravity(fallingBricks)

        print(f"stack is stable, took {time.time()-tic} s with {numFell} bricks counted as falling")

        p1Ct = 0
        p2Ct = 0

        for i, brick in enumerate(restingBricks):
            tic = time.time()
            #try disintegrating, see if the stack falls - if not, add one to counter
            potentiallyFallingBricks = deepcopy(restingBricks)
            potentiallyFallingBricks.pop(potentiallyFallingBricks.index(brick))

            _, numFell = runGravity(potentiallyFallingBricks)

            #part 2 - figure out how many "bricks" are in newResting but not in potentiallyFallingBricks
            if not numFell:
                p1Ct += 1
            p2Ct += numFell
            print(f"disintegrating {i}/{len(restingBricks)} took {time.time() - tic} s with {numFell} bricks counted as falling")
        return p1Ct, p2Ct

    # with open("inp_ex.txt", "r") as inp:
    with open("inp.txt", "r") as inp:
        data_orig = inp.read().strip().splitlines()
    repeats = 1

    now = time.time()
    for _ in range(0,repeats):
        if repeats > 1:
            _ = solve(data_orig=data_orig)
        else:
            print(solve(data_orig=data_orig))
    then = time.time()
    print("Elapsed time for parts 1 and 2: " + str(float(then-now)/repeats) + " s average per run")