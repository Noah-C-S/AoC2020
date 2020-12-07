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

def calculateSum(group):
    sum = 0
    values = [True]*26
    for char in group.replace("\n", ""):
        #print(char + "," + str(ord(char)))
        if(values[ord(char)- 97]):
            sum += 1
            values[ord(char)-97] = False
    print(group + " | " + str(sum))
    return sum

def calculateSum2(group):
    sum = 0
    valueTables = []
    for line in group.split("\n"):
        #print(char + "," + str(ord(char)))
        values = [True]*26
        for char in line.strip():
            if(values[ord(char)- 97]):
                values[ord(char)-97] = False
        valueTables.append(values)
    print(valueTables)
    for c in range(26):   
        print(list(filter(lambda v: not v[c], valueTables)))
        if(len(list(filter(lambda v: not v[c], valueTables))) == len(valueTables)):
            sum += 1
    print(group + " | " + str(sum))
    return sum


sums = []
group = ""
for line in inputFile:
    group = group + line
    if(line == '\n'):
        lsum = calculateSum2(group.strip())
        sums.append(lsum)
        print(group)
        group = ""
    else:
        print(line.strip())
lsum = calculateSum2(group.strip())
sums.append(lsum)

    
print("num: " + str(sum(sums)))
    
    