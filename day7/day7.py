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


bags = dict()

for line in inputFile:
    bagSplit = line.split("contain")
    bag = bagSplit[0].strip()
    bags[bag] = []
    innerBags = bagSplit[1].split(",")
    for innerBag in innerBags:
        bags[bag].append(re.sub(r'/d', "", innerBag).strip())
#print(bags)
searchFor = "shiny gold"
containing = []
containing.append(searchFor)

while True:
    startLen = len(containing)
    for bag in bags:
        for innerBag in bags[bag]:
            if(bag.strip("s") in containing):
                break
            for outerBag in containing:
                if(innerBag.count(outerBag) > 0):
                    containing.append(bag.strip("s"))
                    break
    if(len(containing) == startLen):
        break;
    #print(containing)   

def calculateInnerBags(bagToSearchFor):
    count = 0
    #print(str(amount) + " " + bagToSearchFor)
    for innerBag in bags[bagToSearchFor]:
        #print("\t" + innerBag)
        if(innerBag == "no other bags."):
            return 1
        iBagPart = innerBag.partition(" ")
        num = int(iBagPart[0])
        theBag = iBagPart[2]
        if(not theBag.endswith("s.")):
            theBag = theBag.replace(".", "s")
        theBag = theBag.strip(".")
        if(not theBag.endswith("s")):
            theBag = theBag + "s"
        count += num * calculateInnerBags(theBag)
    #print(str(amount) + " " + bagToSearchFor + ": " + str(count))
    return 1 + count 
print("Part 1: " + str(len(containing) -1))
print("Part 2: " + str(calculateInnerBags("shiny gold bags") -1))
    