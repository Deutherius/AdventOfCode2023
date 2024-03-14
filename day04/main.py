import time
from collections import Counter

now = time.time()
# with open("inp_ex.txt", "r") as inp:
with open("inp.txt", "r") as inp:
    data = inp.readlines()

total = 0
cardCt = Counter()

for cardNum, line in enumerate(data):
    cardNum += 1
    cardCt[cardNum] += 1 # the original card you have
    left, right = line.strip().split("|")
    winNums = [int(n) for n in left.split(":")[1].strip().replace("  ", " ").split(" ")]
    ourNums = [int(n) for n in right.strip().replace("  ", " ").split(" ")]
    matches = set(ourNums) & set(winNums)
    if len(matches):
        total += 2**(len(matches)-1)
        for i in range(1, len(matches)+1): #the extra cards we won
            cardCt[cardNum+i] += cardCt[cardNum]

print(total)
print(cardCt.total())

then = time.time()
print("Elapsed time: " + str(then-now) + " s")