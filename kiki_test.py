# Dynamic Programming Python implementation of Coin
# Change problem

from collections import deque
from itertools import cycle
import math

def count(Step_size, step_num, n):
 
    # table[i] will be storing the number of solutions for
    # value i. We need n+1 rows as the table is constructed
    # in bottom up manner using the base case (n = 0)
    # Initialize all table values as 0
    table = [0 for k in range(n+1)]
 
    # Base case (If given value is 0)
    table[0] = 1
 
    # Pick all coins one by one and update the table[] values
    # after the index greater than or equal to the value of the
    # picked coin
    all_comb = [[1]*n]
    cur_com = []
    for i in range(0,step_num):
        for j in range(Step_size[i],n+1):
            cur_step_size = Step_size[i]
            table[j] += table[j-cur_step_size]

            # #get the list of comb
            # if cur_step_size != Step_size[0]:
            #     if j == Step_size[i]:
            #         cur_com.append(Step_size[i])
            #     if table[j] == table[j-1]:
            #         cur_com.append(Step_size)
 
    return table[n]
 
def maxResult(nums: list[int], k: int) -> int:
        n = len(nums)
        deq = deque([n-1])
        #to start at second to last element
        for i in range(n-2, -1, -1):
            
            #check if we leave our outer step size limit looking  
            if deq[0] - i > k: 
                 deq.popleft()
            nums[i] += nums[deq[0]]
            #if there is an index in deq and the if the sum of nums of last step is lower than nums new step disregard that index 
            while len(deq) and nums[deq[-1]] <= nums[i]: 
                 deq.pop()
            deq.append(i)
        return nums[0]

def maxResult(nums: list[int], k: list) -> int:
        n = len(nums)
        deq = deque([n-1])
        #to start at second to last element
        index = n-2

        while index != 0:
            #check if we leave our outer step size limit looking  
            if deq[0] - i > k: 
                 deq.popleft()
            nums[i] += nums[deq[0]]
            #if there is an index in deq and the if the sum of nums of last step is lower than nums new step disregard that index 
            while len(deq) and nums[deq[-1]] <= nums[i]: 
                 deq.pop()
            deq.append(i)
        return nums[0]

#stepsize list

def fancy_range(start, stop, steps=(1,)):
    #substract step sizes to account for deduction of previous step sizes
    first_step = steps[0]
    steps = [y - x for x,y in zip(steps,steps[1:])]

    steps.insert(0,first_step)
    steps = cycle(steps)
    val = start
    while val > stop:
        yield val
        step = next(steps)
        while val+step < 0:
             step = next(steps)
        val += step

#copy

def maxResult2(nums: list[int], k: list) -> int:
        n = len(nums)
        deq = deque([n-1])
        # disregard the first value that is the end of the queue 
        loop_range = list(fancy_range(n-1, -1, k))[1:]
        print(loop_range)
        #to start at second to last element
        for i in range(n-2, -1, -1):
            
            #check if we leave our outer step size limit looking  
            if deq[0] - i > k[-1]: 
                 deq.popleft()
            nums[i] += nums[deq[0]]
            #if there is an index in deq and the if the sum of nums of last step is lower than nums new step disregard that index 
            while len(deq) and nums[deq[-1]] <= nums[i]: 
                 deq.pop()
            deq.append(i)
        return nums[0]

#See if a number is prime
def is_prime(n:int):
    
    for i in range(2,int(math.sqrt(n))+1):
        if (n%i) == 0:
            return False
    return True
    
#get a list of possible jumping steps
def get_jumps(n):
    ending_three = [v for v in range(n) if v%10 == 3]
    possiple_jumps = [p for p in ending_three if is_prime(p)==True]
    
    return possiple_jumps

# gives back indices of possible paths taken
def create_paths(start:int, steps:list)->list:
    all_paths = []
    
    temp = deque([[[start]]])
    
    # tree structure, start with the end and add indices possible step to create branches 
    while bool(temp[0]):
         
        new_branches = []
        for step in steps:
            #loop through nodes
            for i in temp[0]:
                new_item = i[-1] - step
                sub_branch =[*i, new_item]

                # if end is reached or steps are bigger than the smallest possible prime
                # only steps of 1 are allowed, add those right away
                if new_item==0:
                    all_paths.append(sub_branch)
                    continue
                elif new_item < steps[1]: 
                     sub_branch.extend(range(new_item-1,-1,-1))
                     all_paths.append(sub_branch)
                     continue

                new_branches.append(sub_branch)

        temp.append(new_branches)
        temp.popleft()

    return all_paths 

cell_test = [1, 3, 13, 23, 43, 53, 73, 83, 103, 113, 163, 173, 193, 223, 233, 263, 283, 293, 313, 353, 373, 383, 433, 443, 463, 503, 523, 563, 593, 613, 643, 653, 673, 683, 733, 743, 773, 823, 853, 863, 883, 953, 983, 1013, 1033, 1063, 1093, 1103, 1123, 1153, 1163, 1193, 1213, 1223, 1283, 1303, 1373, 1423, 1433, 1453, 1483, 1493, 1523, 1543, 1553, 1583, 1613, 1663, 1693, 1723, 1733, 1753, 1783, 1823, 1873, 1913, 1933, 1973, 1993, 2003, 2053, 2063, 2083, 2113, 2143, 2153, 2203, 2213, 2243, 2273, 2293, 2333, 2383, 2393, 2423, 2473, 2503, 2543, 2593, 2633, 2663, 2683, 2693, 2713, 2753, 2803, 2833, 2843, 2903, 2953, 2963, 3023, 3083, 3163, 3203, 3253, 3313, 3323, 3343, 3373, 3413, 3433, 3463, 3533, 3583, 3593, 3613, 3623, 3643, 3673, 3733, 3793, 3803, 3823, 3833, 3853, 3863, 3923, 3943, 4003, 4013, 4073, 4093, 4133, 4153, 4243, 4253, 4273, 4283, 4363, 4373, 4423, 4463, 4483, 4493, 4513, 4523, 4583, 4603, 4643, 4663, 4673, 4703, 4723, 4733, 4783, 4793, 4813, 4903, 4933, 4943, 4973, 4993, 5003, 5023, 5113, 5153, 5233, 5273, 5303, 5323, 5333, 5393, 5413, 5443, 5483, 5503, 5563, 5573, 5623, 5653, 5683, 5693, 5743, 5783, 5813, 5843, 5903, 5923, 5953, 6043, 6053, 6073, 6113, 6133, 6143, 6163, 6173, 6203, 6263, 6323, 6343, 6353, 6373, 6473, 6553, 6563, 6653, 6673, 6703, 6733, 6763, 6793, 6803, 6823, 6833, 6863, 6883, 6983, 7013, 7043, 7103, 7193, 7213, 7243, 7253, 7283, 7333, 7393, 7433, 7523, 7573, 7583, 7603, 7643, 7673, 7703, 7723, 7753, 7793, 7823, 7853, 7873, 7883, 7933, 7963, 7993, 8053, 8093, 8123, 8233, 8243, 8263, 8273, 8293, 8353, 8363, 8423, 8443, 8513, 8543, 8563, 8573, 8623, 8663, 8693, 8713, 8753, 8783, 8803, 8863, 8893, 8923, 8933, 8963, 9013, 9043, 9103, 9133, 9173, 9203, 9283, 9293, 9323, 9343, 9403, 9413, 9433, 9463, 9473, 9533, 9613, 9623, 9643, 9733, 9743, 9803, 9833, 9883, 9923, 9973]

n = len(cell_test)

ok_jumps = get_jumps(n)
ok_jumps.insert(0,1)

result = create_paths(n,[1,3])

cell = [0,-4,-20,90,-80,100,10]
k=[1,3]
k = [a*-1 for a in k]
#print(maxResult2(cell, k))
print(maxResult(cell, 3))


## Driver program to test above function
# arr = [1,2,5]
# m = len(arr)
# n = 10
# x = count(arr, m, n)
# print (x)
 
