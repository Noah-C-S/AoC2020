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
    
#inputs = inputFile.read().split("\n")

def log(message):
    if(args.verbose > 0):
        print(message)

tiles = []
for line in inputFile:
    tiles.append(line.strip())
    
black_tiles = dict() # Just store a list of black tiles
#x,y. s = y-1, n = y + 1, e = x - 1, w =  + 1, idk if it's necessary to worry about delimittiers?


def calculateCoord(tile):
    x = 0
    y = 0
    prev = ""
    for char in tile:
        if(char == "s"):
            prev = "s"
        elif (char == "n"):
            prev = "n"
        elif (char == "e"):
            if(prev == ""):
                x += 1
            elif(prev == "s"):
                x += 1
                y -= 1
            elif(prev == "n"):
                y += 1
            prev = ""
        elif (char == "w"):
            if(prev == ""):
                x -= 1
            elif(prev == "n"):
                x -= 1
                y += 1
            elif (prev == "s"):
                y -= 1
            prev = ""
                
    return (x, y)


def tileBlack(loc):
    return black_tiles.get(loc, False)

def flipTileAt(loc):
    global black_tiles
    if(black_tiles.get(loc, False)):
        black_tiles.pop(loc)
    else:
        black_tiles[loc] = True

def part1():
    global black_tiles
    for tile in tiles:
        loc = calculateCoord(tile)
        flipTileAt(loc)
        log(loc)
    return len(black_tiles)

def getAdjacent(loc):
    adj = []
    x = loc[0]
    y = loc[1]
    adj.append((x + 1, y))
    adj.append((x - 1, y))
    adj.append((x -1, y + 1))
    adj.append((x, y + 1))
    adj.append((x, y - 1))
    adj.append((x + 1, y -1))
    return adj

def processTiles():
    toProcess = dict()
    for bt in black_tiles:
        if(not toProcess.get(bt, False)):
            toProcess[bt] = True
        for adj in getAdjacent(bt):
            if(not toProcess.get(adj, False)):
                toProcess[adj] = True
    toFlip = dict()
    for processLoc in toProcess:
        blackAtLoc = tileBlack(processLoc)
        numBlack = 0
        for adj in getAdjacent(processLoc):
            if(tileBlack(adj)):
                numBlack += 1
        if(blackAtLoc):
            if(numBlack == 0 or numBlack > 2):
                toFlip[processLoc] = True
        else:
            if(numBlack == 2):
                toFlip[processLoc] = True
    
    for flip in toFlip:
        flipTileAt(flip)

def getNumBlack():
    return len(black_tiles)


def part2():
    for i in range(100):
        processTiles()
        log(i)
        log(getNumBlack())
    return getNumBlack()
print("Part 1 " + str(part1()))
print("Part 2 " + str(part2()))

