import os
import sys
import re
import time as timeMod
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
    inputs.append(line)


def part1():
    memory = dict()
    oneMask = 0
    zeroMask = 0b111111111111111111111111111111111111
    for line in inputs:
        els = line.split(" ")
        if els[0] == "mask":
            oneMask = 0
            #zeroMask = 0b111111111111111111111111111111111111
            zeroMask = 0
            for i in range(36):
                if(els[2][i] == "1"):
                    oneMask += 2** (35 - i)
                elif(els[2][i] == "0"):
                    #zeroMask = zeroMask & ~(2** i)
                    zeroMask += 2** (35 - i)
            zeroMask = ~zeroMask
                    
            print(els[2].strip())
            print('{0:036b}'.format(oneMask))
            print('{0:036b}'.format(zeroMask))
            print("_________________________________")
            continue
        addr = int(els[0].strip("mem[").strip("]"))
        val = int(els[2])
        val = val | oneMask
        val = val & zeroMask
        memory[addr] = val
    sum = 0
    for value in memory:
        print(str(value) + ": " + str(memory[value]))
        sum+= memory[value]
    return sum
    
def part2():
    memory = dict()
    oneMask = 0
    xs = []
    for line in inputs:
        els = line.split(" ")
        if els[0] == "mask":
            oneMask = 0
            xs = []
            for i in range(36):
                if(els[2][i] == "1"):
                    oneMask += 2** (35 - i)
                elif(els[2][i] == "X"):
                    xs.append(i)
            #print(els[2].strip())
            #print('{0:036b}'.format(oneMask))
            #print(xs)
            #print("_________________________________")
            continue
        addr = int(els[0].strip("mem[").strip("]"))
        val = int(els[2])
        print(val)
        addr = addr | oneMask
        for i in range(2 ** len(xs)):
            theAddr = addr
            tOneMask = 0
            tZeroMask = 0
            for j in range(len(xs)):
                if(i & (1 << (j))):#Basically if the jth bit of i is zero
                    tZeroMask += 2 ** (35 - xs[j])
                else:
                    tOneMask += 2 ** (35 - xs[j])
            tZeroMask = ~tZeroMask
            theAddr = theAddr | tOneMask
            theAddr = theAddr & tZeroMask
            #print(theVal)
            print('{0:036b}'.format(theAddr) + ", decimal: " + str(theAddr))
            memory[theAddr] = val
           
    theSum = 0
    for value in memory:
        print(str(value) + ": " + str(memory[value]))
        theSum+= memory[value]
    return theSum
    
   
#print("Part 1 " + str(part1()))
print("Part 2 " + str(part2()))

