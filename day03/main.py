class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

import math
import time


now = time.time()
# with open("inp_ex.txt", "r") as inp:
with open("input.txt", "r") as inp:
    data = inp.readlines()

# add padding of "."
data2 = ["."*(len(data[0])+1)]
for i, line in enumerate(data):
    data2.append("." + str(data[i]).strip() + ".")
data2.append("."*(len(data[0])+1))


accumulatingDigits = False
digitString = ""

total = 0
total2 = 0

for i, line in enumerate(data2):
    linestring = "."
    if i == 0 or i == len(data2)-1:
        continue
    for j, symbol in enumerate(line):
        if j == 0:
            continue

        if not symbol.isdigit() and not accumulatingDigits:
            linestring += symbol
        
        # if symbol is number, accumulate all the digits of it
        if symbol.isdigit():
            digitString += symbol
            accumulatingDigits = True
            continue
        elif not symbol.isdigit() and accumulatingDigits:
            # stop accumulating digits, find neighbors
            accumulatingDigits = False
            number = int(digitString)
            # now we have a number, figure out if any symbol around it is not a dot or another digit
            digitArea = data2[i-1][j-len(digitString)-1:j+1] + data2[i][j-len(digitString)-1:j+1] + data2[i+1][j-len(digitString)-1:j+1]
            digitString = ""

            isPartNum = False
            for areaDigit in digitArea:
                if not areaDigit == "." and not areaDigit.isdigit():
                    # add the number to the pile of total
                    isPartNum = True
                    total += number
                    break
            if isPartNum:
                linestring += bcolors.OKBLUE + str(number) + bcolors.ENDC
            else:
                linestring += bcolors.FAIL + str(number) + bcolors.ENDC
            linestring += symbol

        # part 2: gears
        if symbol == "*":
            gearSpace = [data2[i-1][j-1:j+2]]
            gearSpace.append(data2[i][j-1:j+2])
            gearSpace.append(data2[i+1][j-1:j+2])
            gearNumberNeighbors = set()
            for gi, gearLine in enumerate(gearSpace):
                for gj, gearSymbol in enumerate(gearLine):
                    if gearSymbol.isdigit():
                        # go back and forth until we get the complete number
                        # go left first with temp index j
                        tj = j+gj-1
                        while data2[i+gi-1][tj].isdigit():
                            tj -=1
                        #now we have the start of the digit at tj+1
                        #now go right until we hit nondigit and accumulate number
                        tj += 1
                        gAcc = ""
                        while data2[i+gi-1][tj].isdigit():
                            gAcc += data2[i+gi-1][tj]
                            tj += 1
                        #now we should have the entire number
                        #numbers around gears are unique
                        gearNumberNeighbors.add(int(gAcc))
            if len(gearNumberNeighbors) == 2:
                total2 += math.prod(gearNumberNeighbors)

    linestring += "."
            
        


print(total)
print(total2)

then = time.time()
print("Elapsed time: " + str(then-now) + " s")