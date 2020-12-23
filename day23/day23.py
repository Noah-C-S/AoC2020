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

labels = []
for char in inputFile.read():
    if(char == "\n"):
        break
    labels.append(int(char))

p1Labels = copy.deepcopy(labels)

#Slow version I implemented for part 1
def makeMove(theLabels, moveNum):
    labels = copy.deepcopy(theLabels)
    current = labels[moveNum]
    pickedUp = []
    loc = moveNum + 1
    locs = []
    for i in range(3):
        if(loc >= len(labels)):
            loc = 0
        pickedUp.append(labels[loc])
        locs.append(loc)
        loc+=1 
    labels.pop(locs[0])
    try:
        labels.pop(locs[0])
    except IndexError:
        labels.pop(locs[1])
        labels.pop(locs[1])
    else:
        try:
            labels.pop(locs[0])
        except IndexError:
            labels.pop(locs[2])
    destCup = current - 1
    while destCup not in labels:
        destCup -=1
        if(destCup < min(labels)):
            destCup = max(labels)
    #log(theLabels)
    #log("Current: " + str(current))
    #log("Pick up: " + str(pickedUp))
    #log("Destination: " + str(destCup))
    #log("")
    index = labels.index(destCup)
    for pu in pickedUp[::-1]:
        labels.insert(index+1, pu)
    while(labels[moveNum] != current):
        labels.append(labels.pop(0))
    return labels
    
def part1():
    global p1Labels
    moveNum = 0
    counter = 0
    for i in range(100):
        counter += 1
        p1Labels = makeMove(p1Labels, moveNum)
        moveNum +=1
        if(moveNum >= len(p1Labels)):
            moveNum = 0
    log(p1Labels)
    result = ""
    while (p1Labels[0] != 1):
        p1Labels.append(p1Labels.pop(0))
    for l in p1Labels[1:]:   
        result = result + str(l)
    return result

        
class Node:
    def __init__(self, num, next):
        self.num = num
        self.next = next
    def __eq__(self, other):
        if(other is None or self is None):
            return False
        return self.num == other.num
        
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __str__(self):
        return str(self.num)

class CircLL:
    def __init__(self, length):
        self.head = None
        self.tail = None
        self.current = None
        self.pickedUp = None
        self.nodes = [None] * length #too lazy to use index 0
    
    def push(self, num):
        #All point to head at first
        #But when a new one is added *after* it, then it will point to that new one
        newNode = Node(num, self.head)
        if(self.head is None):
            self.head = newNode
            self.current = newNode
        if(self.tail is not None):
            self.tail.next = newNode
        self.tail = newNode
        self.nodes[num] = newNode
        
       
    
    def getResult(self):
        oneNode = self.nodes[1]
        nextNode = oneNode.next
        log(str(nextNode.num) + ", " + str(nextNode.next.num))
        return nextNode.num * nextNode.next.num
    
    def getP1(self):
        oneNode = self.nodes[1]
        nextNode = oneNode.next
        result = ""
        maxGoes = len(self.nodes) + 5
        numGoes = 0
        while nextNode.num != 1 and numGoes < maxGoes:
            result = result + str(nextNode.num)
            nextNode = nextNode.next
            numGoes += 1
        return result
    
    def printList(self):
        if(args.verbose < 1):
            return
        if self.head.next is None:
            log(self.head.num)
            return
        start = self.head.num
        pointer = self.head
        toPrint = str(pointer.num)
        pointer = pointer.next
        maxLoops = 40
        loops = 0
        while pointer is not None and pointer.num != start and loops < maxLoops:
            toPrint += " " + str(pointer.num)
            pointer = pointer.next
            loops += 1
        log(toPrint)
    
    def writeList(self):
        filepath = os.path.normpath(os.path.join(os.path.dirname(__file__), "out.txt"))
        outFile = open(filepath, "w")
        if self.head.next is None:
            outFile.write(str(self.head.num))
            return
        start = self.head.num
        pointer = self.head
        toPrint = str(pointer.num)
        pointer = pointer.next
        while pointer is not None and pointer.num != start:
            toPrint += " " + str(pointer.num)
            pointer = pointer.next
        outFile.write(toPrint)
        outFile.close()
    
    def makeMove(self):
        pickedUp = []
        currentNum = self.current.num
        toPick = self.current.next
        for i in range(3):
            pickedUp.append(toPick)
            toPick = toPick.next
        toLog = "Picked Up: "
        for thePicked in pickedUp:
            toLog += str(thePicked.num) + ", "
        log(toLog)
        self.current.next = toPick #picked up will actually be the one after the last one picked up :P
        destNum = currentNum -1
        destNode = self.nodes[destNum]
        while destNode in pickedUp or destNode is None:
            destNum = destNum -1
            if(destNum <= 0):
                destNum = len(self.nodes) - 1
            destNode = self.nodes[destNum]
        log("Destination: " + str(destNode.num))
        dNextNode = destNode.next
        destNode.next = pickedUp[0]
        pickedUp[2].next = dNextNode
        log("Current number: " + str(self.current.num)) #for debugging
        self.current = self.current.next #for next turn

def part1WithCLL():
    cups = CircLL(len(labels) + 1)
    for num in labels:
        cups.push(num)
        cups.printList()
    for i in range(100):
        log("Move no. " + str(i + 1))
        cups.makeMove()
        cups.printList()
        log("")
    
    return cups.getP1()

     
def part2():
    cups = CircLL(1000001)
    for num in labels:
        cups.push(num)
        cups.printList()
    for a in range(len(labels) +1,  1000001):
        cups.push(a)
    for i in range(10000000):
        if((i + 1) % 100000 == 0):
            log("Move no. " + str(i + 1))
        cups.makeMove()
    cups.writeList()
    return cups.getResult()
   
print("Part 1 " + str(part1WithCLL()))
print("Part 2 " + str(part2()))

