import os
import sys
import re
import time as timeMod
import argparse
import math
import copy

parser = argparse.ArgumentParser(description='AoC solution')
parser.add_argument('--file', '-f', help='File to run the program on, default input.txt', type = str, default="monster.txt")
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
    if(args.verbose >= 0):
        print(message)

monsterImage = inputFile.read().split("\n")

monsterArr = []
for i in range(len(monsterImage)):
    for j in range(len(monsterImage[i])):
        if(monsterImage[i][j] == "#"):
            monsterArr.append([i -1, j])
print(monsterArr)

