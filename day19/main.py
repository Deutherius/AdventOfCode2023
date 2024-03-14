import time
from copy import deepcopy
from math import prod

def parseRule(l:str) -> tuple[str, str]:
    ruleName, rulestr = l.strip().replace("}","").split("{")
    ruleSpaces = rulestr.replace(":", " ").replace(",", " ")
    ruleParts = ruleSpaces.split()
    newRule = ""
    skipNext = False
    for i, part in enumerate(ruleParts):
        if skipNext: 
            skipNext = False
            continue
        if "<" in part or ">" in part:
            #it's a condition
            #next one is destination, the one after that is the else destination
            newRule += "\"" + ruleParts[i+1] + "\" if " + part + " else "
            skipNext = True
        else:
            newRule += "\"" + part + "\""
    return ruleName, newRule

def runItem(item: list[int, int, int, int], rules: dict[str, str]):
    x,m,a,s = item
    nextRule = "in"

    while not nextRule == "A" and not nextRule == "R":
        nextRule = eval(rules[nextRule])
    
    if nextRule == "A":
        return x+m+a+s
    return 0

def parseRule2(l:str, rules: dict[str, list[str, str, str]]) -> dict[str, list[str, str, str]]:
    ruleName, rulestr = l.strip().replace("}","").split("{")
    ruleSpaces = rulestr.replace(":", " ").replace(",", " ")
    ruleParts = ruleSpaces.strip().split()
    if len(ruleParts) == 3:
        #standard rule, parse it
        rules[ruleName] = ruleParts
    else:
        #chained rule
        furtherRule_Name = "_" + ruleName
        rules[ruleName] = ruleParts[:2] + [furtherRule_Name]
        newL = " ".join((furtherRule_Name + "{", *ruleParts[2:]))
        rules = parseRule2(newL, rules)
    return rules

def split_interval(interval: tuple[int, int], N: int, sign: str) -> tuple[int, int]:
    if sign == ">":
        if N < interval[0]:
            return (), interval
        elif N >= interval[1]:
            return interval, ()
        else:
            return (interval[0], N), (N + 1, interval[1])
    elif sign == "<":
        if N > interval[1]:
            return (), interval
        elif N <= interval[0]:
            return interval, ()
        else:
            return (interval[0], N - 1), (N, interval[1])
    else:
        raise ValueError("Invalid sign. Use '<' or '>'.")

def traverseRules(rule:str, rules:dict[str, list[str,str,str]], xmasCube: dict[str, tuple[int, int]]) -> int:
    condition, resPass, resFail = rules[rule]
    var = condition[0]
    sign = condition[1]
    num = int(condition[2:])
    interval = xmasCube[var]
    retVal = 0

    #split interval into two intervals if applicable
    int1, int2 = split_interval(interval, num, sign)
    if sign == ">":
        int1, int2 = int2, int1

    if int1:
        xmasCubelette = deepcopy(xmasCube)
        xmasCubelette[var] = int1
        if resPass == "A":
            retVal += prod([v[1] - v[0] + 1 for v in xmasCubelette.values()])
        elif not resPass == "R":
            retVal += traverseRules(resPass, rules, xmasCubelette)
    if int2:
        xmasCubelette = deepcopy(xmasCube)
        xmasCubelette[var] = int2
        if resFail == "A":
            retVal += prod([v[1] - v[0] + 1 for v in xmasCubelette.values()])
        elif not resFail == "R":
            retVal += traverseRules(resFail, rules, xmasCubelette)
    return retVal

def solve(data_orig: str) -> int:
    parsingRules = True
    rules = {}
    rulesFlat = {}
    items = []
    for line in data_orig:
        l = line.strip()
        if l and parsingRules:
            ruleName, newRule = parseRule(l)
            rules[ruleName] = newRule
            rulesFlat = parseRule2(l, rulesFlat)
        elif l and not parsingRules:
            x,m,a,s = l.replace("{","").replace("}","").replace("x=","").replace("m=","").replace("a=","").replace("s=","").replace(","," ").split()
            items.append((int(x), int(m), int(a), int(s)))
        else:
            parsingRules = False    
    
    #part 1
    aCt = 0
    for item in items:
        aCt += runItem(item, rules)
    #part 2
    aCt2 = 0
    xmasCube = {"x": (1, 4000), "m": (1,4000), "a": (1, 4000), "s": (1, 4000)}
    aCt2 = traverseRules("in", rulesFlat, xmasCube)

    return aCt, aCt2

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
print("Elapsed time for part 1 and 2: " + str(float(then-now)/repeats) + " s average per run")
