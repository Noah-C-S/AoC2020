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

player1 = []
player2 = []
mode = 0

for line in inputFile:
    if(line == "\n"):
        mode += 1
    try:
        if(mode == 0):
            player1.append(int(line))
        if(mode == 1):
            player2.append(int(line))
    except ValueError:
        continue

player1_c = copy.deepcopy(player1)
player2_c = copy.deepcopy(player2)

def turn():
    global player1
    global player2
    player1Num = player1.pop(0)
    player2Num = player2.pop(0)
    if(player1Num > player2Num):
        player1.append(player1Num)
        player1.append(player2Num)
    else:
        player2.append(player2Num)
        player2.append(player1Num)
        
def calculateScore(deck):
    score = 0
    for i in range(len(deck)):
        score += deck[i] * (len(deck) - i)
    return score

def part1():
    while(len(player1) > 0 and len(player2) > 0):
        turn()
    if(len(player1) > 0):
        return calculateScore(player1)
    else:
        return calculateScore(player2)
        
#plays a game of recursive combat using the given decks
#returns a list containing [winning deck, winning player]
def playRecursive(player1_d, player2_d):
    player1_history = [copy.deepcopy(player1_d)]
    player2_history = [copy.deepcopy(player2_d)]
    player1 = copy.deepcopy(player1_d)
    player2 = copy.deepcopy(player2_d)
    while len(player1) > 0 and len(player2) > 0:
        log(player1)
        log(player2)
        player1Num = player1.pop(0)
        player2Num = player2.pop(0)
        if(len(player1) >= player1Num and len(player2) >= player2Num):
            winner = playRecursive(player1[:player1Num], player2[:player2Num])[1]
            if(winner == 1):
                player1.append(player1Num)
                player1.append(player2Num)
            else:
                player2.append(player2Num)
                player2.append(player1Num)
        else:
            if(player1Num > player2Num):
                player1.append(player1Num)
                player1.append(player2Num)
            else:
                player2.append(player2Num)
                player2.append(player1Num)
        if(player1 in player1_history and player2 in player2_history):
            return [player1, 1]
        player1_history.append(copy.deepcopy(player1))
        player2_history.append(copy.deepcopy(player2))
    
    if(len(player1) > 0):
        return [player1, 1]
    else:
        return [player2, 2]
        
    

def part2():
    result = playRecursive(player1_c, player2_c)
    log("Player " + str(result[1]) + " Wins!")
    return calculateScore(result[0])
   
print("Part 1 " + str(part1()))
print("Part 2 " + str(part2()))

