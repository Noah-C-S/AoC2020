import os
import sys
import re
import argparse

parser = argparse.ArgumentParser(description='AoC solution')
parser.add_argument('--file', '-f', help='File to run the program on, default input.txt', type = str, default="input.txt")
args = parser.parse_args()

filename = os.path.normpath(os.path.join(os.path.dirname(__file__), args.file))
try:
    inputFile = open(filename)
except FileNotFoundError:
    print("No file found at " + filename)
    sys.exit(1)

inputs = []
for line in inputFile:
    inputs.append(int(line))

gameJolt = max(inputs) + 3
inputs.sort()
inputs.append(gameJolt)
curJolt = 0
num1s = 0
num3s = 0
for jolt in inputs:
    diff = jolt - curJolt
    #print(str(jolt) + " " + str(diff))
    if(diff <= 3):
        if(diff == 1):
            num1s += 1
        elif (diff == 3):
            num3s += 1
        curJolt = jolt
    else:
        print("no solution")

print("nums: " + str(num1s) + " " + str(num3s))
print("part 1 " + str(num1s * num3s))

#BRUTE FORCE (will take like 10 days for an actual puzzle input)
def part2(past, future): 
    #print(str(past) + " | " + str(future))
    curJolt = 0
    if(len(past) > 0):
        curJolt = max(past)
    num = 0
    while len(future) > 0:
        jolt = future.pop(0)
        diff = jolt - curJolt
        if(diff <= 3):
            newPast = past.copy()
            newPast.append(jolt)
            num += part2(newPast, future.copy())
        else:
            break
    if(len(future) == 0 and gameJolt - max(past) <= 3):
        #print(past)
        num += 1
    
    return num
#print(str(part2([0], inputs))) Brute force method. This way is able to output each of the possible routes, but it takes forever

inputs.insert(0, 0) #lol part 2 expects the zero, part 1 doesn't. I'm a mess 

#much better solution
def part2Alt(): 
    numWays = [1] #1 way to get to first element
    for i in range(1, len(inputs)):
        nw = 0
        for j in range(1, 4):
            if (i - j) >= 0: 
                jolt = inputs[i-j]
                diff = inputs[i] - jolt
                #print(str(jolt) + " | " + str(inputs[i]) + " | " + str(diff))
                if(diff <= 3):
                    nw += numWays[i - j]
        #print([inputs[i], nw])
        numWays.append(nw)
    #print(numWays)
    return numWays[len(numWays) -1]
print("part 2: " + str(part2Alt()))
            