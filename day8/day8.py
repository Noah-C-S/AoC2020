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
input = []

for line in inputFile:
    input.append(line)
lastReplaced = -1
def replaceOne():
    global lastReplaced
    global input
    i = lastReplaced
    if(lastReplaced >= 0):
        input[lastReplaced] = input[lastReplaced].replace("nop", "jmp")
    while True:
        i +=1
        #print(input[i])
        #print(input[i].count("jmp"))
        if(input[i].count("jmp") > 0):
            input[i] = input[i].replace("jmp", "nop")
            lastReplaced = i
            break
part1 = True
def goThrough():
    a = 0
    accumulator = 0
    alreadyRun = [False]*len(input)
    #print(input)
    while(a < len(input)):
        line = input[a]
        lineSplit = line.split(" ")
        op = lineSplit[0]
        num = int(lineSplit[1])
        #print(line)
        #print(op + "," + str(num))
        #print(a)
        if(alreadyRun[a]):
            global part1
            if(part1):
                print("Part 1:" + str(accumulator))
                part1 = False
            replaceOne()
            return goThrough()
        alreadyRun[a] = True
        if(op == "nop"):
            a = a + 1
            continue
        elif(op == "acc"):
            accumulator = accumulator + num
            a = a + 1
        elif(op == "jmp"):
            a = a + num
    return accumulator



print("Part 2:" + str(goThrough()))