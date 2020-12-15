import os
import sys
import re
import time as timeMod
import argparse

parser = argparse.ArgumentParser(description='AoC solution')
parser.add_argument('--file', '-f', help='File to run the program on, default input.txt', type = str, default="input.txt")
parser.add_argument('--verbose', '-v', help = "0 if you want it to be silent, 1 if you want output, default 0", type = int, default = 0)
args = parser.parse_args()

filename = os.path.normpath(os.path.join(os.path.dirname(__file__), args.file))
try:
    inputFile = open(filename)
except FileNotFoundError:
    print("No file found at " + filename)
    sys.exit(1)
inputs = []
for num in inputFile.read().split(","):
    inputs.append(int(num))


def part1():
    allSpoken = []
    for num in inputs:
        allSpoken.insert(0, num)
    for a in range(len(inputs), 2020):
        lastSpoken = allSpoken[0]
        if(args.verbose > 0):
            print(str(allSpoken))
            print("LastSpoken, a: " + str(lastSpoken) + ", " + str(a))
        try:
            lastTimeSpoken = len(allSpoken) - allSpoken.index(lastSpoken, 1, len(allSpoken) + 1) 
            if(args.verbose > 0):
                print(str(lastTimeSpoken))
        except ValueError:
            allSpoken.insert(0, 0)
            if(args.verbose > 0):
                print("first")
        else:
            allSpoken.insert(0, a - lastTimeSpoken)
    return allSpoken[0]

def part2():
    previous = 0
    lastSpoken = dict()
    for i in range(len(inputs)):
        lastSpoken[inputs[i]] = i
        previous = inputs[i]
    for a in range(len(inputs), 30000000):
        lastTimeSpoken = lastSpoken.get(previous, -1)
        lastSpoken[previous] = a - 1
        if(args.verbose > 0):
           print(str(previous) + ", " + str(lastTimeSpoken)+ ", "  + str(a))
        if(lastTimeSpoken == -1):
            previous = 0
        else:
            previous = a - lastTimeSpoken - 1
    return previous
    
    
   
print("Part 1 " + str(part1()))
print("Part 2 " + str(part2()))

