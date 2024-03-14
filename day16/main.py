import time, os
from collections import deque

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    BCKGGREEN = '\x1b[6;30;42m'
    BCKRED = '\x1b[0;31;41m'
    ENDBCKG = '\x1b[0m'
    ENDC = '\033[0m'

def pad(array2d, c="", reps=1):
    if reps < 1: return array2d
    res = [c*(len(array2d[0])+reps*2-1)]
    for _ in range(reps-1):
        res.append(c*(len(array2d[0])+reps*2-1))
    for i, line in enumerate(array2d):
        res.append(c*reps + str(array2d[i]).strip() + c*reps)
    for _ in range(reps):
        res.append(c*(len(array2d[0])+reps*2-1))
    return res

def visualize(field: list[list[str]], energies: list[list[int]], coords: deque[tuple[int, int, int]]):
    os.system('cls' if os.name == 'nt' else 'clear')
    for i, line in enumerate(field):
        lineString = ""
        for j, c in enumerate(line):
            for k in range(4):
                if tuple((i, j, k)) in coords:
                    lineString += bcolors.BCKGGREEN + c + bcolors.ENDBCKG
                    break
            else:
                if energies[i][j]:
                    lineString += bcolors.BCKRED + c + bcolors.ENDBCKG
                else:
                    lineString += c
        print(lineString)
    time.sleep(0.05)

def solve(data_orig: str, vis: bool=False):
    data = pad(data_orig, c="#", reps=1)
    mirrors = [[] for _ in range(len(data))]
    beams = deque()
    for i, line in enumerate(data):
        for c in line.strip():
            mirrors[i].append(c)
    # / mirror:
    #right <-> up
    #left <-> down
    # \ mirror
    # right <-> down
    # up <-> left
    dirChangeByMirror = {("/", 0): 1, ("/", 1): 0, ("/", 2): 3, ("/", 3): 2,\
                         ("\\", 0): 3, ("\\", 3): 0, ("\\", 1): 2, ("\\", 2): 1}
    
    topScore = 0

    #generate possible starts
    #can start on any (0, X, 3) where X is 1..end-1 for row width
    #can start on any (end, X, 1) where X is 1..end-1 for row width
    #can start on any (X, 0, 0) where X is 1..end-1 for matrix height
    #can start on any (X, end, 2) where X is 1..end-1 for matrix height
    starts = []
    for X in range(1, len(mirrors[0])-1):
        starts.append((0, X, 3))
        starts.append((len(mirrors)-1, X, 1))
    for X in range(1, len(mirrors)-1):
        starts.append((X, 0, 0))
        starts.append((X, len(mirrors[0])-1, 2))

    for start in starts:
        beams.appendleft(start) # coordinates, Y, X, heading -> heading 0 = right, 1 = up, 2 = left, 3 = down
        beamCache = {}
        concurrentBeams = 1
        energies = [[0 for _ in line] for line in mirrors]

        while beams:
            for _ in range(concurrentBeams):
                beam = beams.pop()
                energies[beam[0]][beam[1]] = 1
                if not beamCache.get(beam):
                    beamCache[beam] = 1
                else:
                    concurrentBeams -= 1
                    continue
                match beam[2]:
                    case 0:
                        #beam going right, test what is there
                        beamNext = (beam[0], beam[1]+1, beam[2])
                    case 1: #up
                        beamNext = (beam[0]-1, beam[1], beam[2])
                    case 2: #left
                        beamNext = (beam[0], beam[1]-1, beam[2])
                    case 3: #down
                        beamNext = (beam[0]+1, beam[1], beam[2])
                nextTile = mirrors[beamNext[0]][beamNext[1]]
                match nextTile:
                    case ".":
                        #just move
                        beams.appendleft(beamNext)
                    case "|":
                        #test if splitting, if not just move
                        if beam[2] in [0,2]:
                            concurrentBeams += 1
                            #plitting
                            beams.appendleft((beamNext[0], beamNext[1], 1))
                            beams.appendleft((beamNext[0], beamNext[1], 3))
                        else:
                            #passing through
                            beams.appendleft(beamNext)
                    case "-":
                        if beam[2] in [1,3]:
                            concurrentBeams += 1
                            #plitting
                            beams.appendleft((beamNext[0], beamNext[1], 0))
                            beams.appendleft((beamNext[0], beamNext[1], 2))
                        else:
                            #passing htrough
                            beams.appendleft(beamNext)
                    case "/" | "\\":
                        beams.appendleft((beamNext[0], beamNext[1], dirChangeByMirror[(nextTile, beamNext[2])]))
                    case "#":
                        #end of beam, goodbye
                        concurrentBeams -= 1
            if vis: visualize(mirrors, energies, beams)
        if start == (1, 0, 0):
            p1Score = sum([sum(a) for a in energies])-1
        topScore = max(topScore, sum([sum(a) for a in energies])-1)
        if vis: os.system("pause") 
    return p1Score, topScore

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
