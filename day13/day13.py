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

file = inputFile.read()
lines = file.split("\n")
time = int(lines[0])
rawIds = lines[1].split(",")

print(time)
print(rawIds)
def part1():
    ids = []
    for id in rawIds:
        if(id == "x"):
            continue
        ids.append(int(id))
    minId = 10000000000000
    theId = 0
    for id in ids:
        sum = id
        while(sum < time):
            sum += id
        if(sum < minId):
            minId = sum
            theId = id
    print(minId)
    return (minId - time) * theId
"""
num = 100000000000000
while True:
    if num % 983 == 0:
        print(num - 17)
        break
    num += 1
   """ 
def part2():
    timestamps = []
    for i in range(len(rawIds)):
        if(rawIds[i] == "x"):
            continue
        timestamps.append((int(rawIds[i]), i))
    firstVar = "(define ns '("
    secondVar = "(define as '("
    for timestamp in timestamps:
        firstVar = firstVar + " " + str(timestamp[0])
    for timestamp in timestamps:
        secondVar = secondVar + " " + str(timestamp[0] - timestamp[1])
    print("Paste the following two lines into the top of solver.rkt")
    print(firstVar + "))")
    print(secondVar + "))")
    print("attempting brute force...")
    maxLoc = 0
    maxVal = 0 
    for t in range(len(timestamps)):
        if(timestamps[t][0] > maxVal):
            maxLoc = timestamps[t][1]
            maxVal = timestamps[t][0]
    current = maxVal - maxLoc
    #current = 100007578419274
    while True:
        #start = timeMod.perf_counter()
        for i in range(len(timestamps)):
            if((current + timestamps[i][1]) % timestamps[i][0] != 0):
                #print((current + i) / timestamps[i])
                break
            if(i >= len(timestamps) -1):
                return current
        #print(str(maxVal) + "/" + str(timeMod.perf_counter() - start))
        current += maxVal
        #print(current)

    
   
print("Part 1 " + str(part1()))
print("Part 2 " + str(part2()))

