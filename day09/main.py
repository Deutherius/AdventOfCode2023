import time

def solve(data_orig):
    nums = []
    total = 0
    total2 = 0
    for index, line in enumerate(data_orig):
        nums.append([[int(a) for a in line.strip().split()]])
        # print(nums)
        index2 = 0    
        while True:
            nums[index].append([j-i for i, j in zip(nums[index][index2][:-1], nums[index][index2][1:])])
            index2 += 1
            if all((a == 0 for a in nums[index][index2])):
                break
    #now go in reverse, appending the correct digit to each subarray and add all main array last digits
    for index, cluster in enumerate(nums):
        for index2, _ in reversed(list(enumerate(cluster[:-1]))):
            nums[index][index2].append(cluster[index2][-1] + cluster[index2+1][-1]) #future
            nums[index][index2].insert(0, cluster[index2][0] - cluster[index2+1][0]) #past
        total += nums[index][index2][-1]
        total2 += nums[index][index2][0]
    
    return total, total2

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
print("Elapsed time for both parts: " + str(float(then-now)/repeats) + " s average per run")
