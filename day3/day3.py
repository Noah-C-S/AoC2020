import os
import sys

filename = os.path.normpath(os.path.join(os.path.dirname(__file__), "input.txt"))
inputs = []
try:
    inputFile = open(filename)
except FileNotFoundError:
    print("No file found at " + filename)
    sys.exit(1)
counter = 0 
x = 0
lineNum = 0
for line in inputFile:
    if((lineNum % 2) != 0):
        lineNum+= 1
        continue
    line = line.strip()
    lineNum += 1
    print(line + ", " + str(x) + ", " + line[x] + ", " + str(lineNum))
    if(line[x] == '#'):
        counter+=1
    x+=1
    if(x >= len(line)):
        x = x - len(line)
    
print("Number of trees = " + str(counter))
