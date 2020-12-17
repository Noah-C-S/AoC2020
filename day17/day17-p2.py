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


def printDimension():
    for w in range(len(p_dimension)):
        print("w = : " + str(w))
        for z in range(len(p_dimension[w])):
            print("z = " + str(z - len(p_dimension[w])//2 ) + ", w = " + str(w - len(p_dimension)//2 ))
            for y in range(len(p_dimension[w][z])):
                print(p_dimension[w][z][y])
        print("")
        
    print("__________________________")


lines = inputFile.read().split("\n")

#ughhh for some reason that I ABSOLUTELY can NOT figure out, expandAllByOne is expanding *SOME* rows at different rates than *OTHERS*. SO BIG FIXED SIZE DIMENSION I GUESS
size = 30
middle = (size -2) //2
print(middle)

p_dimension = [[[["." for x in range(size) ] for y in range(size)] for z in range(size)] for w in range(size)]
#printDimension()
for i in range(len(lines)):
    line = lines[i]
    p_dimension[middle][middle][middle + i] = list(("." * ((size - len(line))//2)) + line.strip() + ("." * ((size - len(line))//2 +((size + len(line)) % 2))))

printDimension()
def expandAllByOne(p_dim):
    pock_dim = copy.deepcopy(p_dim)
    for i in range(len(pock_dim)):
        #expand x by adding . to the start and end of each line
        for j in range(len(pock_dim[i])):
            for k in range(len(pock_dim[i][j])):
                #print(pock_dim[i][j][k])
                pock_dim[i][j][k] = "." + pock_dim[i][j][k] + "."

            #print(pock_dim[i][j])
        #expand y by adding a bunch of .s to the top and bottom of each plane
            pock_dim[i][j].insert(0, "." * len(pock_dim[i][j][-1]))
            pock_dim[i][j].append("." * len(pock_dim[i][j][-1]))

        #add new z values by adding a plane of . to the front and back of the whole dimension
        pock_dim[i].insert(0, ["." * len(pock_dim[i][-1][-1])] * len(pock_dim[i][-1]))
        pock_dim[i].append(["." * len(pock_dim[i][-1][-1])] * len(pock_dim[i][-1]))
    #add new w values by adding a whole new 3d dimension to the w- and w+ of this one
    #print(str(len(pock_dim[0][0][0])) + "," + str(len(pock_dim[0][0])) + "," + str(len(pock_dim[0])))
    """new_dim = [["." * 10] * 10] * 10
    new_dim = [["." * len(pock_dim[0][0][0])] * len(pock_dim[0][0])] * len(pock_dim[0])
    for plane in new_dim:
        for row in plane:
            print(row)
        print("______________")
    print("VVVVVVVVVVVVVVVVVVVVVVVVVV")"""
    pock_dim.insert(0, [["." * len(pock_dim[0][0][0])] * len(pock_dim[0][0])] * len(pock_dim[0]))
    pock_dim.append([["." * len(pock_dim[0][0][0])] * len(pock_dim[0][0])] * len(pock_dim[0]))
    return pock_dim

def countCubes():
    count = 0
    for threeDspace in p_dimension:
        for plane in threeDspace:
            for row in plane:
                count += row.count("#")
    return count




def getActiveNeighbors(reference, x, y, z, w):
    numActive = 0
    checked = []
    for i in range (-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                for l in range(-1, 2):
                    if( (i == 0 and j == 0 and k == 0 and l == 0) or ((w + i) < 0 or (z + j) < 0 or (y + k) < 0 or (x + l) < 0 )):
                        continue
                    checked.append([x + l,y + k,z + j,w + i])
                    try:
                        adj = reference[w + i][z + j][y + k][x + l]
                    except IndexError:
                        continue
                    else:
                        if(adj == "#"):
                            numActive += 1
    #print(str(x) + ',' + str(y) + ',' + str(z) + ',' + str(w))
    #print(checked)
    #print(numActive)
    #print("_______")
    return numActive
                

def runCycle():
    global p_dimension
    #e_dim = expandAllByOne(p_dimension)
    e_dim = copy.deepcopy(p_dimension)
    reference_dim = copy.deepcopy(e_dim)
    for w in range(len(e_dim)):
        for z in range(len(e_dim[w])):
            for y in range(len(e_dim[w][z])):
                for x in range(len(e_dim[w][z][y])):
                    numActive = getActiveNeighbors(reference_dim, x, y, z, w)
                    thisOne = e_dim[w][z][y][x]
                    if(thisOne == "#"):
                        if(numActive != 2 and numActive != 3):
                            #e_dim[w][z][y] = e_dim[w][z][y][:x] + "." + e_dim[w][z][y][x + 1:]
                            e_dim[w][z][y][x] = "."
                    else:
                        if(numActive == 3):
                            #e_dim[w][z][y] = e_dim[w][z][y][:x] + "#" + e_dim[w][z][y][x + 1:]
                            e_dim[w][z][y][x] = "#"
    p_dimension = e_dim
    #print(e_dim)
    printDimension()
    

def part2():
    printDimension()
    for i in range(6):
        runCycle()
    return countCubes()


  
    
    
   
#print("Part 1 " + str(part1()))
print("Part 2 " + str(part2()))

