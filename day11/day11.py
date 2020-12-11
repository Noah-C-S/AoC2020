import os
import sys
import re
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
for line in inputFile:
    inputs.append(line)

def printSeats(seats):
    if(args.verbose == 0):
        return
    for r in seats:
        print(r.strip())
    print("\n__________________\n")

def doIteration(seats):
    mSeats = seats.copy()
    for r in range(len(seats)):
        for c in range(len(seats[r])):
            if(seats[r][c] not in ["L", "#"]):
                continue
            numAdj = 0
            #print("(" + str(r) + ", " + str(c)+ ")")
            for i in range(-1, 2):
                for j in range(-1, 2):
                    
                    if(i == 0 and j == 0 or (r + i) < 0 or (c + j) < 0): 
                        continue
                    try:
                        adj = seats[r + i][c + j] 
                        #print(adj)
                    except IndexError:
                        continue
                    else:
                        if(adj == "#"):
                            numAdj += 1
            #print(numAdj)
            if(numAdj == 0):
                mSeats[r] = mSeats[r][:c] + "#" + mSeats[r][c + 1:]
            elif(numAdj >= 4):
                mSeats[r] = mSeats[r][:c] + "L" + mSeats[r][c + 1:]
    return mSeats

def getNumOccupied(seats):
    numOcc = 0
    for r in seats:
        for c in r:
            if(c == "#"):
                numOcc += 1
    return numOcc

def part1():
    lastOccupied = 0
    lastSeats = inputs
    printSeats(inputs)
    while True:
        nextSeats = doIteration(lastSeats)
        printSeats(nextSeats)
        nextOccupied = getNumOccupied(nextSeats)
        if(nextOccupied == lastOccupied):
            return nextOccupied
        lastSeats = nextSeats
        lastOccupied = nextOccupied

def doIteration2(seats):
    mSeats = seats.copy()
    for r in range(len(seats)):
        for c in range(len(seats[r])):
            if(seats[r][c] not in ["L", "#"]):
                continue
            numSeen = 0
            #print("(" + str(r) + ", " + str(c)+ ")")
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if(i == 0 and j == 0):
                        continue
                    k = r
                    l = c
                    while True:
                        k += i
                        l += j
                        if(k < 0 or l < 0):
                            break
                        try:
                            seen = seats[k][l] 
                        except IndexError:
                            break
                        else:
                            if(seen == "#"):
                                numSeen += 1
                                break
                            elif(seen == "L"):
                                break
            if(numSeen == 0):
                mSeats[r] = mSeats[r][:c] + "#" + mSeats[r][c + 1:]
            elif(numSeen >= 5):
                mSeats[r] = mSeats[r][:c] + "L" + mSeats[r][c + 1:]
    return mSeats

def part2():
    lastOccupied = 0
    lastSeats = inputs
    printSeats(inputs)
    while True:
        nextSeats = doIteration2(lastSeats)
        printSeats(nextSeats)
        nextOccupied = getNumOccupied(nextSeats)
        if(nextOccupied == lastOccupied):
            return nextOccupied
        lastSeats = nextSeats
        lastOccupied = nextOccupied

   
print("Part 1 " + str(part1()))
print("Part 2 " + str(part2()))

