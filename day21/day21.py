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


foods = []
for line in inputFile:
    split = line.split(" (contains ")
    ingredients = split[0]
    allergens = split[1].strip(")\n").split(" ")
    for i in range(len(allergens)):
        allergens[i] = allergens[i].strip(",")
    food = []
    food.append(allergens)
    food.append(ingredients.split(" "))
    foods.append(food)

log(foods)

#Gets all the ingredient lists which contain a particular allergen
def getAllContains(allergen):
    containing = []
    for food in foods:
        if(allergen in food[0]):
            containing.append(food)
    return containing

#Gets all unique allergens
def getAllAllergens():
    allergens = []
    for food in foods:
        for allergen in food[0]:
            if(not allergen in allergens):
                allergens.append(allergen)
    return allergens

log(getAllAllergens())

def getAllingredients():
    ingredients = []
    for food in foods:
        for ingredient in food[1]:
            if(not ingredient in ingredients):
                ingredients.append(ingredient)
    return ingredients

def getCommonIngredients(theFoods):
    common = theFoods[0][1]
    for food in theFoods:
        for ingredient in common:
            newCommon = copy.deepcopy(common)
            if(ingredient not in food[1]):
                newCommon.remove(ingredient)
            common = newCommon
    return common

containsDairy = getAllContains("dairy")
log(containsDairy)
log(getCommonIngredients(containsDairy))

allergenIngredients = dict()

def part1():
    allergens = getAllAllergens()
    while(len(allergens) > 0):
        toCheck = allergens.pop(0)
        containsCheck = getAllContains(toCheck)
        commonCheck = getCommonIngredients(containsCheck)
        for k in allergenIngredients:
            try:
                commonCheck.remove(allergenIngredients[k])
            except ValueError:
                pass
        if(len(commonCheck) == 1):
            allergenIngredients[toCheck] = commonCheck[0]
        else:
            allergens.append(toCheck)
        log(allergens)
    numNoAllergen = 0
    log(allergenIngredients)
    for food in foods:
        for ingredient in food[1]:
            if ingredient not in allergenIngredients.values():
                numNoAllergen += 1
    return numNoAllergen
        

def part2():
    alphabetKeys = sorted(allergenIngredients.keys())
    canonD = ""
    for k in alphabetKeys:
        canonD = canonD + "," + allergenIngredients[k]
    return canonD.strip(",")
   
print("Part 1 " + str(part1()))
print("Part 2 " + str(part2()))

