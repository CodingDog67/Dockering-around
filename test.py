#!/bin/python3

import math
import os
import random
import re
import sys
import copy
from itertools import accumulate
from collections import deque

#
# Complete the 'maxGameScore' function below.
#
# The function is expected to return an INTEGER.
# The function accepts INTEGER_ARRAY cell as parameter.
#

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

def find_pathways(len_array:int, jumps:list[int]):
    #stop conditions
    if len_array < 0:
        return []
    if len_array == 0:
            return [[]]
    
    all_jump_combos = []

    for last_used_jump in jumps:
        combos = find_pathways(len_array - last_used_jump, jumps)
        for combo in combos:
            combo.append(last_used_jump)
            all_jump_combos.append(combo)

    return all_jump_combos

def maxGameScore(cell:list[int])->int:
    # Write your code here
    max_points = None
    n = len(cell)
    ok_jumps = get_jumps(n)
    ok_jumps.insert(0,1)
    print(ok_jumps)
   
    all_paths = find_pathways(n-1, ok_jumps)
           
    for path in all_paths:
        path_indices = list(accumulate(path))
        temp_values = [cell[i] for i in path_indices]            
        path_max = sum(temp_values)
        if max_points == None or path_max > max_points:
            max_points = path_max     
                
            
    return max_points

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    cell_count = int(input().strip())
    
    cell = []
    
    for _ in range(cell_count):
        cell_item = int(input().strip())
        cell.append(cell_item)
    
   
    result = maxGameScore(cell)

    fptr.write(str(result) + '\n')

    fptr.close()


##Slow solution to hackerrank pawn jump 