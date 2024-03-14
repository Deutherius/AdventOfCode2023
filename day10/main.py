import time
from collections import deque

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

def pad(array2d, c="", reps=1):
    if reps < 1: return array2d
    res = ["."*(len(array2d[0])+reps*2-1)]
    for _ in range(reps-1):
        res.append("."*(len(array2d[0])+reps*2-1))
    for i, line in enumerate(array2d):
        res.append("."*reps + str(array2d[i]).strip() + "."*reps)
    for _ in range(reps):
        res.append("."*(len(array2d[0])+reps*2-1))
    return res

def solve(data_orig):
    transMap = {".": "  ", "|": "NS", "-": "EW", "L": "NE", "J": "NW", "7": "SW", "F": "SE", "S": "NWSE"}
    dirSwaps = {"E": "W", "W": "E", "N": "S", "S": "N"}
    pipes = []
    dists = []
    queue = deque()
    # add padding of "."
    dataPadded = pad(data_orig, ".", 1)

    for line in dataPadded:
        pipes.append([transMap[c] for c in line.strip()])
        dists.append([0 if(c == "S") else -1 for c in line.strip()])

    #find where start is
    [startCoords] = [ (i, x.index("NWSE")) for i, x in enumerate(pipes) if "NWSE" in x ]
    queue.appendleft(startCoords)
    while queue:
        #check directions of current coord from queue
        (Y, X) = queue.pop()
        validDirs = []
        #only look to where this pipe is connecting
        for direction in pipes[Y][X]:
            if not direction.strip(): continue
            dS = str.replace(direction, direction, dirSwaps[direction]) #opposite of where we are looking
            match direction:
                case "N":
                    if dists[Y-1][X] != -1: continue
                    newCoords = (Y-1, X)
                case "S":
                    if dists[Y+1][X] != -1: continue
                    newCoords = (Y+1, X)
                case "W":
                    if dists[Y][X-1] != -1: continue
                    newCoords = (Y, X-1)
                case "E":
                    if dists[Y][X+1] != -1: continue
                    newCoords = (Y, X+1)
            newNode = pipes[newCoords[0]][newCoords[1]]
            if set(newNode).intersection(dS):
                queue.appendleft(newCoords)
                dists[newCoords[0]][newCoords[1]] = dists[Y][X] + 1
                if pipes[Y][X] == "NWSE": #figure out Starting tile type
                    validDirs.append(direction)
        if pipes[Y][X] == "NWSE":
            #change starting node to correct type for part 2
            pipes[Y][X] = "".join(validDirs)

    inct = 0
    for Y, line in enumerate(dataPadded):
        inside = False
        for X, _ in enumerate(line):
            if dists[Y][X] + 1:
                # this is a loop segment, figure out if it's north-facing
                if "N" in pipes[Y][X] and not inside:
                    inside = True
                elif "N" in pipes[Y][X] and inside:
                    inside = False
            else:
                #this is not part of the loop, mark it for ouside/inside
                if inside:
                    inct += 1
    return (max(*[item for row in dists for item in row]), inct)

# with open("inp_ex.txt", "r") as inp:
# with open("inp_ex2.txt", "r") as inp:
# with open("inp_ex3.txt", "r") as inp:
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
