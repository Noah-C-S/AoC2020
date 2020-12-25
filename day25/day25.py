import os
import sys
import re
import time as timeMod
import argparse
import math
import copy

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
    
inputs = inputFile.read().split("\n")

DIVIDEND = 20201227
SUBNUM = 7
cardKey = int(inputs[0])
doorKey = int(inputs[1])


def log(message):
    if(args.verbose > 0):
        print(message)

def loop(num, subnum):
    val = num * subnum
    val = val % DIVIDEND
    return val

def part1():
    val = 1
    numLoops = 0
    while True:
        val = loop(val, SUBNUM)
        log(val)
        numLoops += 1
        if(val == cardKey):
            break
    log("Num Loops: " + str(numLoops))
    key = 1
    for a in range(numLoops):
        key = loop(key, doorKey)
        log(key)
    return key
        
#There is no part 2
    
    
print("Part 1 " + str(part1()))
#print("Part 2 " + str(part2()))

