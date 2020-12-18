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
    
inputs = inputFile.read().split("\n")

def log(message):
    if(args.verbose > 0):
        print(message)
  
def evaluate(theExpr):
    expr = copy.deepcopy(theExpr)
    try:
        if(expr == ''):
            #print("Something wrong?")
            return 0
        return int(expr)
    except ValueError:
        i = 0
        subExpr = ""
        startIndex = 0
        inPar = False
        #print(expr)
        while i < len(expr):
            #print(expr)
            if(expr.count("(") == 0):
                break
            if(expr[i] == "("):
                subExpr = ""
                startIndex = i
                inPar = True
            elif(expr[i] == ")"):
                log(str(startIndex) + "," + str(i) + ": " + subExpr)
                expr = expr[:startIndex] + str(evaluate(subExpr)) + expr[i + 1:]
                i = 0
                log(expr)
                subExpr = ""
                startIndex = 0
                inPar = False
                continue
            elif inPar:
                subExpr = subExpr + expr[i]
            i += 1
        #print("No ??????")
        #print(expr)
        #ok hopefully no parenthesis
        split = expr.split(" ")
        while len(split) > 1:
            first = int(split.pop(0))
            op = split.pop(0)
            second = int(split.pop(0))
            if(op == "+"):
                split.insert(0, first + second)
            elif(op == "*"):
                split.insert(0, first * second)
        return int(split[0])

def evaluate2(theExpr):
    expr = copy.deepcopy(theExpr)
    try:
        if(expr == ''):
            #print("Something wrong?")
            return 0
        return int(expr)
    except ValueError:
        i = 0
        subExpr = ""
        startIndex = 0
        inPar = False
        #print(expr)
        while i < len(expr):
            #print(expr)
            if(expr.count("(") == 0):
                break
            if(expr[i] == "("):
                subExpr = ""
                startIndex = i
                inPar = True
            elif(expr[i] == ")"):
                
                log(str(startIndex) + "," + str(i) + ": " + subExpr)
                expr = expr[:startIndex] + str(evaluate2(subExpr)) + expr[i + 1:]
                i = 0
                log(expr)
                subExpr = ""
                startIndex = 0
                inPar = False
                continue
            elif inPar:
                subExpr = subExpr + expr[i]
            i += 1
        #print("No ??????")
        log(expr)
        #ok hopefully no parenthesis
        split = expr.split(" ")
        while i < len(split) -1:
            #print(split)
            #print(i)
            op = split[i + 1]
            if(op == "*"): #Skip these
                i += 2
                continue
            first = int(split.pop(i))
            op = split.pop(i)
            second = int(split.pop(i))
            split.insert(i, first + second)
        while len(split) > 1:
            first = int(split.pop(0))
            op = split.pop(0)
            second = int(split.pop(0))
            if(op == "*"):
                split.insert(0, first * second)
            else:
                print("WARNING: didn't get all additions!")
        return int(split[0])
      
def part1():
    sum = 0
    for line in inputs:
        sum+= evaluate(line)
    return sum

def part2():
    sum = 0
    for line in inputs:
        sum+= evaluate2(line)
    return sum

  
    
    
   
print("Part 1 " + str(part1()))
print("Part 2 " + str(part2()))

