import os
import sys
import re
import time as timeMod
import argparse

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

fields = dict()
my_ticket = ""
nearby_tickets = []
#parse the input
mode = 0

#takes in ticket string, outputs array of ints
def parse_ticket(ticket):
    ticket_arr = []
    for num in ticket.strip().split(","):
        ticket_arr.append(int(num))
    return ticket_arr

def parse_range(field_ranges):
    range_arr = []
    for field_range in field_ranges.strip().split("or"):
        nums = field_range.split("-")
        lower = int(nums[0].strip())
        upper = int(nums[1].strip())
        range_arr.append(range(lower, upper + 1)) #upper inclusive
    return range_arr

for line in inputFile:
    if(line == "\n"):
        mode += 1
        continue
    if(mode == 0):
        split = line.split(": ")
        fields[split[0].strip()] = parse_range(split[1].strip())
    elif(mode == 1):
        if(line.strip() == "your ticket:"):
            continue
        else:
            my_ticket = parse_ticket(line)
    elif(mode == 2):
        if(line.strip() == "nearby tickets:"):
           continue
        else:
            nearby_tickets.append(parse_ticket(line))

def validate_num(number):
    for field in fields:
        for nRange in fields[field]: 
            if number in nRange:
                return True
    return False

def invalid_for(number):
    invalid = []
    for field in fields:
        found = False
        for nRange in fields[field]:
            if number in nRange:
                found = True
        if(not found):
            invalid.append(field)
            #print(str(number) + ": " + str(fields[field]))
    
    return invalid

#print(fields)
#print(my_ticket)
#print(nearby_tickets)


def validate_ticket(ticket):
    for num in ticket:
        if(not validate_num(num)):
            return False
    return True

def part1():
    ticket_error = 0
    for nTicket in nearby_tickets:
        for num in nTicket:
            if(not validate_num(num)):
                #print(num)
                ticket_error += num
    return ticket_error

possibilities = dict()
for key in fields.keys():
    possibilities[key] = [True] * len(fields.keys())
indecies= [None] * len(fields.keys())



def place(field, min):
    global indecies
    try:
        index = possibilities[field].index(True, min)
    except ValueError:
        return False
    if(indecies[index] == None):
        indecies[index] = field
        return True
    else:
        return place(field, index + 1)

def get_possibilities(field):
    min = 0
    indexes = []
    while True:
        try:
            index = possibilities[field].index(True, min)
            indexes.append(index)
            min = index + 1
        except ValueError:
            return indexes
            
        

def part2():
    ticket_list = filter(validate_ticket, nearby_tickets) #filter invalid tickets
    global possibilities
    for valid_ticket in ticket_list:
        for i in range(len(valid_ticket)):
            invalid = invalid_for(valid_ticket[i])
            for field in invalid:
                possibilities[field][i] = False
    done = False
    for field in possibilities:
        if(not place(field, 0)):
            possible_indexes = get_possibilities(field)
            for possible in possible_indexes:
                if(place(indecies[possible], 0)):
                    indecies[possible] = field
                    break
    if(args.verbose > 0):
        print(indecies)
    print("unplaced fields (if any). Move these to the top of your input:")
    for field in possibilities:
        if(field in indecies):
            continue
        if(not place(field, 0)):
            print(field + ": " + str(possible_indexes))
    prod = 1
    for a in range(len(indecies)):
        if(indecies[a] != None and indecies[a].count("departure") > 0):
            prod *= my_ticket[a]
    return prod
  
    
    
   
print("Part 1 " + str(part1()))
print("Part 2 " + str(part2()))

