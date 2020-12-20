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
    
#inputs = inputFile.read().split("\n")
sys.setrecursionlimit(3500)
def log(message):
    if(args.verbose > 0):
        print(message)

rules = [""]*300
messages = []
mode = 0
for line in inputFile:
    if(line == "\n"):
        mode +=1
        continue
    if(mode == 0):
        ruleNum = int(line.strip().partition(":")[0])
        rule = line.strip().partition(": ")[2].strip()
        rules[ruleNum] = rule
    elif(mode == 1):
        messages.append(line.strip())

messLen = len(messages[0])
for message in messages:
    if(len(message) > messLen):
        mesLen = len(message)


log(rules)
#log(messages)

def createRegEx(ruleNum):
    rule = rules[ruleNum]
    done = False
    while not done:
        done = True
        num = ""
        inNum = False
        startNum = -1
        #Find the first number and replace it with the expanded version wrapped in parenthesis
        #if it finds no numbers, it's done. Remove spaces and
        for i in range(len(rule)):
            #yeah I could use a regEx for this
            isANumber = rule[i] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            if(isANumber):
                inNum = True
                num+= rule[i]
                done = False
                if(startNum == -1):
                    startNum = i
            if(inNum and (not isANumber or (i + 1) == len(rule))):
                #found the number, replace it with the rule one farther down with parenthesis around it!
                log("solving: " + num + ", " + str(rules[int(num)]))
                theRule = rules[int(num)]
                if(theRule in ['"a"', '"b"']):
                    theRule = theRule[1]
                if theRule.count("|") > 0:
                    rule = rule[:startNum] + " ( " + theRule + " ) " + rule[i + 1:]
                else:
                    rule = rule[:startNum] + " " + theRule + " " + rule[i + 1:]
                break
        log(rule)
    return rule.replace(" ", "") #remove all spaces, now it *should* be a valid regEx
   



def part1():
    num = 0
    #print(rules[104])
    #sys.exit(0)
    expr = createRegEx(0)
    log(expr)
    for message in messages:
        if(re.fullmatch(expr, message)):
            num+= 1
            log(message + " is valid!")
        else:
            log(message + " is invalid!")
    return num

def part2():
    num = 0
    #print(rules[104])
    #sys.exit(0)
    #rules[8] = "42 | 42 8" #should expand to (42)+? hopefully won't get messed update
    rules[8] = " ( 42 )+ " #just pad everything with spaces so it doesn't get stepped on lol
    #rules[11] = "11: 42 31 | 42 11 31" #regEx can't detect palindromes ;_;
    rules[11] = " 42 31 "
    #BUT IT CAN DETECT PALINDROMES OF FINITE LENGTH, yeah it's big brain time
    
    rules[42] = " " + createRegEx(42) + " "
    rules[31] = " " + createRegEx(31) + " "
    
    for i in range(2, messLen):
        rules[11] = rules[11] + " | " + ((" 42 ")) * i + ((" 31 ") * i)
    rules[11] = createRegEx(11)
    #print(createRegEx(11))
    expr = createRegEx(0)
    log(expr)
    for message in messages:
        if(re.fullmatch(expr, message)):
            num+= 1
            log(message + " is valid!")
        else:
            log(message + " is invalid!")
    return num

   
print("Part 1 " + str(part1()))
print("Part 2 " + str(part2()))

