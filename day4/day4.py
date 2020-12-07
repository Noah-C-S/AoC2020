import os
import sys
import re

filename = os.path.normpath(os.path.join(os.path.dirname(__file__), "input.txt"))
inputs = []
try:
    inputFile = open(filename)
except FileNotFoundError:
    print("No file found at " + filename)
    sys.exit(1)

byr = False
iyr = False
eyr = False
hgt = False
hcl = False
ecl = False
pid = False
cid = False
counter = 0
for line in inputFile:
    if(line == "\n"):
        byr = False
        iyr = False
        eyr = False
        hgt = False
        hcl = False
        ecl = False
        pid = False
        cid = False
        print("blank line\n")
        continue
    sys.stdout.write(line)
    #fields = re.split(r':| ', line.strip())
    fields = line.strip().split(" ")
    #print(fields[0][:3])
    #print(fields)
    try:
        for field in fields:
            key = field[:3]
            value = field.split(":")[1].strip()
            if(key == "byr"):
                year = int(value)
                if(year >= 1920 and year <= 2002):
                    byr = True
                    print(key + " : " + value)
                else:
                    byr = False
            if(key == "iyr"):
                year = int(value)
                if(year >= 2010 and year <= 2020):
                    iyr = True
                    print(key + " : " + value)
                else:
                    iyr = False
            if(key == "eyr"):
                year = int(value)
                if(year >= 2020 and year <= 2030):
                    eyr = True
                    print(key + " : " + value)
                else:
                    eyr = False
            if(key == "hgt"):
                if(re.fullmatch(r'\d+(in|cm)', value)):
                    height = int(value[:-2])
                    print(height)
                    if(value[-1] == "m"):
                        if(height >= 150 and height <=193):
                            hgt = True
                            print(key + " : " + value)
                    else:
                        if(height >= 59 and height <=76):
                            hgt = True
                            print(key + " : " + value)
                    
                else:
                    hgt = False
            if(key == "hcl"):
                if(re.fullmatch(r'#(\d|[a-f]){6}', value)):
                    hcl = True
                    print(key + " : " + value)
                else:
                    hcl = False
            if(key == "ecl"):
                if(value in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]):
                    ecl = True
                    print(key + " : " + value)
                else:
                    ecl = False
            if(key == "pid"):
                if(re.fullmatch(r'\d{9}', value)):
                    pid = True
                    print(key + " : " + value)
                else:
                    pid = False
            if(key == "cid"):
                cid = True
                print(key + " : " + value)
    except ValueError:
        continue
    if(byr and iyr and eyr and hgt and hcl and ecl and pid):
        byr = False
        iyr = False
        eyr = False
        hgt = False
        hcl = False
        ecl = False
        pid = False
        cid = False
        print("Good passport")
        counter += 1
print("num: " + str(counter))
    
    