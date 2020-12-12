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
    inputs.append((line[0], int(line[1:])))
print(inputs)
def part1():
    east = 0
    north = 0
    direction = 0
    #0 = E, 90 = N, 180 = W, 270 = S
    for dir in inputs:
        if(dir[0] == "N"):
            north += dir[1]
        elif(dir[0] == "S"):
            north -= dir[1]
        elif(dir[0] == "W"):
            east -= dir[1]
        elif(dir[0] == "E"):
            east += dir[1]
        elif(dir[0] == "L"):
            direction += dir[1]
            if(direction >= 360):
                direction -= 360
        elif(dir[0] == "R"):
            direction -= dir[1]
            if(direction < 0):
                direction += 360
        elif(dir[0] == "F"):
            if(direction  == 90):
                north += dir[1]
            elif(direction == 270):
                north -= dir[1]
            elif(direction == 180):
                east -= dir[1]
            elif(direction == 0):
                east += dir[1]
    return abs(east) + abs(north)
            
        
        
    
def part2():
    east = 10
    north = 1
    sEast = 0
    sNorth = 0
    #0 = E, 90 = N, 180 = W, 270 = S
    for dir in inputs:
        print(str(sEast) + ", " + str(sNorth) + ", wp: " + str(east) + ", " + str(north))
        if(dir[0] == "N"):
            north += dir[1]
        elif(dir[0] == "S"):
            north -= dir[1]
        elif(dir[0] == "W"):
            east -= dir[1]
        elif(dir[0] == "E"):
            east += dir[1]
        elif(dir[0] == "R"):
            if(dir[1]  == 90):
                oldNorth = north
                north = -1 * east
                east = oldNorth
            elif(dir[1] == 270):
                oldNorth = north
                north = east
                east = -1 * oldNorth
            elif(dir[1] == 180):
                east = -1 * east
                north = -1 * north
            elif(dir[1] == 0):
                continue
        elif(dir[0] == "L"):
            if(dir[1]  == 90):
                oldNorth = north
                north = east
                east = -1 * oldNorth
            elif(dir[1] == 270):
                oldNorth = north
                north = -1 * east
                east = oldNorth
            elif(dir[1] == 180):
                north = -1 * north
                east = -1 * east
            elif(dir[1] == 0):
                continue
        elif(dir[0] == "F"):
            sEast += east * dir[1]
            sNorth += north * dir[1]
        
    
    return abs(sEast) + abs(sNorth)
    
   
print("Part 1 " + str(part1()))
print("Part 2 " + str(part2()))

