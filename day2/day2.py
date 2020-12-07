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

def isValid(line):
    parts = line.split(":")
    parts[0].strip()
    parts[1].strip()
    nums = parts[0].split("-")
    letter = parts[0][-1]
    lower = int(nums[0].strip())
    upper = int(nums[1].split(" ")[0].strip())
    number = 0
    """print(line)
    print(lower)
    print(upper)
    print(parts[1])
    print(parts[1][lower])
    print(parts[1][upper])"""
    if(parts[1][lower] == letter):
        number += 1
    if(parts[1][upper] == letter):
        number+=1
    return number ==1 
    

for line in inputFile:
    if (isValid(line)):
        counter+=1
print("Number of valid ones = " + str(counter))
