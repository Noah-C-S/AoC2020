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

preamble = 25
def part1():
    for a in range(preamble, len(inputs)):
        num = inputs[a]
        valid = False
        for j in range(1, 1 + preamble) :
            for k in range(j + 1, 1 + preamble):
                first = inputs[a - j]
                second = inputs[a - k]
                if(first + second == num and first != second):
                    #print(str(num) + " = " + str(first) + " + " + str(second))
                    valid = True
        if(not valid):
            return num
                        
#print(part1())
search = part1()        
print("Part 1: " + str(search))

def part2(num):
    for a in range(len(inputs) - num):
        therange = []
        for b in range(num) :
            therange.append(inputs[a + b])
        if(sum(therange) == search):
            return min(therange) + max(therange)
    return -1

val = -1
nums = 2
while val < 0:
    val = part2(nums)
    nums += 1
print("Part 2: " + str(val))

        