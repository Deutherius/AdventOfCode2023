import time
from collections import Counter
from operator import itemgetter

def rank_hand(hand, joker=False):
    ct = Counter(hand)
    res = ct.most_common()

    if joker and ct.get("J") and len(res) > 1:
        #index of the J tuple
        jIndex = res.index(("J", ct["J"]))
        #change J to the most common letter that is not J, unless the hand is full of Js
        if jIndex == 0:
            res[1] = (res[1][0], res[1][1] + res[0][1])
            res.pop(0)
        else:
            res[0] = (res[0][0], res[0][1] + res[jIndex][1])
            res.pop(jIndex)

    if res[0][1] == 5: return 6 #five of a kind
    elif res[0][1] == 4: return 5 #four of a kind
    elif res[0][1] == 3 and res[1][1] == 2: return 4 #full house
    elif res[0][1] == 3:  return 3 #three of a kind
    elif res[0][1] == 2 and res[1][1] == 2: return 2 #two pairs
    elif res[0][1] == 2: return 1 #one pair
    return 0

def transform_hand(hand, letter_ranks, joker=False):
    hand_score = 0
    #hand power
    hand_score += 10000000000 * rank_hand(hand, joker)
    #letter scores
    for index, letter in enumerate(reversed(hand)):
        hand_score += 10**(index*2)*letter_ranks[letter]
    return hand_score

def solve(data_orig, joker=False):
    data = []
    letter_ranks = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
    if joker: letter_ranks["J"] = 1
    
    for line in data_orig:
        hand, bid = line.strip().split(" ")[0], int(line.strip().split(" ")[1])
        #replace actual hand with hand score - power is high number, cards get converted to lower number
        newHand = transform_hand(hand, letter_ranks, joker=joker)
        data.append((newHand, bid))
    
    data_sorted = sorted(data, key=itemgetter(0), reverse=True)

    total = 0
    for rank, (_, bid) in enumerate(reversed(data_sorted), start=1):
        total += bid*(rank)
    return total

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

repeats = 1
now = time.time()
for _ in range(0,repeats):
    if repeats > 1:
        _ = solve(data_orig=data_orig, joker=True)
    else:
        print(solve(data_orig=data_orig, joker=True))
then = time.time()
print("Elapsed time for part 2: " + str(float(then-now)/repeats) + " s average per run")