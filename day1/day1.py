import os
import sys

filename = os.path.normpath(os.path.join(os.path.dirname(__file__), "input.txt"))
inputs = []
try:
    inputFile = open(filename)
except FileNotFoundError:
    print("No file found at " + filename)
    sys.exit(1)
    
for line in inputFile:
    inputs.append(int(line))
print(inputs)
sum = 2020
for i in range(len(inputs)):
    for j in range(len(inputs) - i):
        for k in range(len(inputs) -i - j):
            curSum = inputs[i] + inputs[i + j] + inputs[i + j + k]
            if(curSum == sum):
                print("Found it chief! " + str(inputs[i]) + " + " + str(inputs[i+j]) + " + " + str(inputs[i + j + k]) + " = " + str(curSum) + "\nThe solution is " + str(inputs[i] * inputs[i+j] * inputs[i+k+j]))
    