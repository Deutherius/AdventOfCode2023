import time

def solve(data_orig):
    total = total2 = 0
    for line in data_orig:
        nums = [[int(a) for a in line.strip().split()]]
        i = 0 
        while any(nums[i]):
            nums.append([j-i for i, j in zip(nums[i][:-1], nums[i][1:])])
            i += 1
        startDigit = 0
        endDigit = 0
        for c in reversed(nums[:-1]):
            endDigit += c[-1]
            startDigit = c[0] - startDigit
        total += endDigit
        total2 += startDigit
    return total, total2

# with open("inp_ex.txt", "r") as inp:
with open("inp.txt", "r") as inp:
    data_orig = inp.readlines()
data_orig = data_orig * 1
repeats = 1
now = time.time()
for _ in range(0,repeats):
    if repeats > 1:
        _ = solve(data_orig=data_orig)
    else:
        print(solve(data_orig=data_orig))
then = time.time()
print("Elapsed time for both parts: " + str(float(then-now)/repeats) + " s average per run")
