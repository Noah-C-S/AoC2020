import os
import sys
import re
import time as timeMod
import argparse
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

p_dimension = []
p_dimension.append([])
for line in inputFile:
    p_dimension[0].append(line.strip())

def expandAllByOne(p_dim):
    #add new x & y values
    pock_dim = copy.deepcopy(p_dim)
    for i in range(len(pock_dim)):
        #expand x by adding . to the start and end of each line
        for j in range(len(pock_dim[i])):
            #print("VVVVVVVVVVVVVV")
            #print(pock_dim[i][j])
            pock_dim[i][j] = "." + pock_dim[i][j] + "."
            #print(pock_dim[i][j])
        #expand y by adding a bunch of .s to the top and bottom of each plane
        pock_dim[i].insert(0, "." * len(pock_dim[i][0]))
        pock_dim[i].append("." * len(pock_dim[i][0]))

    #add new z values by adding a plane of . to the front and back of the whole dimension
    pock_dim.insert(0, ["." * len(pock_dim[0][0])] * len(pock_dim[0]))
    pock_dim.append(["." * len(pock_dim[0][0])] * len(pock_dim[0]))
    return pock_dim

def countCubes():
    count = 0
    for plane in p_dimension:
        for row in plane:
            count += row.count("#")
    return count

def printDimension():
    for plane in p_dimension:
        for row in plane:
            print(row)
        print("______________")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")


def getActiveNeighbors(reference, x, y, z):
    numActive = 0
    for i in range (-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                if( (i == 0 and j == 0 and k == 0) or ((z + i) < 0 or (y + j) < 0 or (x + k) < 0)):
                    continue
                try:
                    adj = reference[z + i][y + j][x + k]
                except IndexError:
                    continue
                else:
                    if(adj == "#"):
                        numActive += 1
    #print(numActive)
    return numActive
                

def runCycle():
    global p_dimension
    e_dim = expandAllByOne(p_dimension)
    reference_dim = copy.deepcopy(e_dim)
    for z in range(len(e_dim)):
        for y in range(len(e_dim[z])):
            for x in range(len(e_dim[z][y])):
                numActive = getActiveNeighbors(reference_dim, x, y, z)
                thisOne = e_dim[z][y][x]
                if(thisOne == "#"):
                    if(numActive != 2 and numActive != 3):
                        e_dim[z][y] = e_dim[z][y][:x] + "." + e_dim[z][y][x + 1:]
                else:
                    if(numActive == 3):
                        e_dim[z][y] = e_dim[z][y][:x] + "#" + e_dim[z][y][x + 1:]
    p_dimension = e_dim
    printDimension()
    

def part1():
    printDimension()
    for i in range(6):
        runCycle()
    return countCubes()

#def part2():

  
    
    
   
print("Part 1 " + str(part1()))
#print("Part 2 " + str(part2()))

