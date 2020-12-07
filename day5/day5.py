import os
import sys
import re
import argparse

parser = argparse.ArgumentParser(description='CNAME cloak detector')
parser.add_argument('--file', '-f', help='File to run the program on, default input.txt', type = str, default="input.txt")
args = parser.parse_args()

filename = os.path.normpath(os.path.join(os.path.dirname(__file__), args.file))
inputs = []
try:
    inputFile = open(filename)
except FileNotFoundError:
    print("No file found at " + filename)
    sys.exit(1)

maxSeat = -1
validIDs = [False] * 1028
def calculateID(line):
    rowUpper = 127
    rowLower = 0
    columnUpper = 7
    columnLower = 0
    rows = line[:7]
    cols = line[7:]
    #print(rows)
    #print(cols)
    for char in rows:
        delta = ((rowUpper + 1) - rowLower) / 2
        if(char == "F"):
            rowUpper = rowUpper - delta
        elif(char == "B"):
            rowLower = rowLower + delta
    for char in cols:
        delta = ((columnUpper + 1) - columnLower) / 2
        if(char == "L"):
            columnUpper = columnUpper - delta
        elif(char == "R"):
            columnLower = columnLower + delta
    #print(line + ", " + str(columnUpper) + ", " + str(columnLower))
    #print((rowUpper * 8) + columnUpper)
    return int((rowUpper * 8) + (columnUpper))

for line in inputFile:
    lineID = calculateID(line.strip())
    if(lineID > maxSeat):
        maxSeat = lineID
    validIDs[lineID] = True

for a in range(1, 1027):
    if(not validIDs[a] and validIDs[a-1] and validIDs[a+1]):
        print(a)

    
print("num: " + str(maxSeat))
    
    