import time

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

def solve(data_orig, visualize=False):
    transMap = {".": "  ", "|": "NS", "-": "EW", "L": "NE", "J": "NW", "7": "SW", "F": "SE", "S": "NWSE"}
    pipes = []
    pipeLoop = []

    dataPadded = pad(data_orig, ".", 1)

    for line in dataPadded:
        pipes.append([transMap[c] for c in line.strip()])
        pipeLoop.append([1 if(c == "S") else 0 for c in line.strip()])

    [(Y, X)] = [ (i, x.index("NWSE")) for i, x in enumerate(pipes) if "NWSE" in x ]
    
    #figure out where we can go from the starting position
    dist = 0
    if "S" in pipes[Y-1][X]: #north segment facing south
        Y -= 1
        cameFrom = "S"
        firstWent = "N"
    elif "N" in pipes[Y+1][X]: #south segment facing north
        Y += 1
        cameFrom = "N"
        firstWent = "S"
    elif "E" in pipes[Y][X-1]: #west segment looking east
        X -= 1
        cameFrom = "E"
        firstWent = "W"
    elif "W" in pipes[Y][X-1]: #east segment looking west
        X += 1
        cameFrom = "W"
        firstWent = "E"
    
    while True:
        dist += 1
        pipeLoop[Y][X] = 1
        dirToGo = str.replace(pipes[Y][X], cameFrom, "")
        match dirToGo:
            case "N":
                Y -= 1
                cameFrom = "S"
            case "S":
                Y += 1
                cameFrom = "N"
            case "E":
                X += 1
                cameFrom = "W"
            case "W":
                X -= 1
                cameFrom = "E"
            case _: #starting node, fix its type and end the run
                pipes[Y][X] = firstWent + cameFrom
                break

    inct = 0
    for Y, line in enumerate(dataPadded):
        if visualize: linestring = ""
        inside = False
        for X, char in enumerate(line):
            if pipeLoop[Y][X]:
                if visualize: linestring += bcolors.OKBLUE + char + bcolors.ENDC
                # this is a loop segment, figure out if it's north-facing
                if "N" in pipes[Y][X] and not inside:
                    inside = True
                elif "N" in pipes[Y][X] and inside:
                    inside = False
            else:
                #this is not part of the loop, mark it for ouside/inside
                if inside:
                    if visualize: linestring += bcolors.WARNING + char + bcolors.ENDC
                    inct += 1
                else:
                    if visualize: linestring += bcolors.OKGREEN + char + bcolors.ENDC
        if visualize: print(linestring)
    
    return (int(dist/2), inct)

# with open("inp_ex.txt", "r") as inp:
# with open("inp_ex2.txt", "r") as inp:
# with open("inp_ex3.txt", "r") as inp:
with open("inp.txt", "r") as inp:
    data_orig = inp.readlines()
repeats = 1
now = time.time()
for _ in range(repeats):
    if repeats > 1:
        _ = solve(data_orig=data_orig)
    else:
        print(solve(data_orig=data_orig, visualize=True))
then = time.time()
print("Elapsed time for part 1: " + str(float(then-now)/repeats) + " s average per run")
