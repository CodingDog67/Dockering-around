# Dynamic Programming Python implementation of Coin
# Change problem

import math
from collections import deque
from itertools import cycle

import numpy as np

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

def allmax(a):
    if len(a) == 0:
        return []
    all_ = [0]
    max_ = a[0]
    for i in range(1, len(a)):
        if a[i] > max_:
            all_ = [i]
            max_ = a[i]
        elif a[i] == max_:
            all_.append(i)
    return all_

def allmin(a):
    if len(a) == 0:
        return []
    all_ = [0]
    max_ = a[0]
    for i in range(1, len(a)):
        if a[i] < max_:
            all_ = [i]
            max_ = a[i]
        elif a[i] == max_:
            all_.append(i)
    return all_

def maxResult_final(nums: list[int], steps: list) -> int:
    best_index = deque([len(nums)-1]) # starting at the end
    cur_index = best_index[0]
    best_value = nums[-1]
    
    while cur_index !=0:
        temp_max_vals = []
        temp_max_idx = []
        
        #update numbers for possible steps taken
        for step in steps:
            
            cur_index = best_index[0] - step
            temp_max_vals.append(nums[best_index[0]]+nums[cur_index]) #+ future step
            temp_max_idx.append(cur_index)

        if len(temp_max_idx) ==1:
            temp_max_vals = temp_max_vals[0]
            temp_max_idx = temp_max_idx[0]

        range_big = 0
        range_small = 0
        #check if num[step] > num[step_smaller] + num[step]
        for i in range(1, len(steps)):
            #reached the end
            start_big_idx = best_index[0] - steps[i]
            start_small_idx = best_index[0] -steps[i-1]
            start_big = nums[start_big_idx]
            start_small = nums[start_small_idx]

            if start_big_idx != 0:
                range_big = max(nums[max(0, start_big_idx-steps[-1]):start_big_idx])
            if start_small_idx != 0:
                range_small = max(nums[max(0, start_small_idx-steps[-1]):start_small_idx])

            if (start_big + range_big) < (start_small + range_small):
                temp_max_vals = temp_max_vals[i-1]
                temp_max_idx = temp_max_idx[i-1]
                break
            else:
                temp_max_vals = temp_max_vals[i]
                temp_max_idx = temp_max_idx[i]


        best_index.append(temp_max_idx)
        # #get all global maxima
        # temp_max = allmax(temp_max_vals)

        # if len(temp_max) == 1:
        #     temp_max_idx = temp_max_idx[temp_max[0]]
        #     temp_max_vals = temp_max_vals[temp_max[0]]
        #     best_index.append(temp_max_idx)

        # #more than one max or min, if-else to treat case of two identical max_values
        # else:    
        #     if temp_max_vals[0] >0:
        #         # if best value pos take smallest step to maximize gain
        #         best_index.append(max([temp_max_idx[i] for i in temp_max]))
        #     else:
        #         # if best value neg take largest step
        #         best_index.append(min([temp_max_idx[i] for i in temp_max]))
        
        #update to reflect taken step, consider corner case that even though prime jump is better than move 1
        #sum of move 1 to prime is the worth more
        # inspect_range = nums[best_index[-1]+1:best_index[0]]
        # sum_inspect = sum(inspect_range)
        # if inspect_range and sum_inspect >0:
        #         nums[best_index[-1]] = nums[best_index[0]] + nums[best_index[-1]] + sum_inspect
        # else:
        #     nums[best_index[-1]] = nums[best_index[0]] + nums[best_index[-1]]

        nums[best_index[-1]] = nums[best_index[0]] + nums[best_index[-1]]

        cur_index = best_index[-1]   
        best_value = nums[best_index[-1]]
        steps = [x for x in steps if x <= best_index[-1]]
        
        best_index.popleft()
     
    return best_value

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

#cell = [0, -6, 8, 70, -500, 4, 100, 80, 200, -600, 50]  #302 result
#cell = [0, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 10] #1210 result
#cell = [0, -1, -1, -1, -1, -1] #-3
cell = [0, 60, 50, 64, 5, -28, 79, 8, 9, 57] #result 327
#cell = [0, -472, 475, -160, 21, -6] # result 3
#cell = [0,5,3,8,9,-5,-9,-10,-8,-6,-30] #result -15
#cell = [0,-100,-100,-1,0,-1] #-2
#cell = [0, 90, 6, 5, -6, 2, 9, 2] #result 112
#cell = [0, 5000, 3, 8]
#cell = [0, -5, -9, -10, -8, -6, -20] #result 30


n = len(cell)

ok_jumps = get_jumps(n)
ok_jumps.insert(0,1)

#result = create_paths(n,[1,3])
result = maxResult_final(cell, ok_jumps)
result2 = maxResult(cell, ok_jumps[-1])
cell = [0,-4,-20,90,-80,100,10]

ok_jumps = [a*-1 for a in ok_jumps]
print(maxResult2(cell, ok_jumps))



## Driver program to test above function
# arr = [1,2,5]
# m = len(arr)
# n = 10
# x = count(arr, m, n)
# print (x)
 
