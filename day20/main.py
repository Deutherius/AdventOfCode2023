import time, os
from collections import deque
from heapq import heapify, heappop, heappush
from functools import cache
from copy import deepcopy
from math import lcm

def PUSH_THE_BUTTON(nodes, numPulsesSentLow):
    queue = deque()
    #create a low signal into the broadcaster, which sends it further
    numPulsesSentLow += 1 #pushed the button, sent a pulse to broadcaster
    for recipient in nodes["broadcaster"][2]:
        numPulsesSentLow += 1 #broadcaster sent a pulse to recipient
        event = ("broadcaster", False, recipient)
        queue.appendleft(event)
    return queue, numPulsesSentLow

def solve(data_orig: str, part2: bool=False):
    FLIPFLOP = "%"
    CONJUNCTION = "&"
    HIGH = True
    LOW = False
    #need to store nodes
    # flipflops only need state and further connections
    # conjunction (NAND) needs to remember what came from each of its connections on the input... and a list of outputs

    # dict of nodes - keys are names
    #                 values are a list [type, state/memory, outputs]
    #                        type is going to be a bool (True: flipflop, False: conjunction, None: broadcast)
    #                        state in the case of type FLIPFLOP: bool
    #                        memory in case of type CONJUNCTION: dict[str, bool] mapping sender (str) and last received signal (bool)
    #                        outputs - list of strings to store names of connected nodes at the output


    #establish nodes
    nodes = {}
    revNodes = {} #reverse connections so we have memory for CONJUNCTIONS
    for line in data_orig:
        # print(line)
        pre, post = line.split(" -> ")
        type = pre[0]
        if type == FLIPFLOP:
            name = pre[1:]
            state = False
        elif type == CONJUNCTION:
            name = pre[1:]
            state = None #for now
        else:
            name = pre
            type = name
            state = None

        connections = [a for a in post.strip().split(", ")]
        for item in connections:
            revNodes.setdefault(item, []).append(name)
        if part2 and name == "rx":
            nodes[name] = [CONJUNCTION, state, connections]    
        else:
            nodes[name] = [type, state, connections]

    #now we need to establish memory for CONJUNCTIONS
    for k, v in nodes.items():
        #if type is conjunction, get all nodes connected to this one and establish their memory
        if v[0] == "&":
            memories = {}
            for value in revNodes[k]:
                memories[value] = False
            nodes[k] = [v[0], memories, v[2]]
    
    if part2:
        cyclesToWatch = {}
        tmpDict = deepcopy(nodes["rx"][1])
        finalNANname = tmpDict.popitem()[0]
        for k in nodes[finalNANname][1].keys():
            cyclesToWatch[k] = []


    numPulsesSentLow = 0
    numPulsesSentHigh = 0
    queue, numPulsesSentLow = PUSH_THE_BUTTON(nodes, numPulsesSentLow)
    buttonPushesRemaining = 999
    buttonPushes = 1

    while True:
        sender, inPulse, recipient = queue.pop()
        # print(f"{sender} -{'high' if inPulse else 'low'}-> {recipient}")
        type, state, sendTo = nodes[recipient]

        if type == FLIPFLOP:
            if inPulse == LOW:
                state = not state
                nodes[recipient][1] = state
                outPulse = state
                for newRecipient in sendTo:
                    event = (recipient, outPulse, newRecipient)
                    queue.appendleft(event)
                    if outPulse:
                        numPulsesSentHigh += 1
                    else:
                        numPulsesSentLow += 1
            
        elif type == CONJUNCTION:
            state[sender] = inPulse
            if all(m == HIGH for m in state.values()):
                outPulse = LOW
            else:
                outPulse = HIGH
            for newRecipient in sendTo:
                event = (recipient, outPulse, newRecipient)
                queue.appendleft(event)
                if outPulse:
                    numPulsesSentHigh += 1
                else:
                    numPulsesSentLow += 1

        #part 2 cycle detection
        if part2 and sender in cyclesToWatch.keys() and inPulse == HIGH:
            cyclesToWatch[sender].append(buttonPushes)             
            if all([len(a) >= 1 for a in cyclesToWatch.values()]):
                break

        if not queue:
            if part2:
                buttonPushes += 1
                queue, numPulsesSentLow = PUSH_THE_BUTTON(nodes, numPulsesSentLow)
            else:
                if buttonPushesRemaining:
                    buttonPushesRemaining -= 1
                    queue, numPulsesSentLow = PUSH_THE_BUTTON(nodes, numPulsesSentLow)
                else:
                    break

    if part2:
        retVal = 1
        for cycle in cyclesToWatch.values():
            retVal = lcm(retVal, cycle[0])
        return retVal

    return numPulsesSentLow*numPulsesSentHigh

with open("inp.txt", "r") as inp:
    data_orig = inp.read().strip().splitlines()
data_orig.append("rx -> broadcaster") #end module for convenience

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
