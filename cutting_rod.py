#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'maxProfit' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER costPerCut
#  2. INTEGER salePrice
#  3. INTEGER_ARRAY lengths
#

def maxProfit(costPerCut, salePrice, lengths):
    totalProfit = 0
    for saleLength in range(1, max(lengths) + 1):
        
        #total num of sellable rods
        totalUniformRods = sum([l // saleLength for l in lengths])

        #total num of cuts needed 
        total_Cuts = sum([max(0, l // saleLength - int(l % saleLength == 0)) for l in lengths])

        #disregard if cutting costs more than it brings back
        curr_profit = totalUniformRods * saleLength * salePrice - total_Cuts * costPerCut

        totalProfit = max(totalProfit, curr_profit)

    return totalProfit

def maxProfit2(costPerCut, salePrice, lengths):
    maxProfit = 0

    for saleLength in range(1, max(lengths) + 1):
        currProfit = 0

        for rod_length in lengths:
            uniform_rods = rod_length // saleLength
 
            if uniform_rods > 0:
                total_cuts = uniform_rods - int(rod_length % saleLength == 0)

                total_cut_cost = total_cuts * costPerCut
                revenues = uniform_rods * salePrice * saleLength

                if revenues > total_cut_cost:
                    currProfit += revenues - total_cut_cost

        if currProfit > maxProfit:
            maxProfit = currProfit

    return maxProfit

if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')

    #costPerCut = int(input().strip())

    #salePrice = int(input().strip())

    #lengths_count = int(input().strip())

    #  for _ in range(lengths_count):
    #     lengths_item = int(input().strip())
    #     lengths.append(lengths_item)
    costPerCut = 1000
    salePrice = 1
    
    lengths = [200,200,200,400,200,200,200,200,200,200,200]

    result = maxProfit2(costPerCut, salePrice, lengths)

    kiki=0
    #fptr.write(str(result) + '\n')

    #fptr.close()
