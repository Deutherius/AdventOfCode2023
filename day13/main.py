import time

def findMirrorPoint(data, oldres=0):
    hdata = ["".join(l) for l in data]
    vdata = ["".join(l) for l in list(zip(*data))]

    nv = len(vdata)
    vres = 0
    for i in range(1,nv):
        left_side = vdata[:i]
        right_side = vdata[i:]
        left_rev = left_side[::-1]
        for a,b in zip(right_side, left_rev):
            if not a == b:
                break
        else:
            if not i == oldres: 
                vres = i
                break

    nh = len(hdata)
    hres = 0
    for i in range(1,nh):
        left_side = hdata[:i]
        right_side = hdata[i:]
        left_rev = left_side[::-1]
        for a,b in zip(right_side, left_rev):
            if not a == b:
                break
        else:
            if not i*100 == oldres: 
                hres = i
                break

    if hres: return hres*100
    if vres: return vres
    return 0

def solve(data_orig):
    data = []
    tot = 0
    tot2 = 0
    for i, line in enumerate(data_orig):
        if line.strip():
            data.append([c for c in line.strip()])
        if not line.strip() or i == len(data_orig)-1: #empty line or EOF
            p1add = findMirrorPoint(data)
            tot += p1add
            #part 2 - change ALL the smudges!
            for i, line in enumerate(data):
                for j, _ in enumerate(line):
                    
                    data[i][j] = "#" if data[i][j] == "." else "." #change one symbol

                    res2 = findMirrorPoint(data, oldres=p1add)

                    data[i][j] = "#" if data[i][j] == "." else "." #change it back

                    if not res2:
                        continue
                    tot2 += res2
                    break        
                else:
                    continue
                break
            data = []
    return tot, tot2


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
print("Elapsed time for parts 1 and 2: " + str(float(then-now)/repeats) + " s average per run")
