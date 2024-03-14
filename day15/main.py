import time
from functools import cache
from collections import defaultdict

@cache
def hash(input: str):
    h = 0
    for c in input.strip():
        h += ord(c)
        h *= 17
        h = h%256
    return h

def solve(data_orig: str):
    boxes = defaultdict(list)
    tot = 0
    for command in data_orig.strip().split(","):
        tot += hash(command)
        commandParts = command.replace("=", " ").replace("-", " ").split()

        operatorIndex = len(commandParts[0])
        h = hash(commandParts[0])

        if command[operatorIndex] == "=":
            lensName, lensNumber = command.split("=")
            if boxes:
                for lens in boxes[h]:
                    if lens[0] == lensName:
                        lst = boxes[h]
                        lensIndex = lst.index(lens)
                        lst.pop(lensIndex)
                        lst.insert(lensIndex, (lensName, lensNumber))
                        boxes[h] = lst
                        break #only one will ever be present
                else:
                    lst = boxes[h]
                    lst.append((lensName, lensNumber))
                    boxes[h] = lst
            else:
                boxes[h] = [(lensName, lensNumber)]
        elif command[operatorIndex] == "-":
            lensName = command.split("-")[0]
            if boxes:
                for lens in boxes[h]:
                    if lens[0] == lensName:
                        boxes[h].pop(boxes[h].index(lens))
                        break #only one will ever be present
                
    tot2 = 0
    for i in range(256):
        if boxes[i]:
            for j, lens in enumerate(boxes[i]):
                tot2 += (i+1) * (j+1) * int(lens[1])

    return tot, tot2

# with open("inp_ex.txt", "r") as inp:
with open("inp.txt", "r") as inp:
    data_orig = inp.read()
repeats = 1

now = time.time()
for _ in range(0,repeats):
    if repeats > 1:
        _ = solve(data_orig=data_orig)
    else:
        print(solve(data_orig=data_orig))
then = time.time()
print("Elapsed time for parts 1 and 2: " + str(float(then-now)/repeats) + " s average per run")
