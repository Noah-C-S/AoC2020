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

tiles = dict()
newOne = True
curNum = 0

for line in inputFile:
    if(line == "\n"):
        newOne = True
        continue
    elif(newOne):
        curNum = int(line.split(" ")[1].strip(":\n"))
        newOne = False
        tiles[curNum] = []
        continue
    else:
        tiles[curNum].append(line.strip())

edgeTiles = dict()
#Like a clock, 0 = top, 1 = right, 2 = bottom, 3 = left
for k in tiles:
    edgeTiles[k] = []
    frame = tiles[k]
    top = frame[0]
    bottom = frame[-1]
    left = ""
    right = ""
    for line in frame:
        #Gonna store these just as strings, i.e. rotated 90 degrees, so top->bottom is stored as left->right
        left = left + line[0]
        right = right + line[-1]
    edgeTiles[k].append(top)
    edgeTiles[k].append(right)
    edgeTiles[k].append(bottom)
    edgeTiles[k].append(left)
    #print(str(k) + "\n:" + str(edgeTiles[k]))
log("Number of tiles: " + str(len(tiles)))
recon_size = int(math.sqrt(len(tiles)))
uniqueEdges = []
cUniqueEdges = []
for k in edgeTiles:
    for edge in edgeTiles[k]:
        if(edge not in uniqueEdges and edge[::-1] not in uniqueEdges):
            uniqueEdges.append(edge)
            cUniqueEdges.append(edge)
        else:
            try:
                cUniqueEdges.remove(edge)
            except ValueError:
                try:
                    cUniqueEdges.remove(edge[::-1])
                except ValueError:
                    pass #apears 3 times or more ig

#Rotates an array of strings by 90 degrees clockwise and returns the result
def rot90(arrIn):
    strArr = copy.deepcopy(arrIn)
    length = len(strArr)
    for i in range(length // 2):
        for j in range(i, length - i - 1):
            temp = strArr[i][j]
            strArr[i] = strArr[i][:j] + strArr[length - 1 - j][i] + strArr[i][j + 1:]
            strArr[length - 1 - j] = strArr[length - 1 - j][:i] +  strArr[length - 1 - i][length - 1 - j] + strArr[length -1 - j][i + 1:]
            strArr[length - 1 - i]= strArr[length - 1 - i][:length - 1 - j] + strArr[j][length - 1 - i] + strArr[length - 1 - i][length - j:]
            strArr[j] = strArr[j][:length - 1 - i] + temp + strArr[j][length - i:]
    return strArr

#Flips strArray across y axis
def flip_y(arrIn):
    strArr = copy.deepcopy(arrIn)
    for i in range(len(strArr)):
        strArr[i] = strArr[i][::-1]
    return strArr

#flips strArray across x axis 
def flip_x(arrIn):
    strArr = []
    for line in arrIn:
        strArr.insert(0, line)
    return strArr

def countUnique(id):
    edges = edgeTiles[id]
    uniqueCount = 0
    for edge in edges:
        if(edge in cUniqueEdges):
            uniqueCount +=1 
    #if(uniqueCount > 0):
        #log(uniqueCount)
    return uniqueCount

#I precompute these for the default, but not for rotated ones
#still top 0, right 1, down 2, left 3
def getEdges(frame):
    edges = []
    top = frame[0]
    bottom = frame[-1]
    left = ""
    right = ""
    for line in frame:
        #Gonna store these just as strings, i.e. rotated 90 degrees, so top->bottom is stored as left->right
        left = left + line[0]
        right = right + line[-1]
    edges.append(top)
    edges.append(right)
    edges.append(bottom)
    edges.append(left)
    return edges

def printFrame(frame):
    if(args.verbose < 1):
        return
    for line in frame:
        for char in line:
            sys.stdout.write(char + " ")
        sys.stdout.write("\n")
    log("______________________")

def removeBorders(frameIn):
    frame = copy.deepcopy(frameIn)
    frame = frame[1:-1]
    for i in range(len(frame)):
        frame[i] = frame[i][1:-1]
    return frame

def reconstructFrame(reconstructed):
    reconstructedFrame = []
    for row in reconstructed:
        recon_lines = ["" for x in range(8)]
        for id in row:
            frame = tiles[id]
            for i in range(len(frame)):
                recon_lines[i] += frame[i]
        for r in recon_lines:
            reconstructedFrame.append(r)
    return reconstructedFrame

#Finda sea monsters, in a frame, returns number found. 
def findSeaMonsters(frame):
    #This is the output from processMonsterImage.py 
    seaMonsterCoords = [[0, 0], [0, 5], [0, 6], [0, 11], [0, 12], [0, 17], [0, 18], [-1, 18], [0, 19], [1, 1], [1, 4], [1, 7], [1, 10], [1, 13], [1, 16]]
    monsFound = 0
    for i in range(1, len(frame) -1):
        for j in range(len(frame[i]) - 20):
            foundMon = True
            for mCoord in seaMonsterCoords:
                if(frame[i + mCoord[0]][j + mCoord[1]] != "#"):
                    foundMon = False
                    break
            if(foundMon):
                monsFound += 1
    return monsFound
            

def part1():
    prod = 1
    numFound = 0
    for k in tiles:
        if(countUnique(k) == 2):
            prod*=k
            numFound+=1
    log(numFound)
    return prod

def part2():
    #ID designations, corners = a random corner piece, edge_pieces = edge pieces, unplaced = middle pieces, reconstructed = ids in the right place relative to each other
    origin = -1
    edge_pieces = []
    unplaced = []
    global tiles
    reconstructed = [[-1 for x in range(recon_size)] for y in range(recon_size)]
    for k in tiles:
        numUnique = countUnique(k)
        if(numUnique >= 1):
            edge_pieces.append(k)
            if(numUnique == 2):
                origin = k
        else:
            unplaced.append(k)
    reconstructed[0][0] = origin #initial one, we'll build it based on this corner
    edge_pieces.remove(origin)
    #have to make sure that the initial corner has *both* non-unique sides facing in
    origin_frame = tiles[origin]
    origin_frame = flip_x(origin_frame)
    for i in range(4):
        originE = getEdges(origin_frame)
        if(originE[1] in cUniqueEdges or originE[2] in cUniqueEdges or originE[1][::-1] in cUniqueEdges or originE[2][::-1] in cUniqueEdges):
            origin_frame = rot90(origin_frame)
        else:
            break
    tiles[origin] = origin_frame
    #form the top row
    log(reconstructed)
    for i in range(1, recon_size):
        edge_to_match = getEdges(tiles[reconstructed[0][i - 1]])[1]
        for edge_piece in edge_pieces:
            edge_frame = tiles[edge_piece]
            last_frame = copy.deepcopy(edge_frame)
            for j in range(4):
                frame_edges = getEdges(last_frame)
                if(frame_edges[3] == edge_to_match):
                    tiles[edge_piece] = last_frame
                    reconstructed[0][i] = edge_piece
                    edge_pieces.remove(edge_piece)
                    break
                elif(frame_edges[1] == edge_to_match):
                    tiles[edge_piece] = flip_y(last_frame)
                    reconstructed[0][i] = edge_piece
                    edge_pieces.remove(edge_piece)
                    break
                elif(frame_edges[3][::-1] == edge_to_match):
                    tiles[edge_piece] = flip_x(last_frame)
                    reconstructed[0][i] = edge_piece
                    edge_pieces.remove(edge_piece)
                    break
                last_frame = rot90(last_frame)
    #Form the left side
    log(reconstructed)
    for i in range(1, recon_size):
        edge_to_match = getEdges(tiles[reconstructed[i - 1][0]])[2]
        for edge_piece in edge_pieces:
            edge_frame = tiles[edge_piece]
            last_frame = copy.deepcopy(edge_frame)
            for j in range(4):
                frame_edges = getEdges(last_frame)
                if(frame_edges[0] == edge_to_match):
                    tiles[edge_piece] = last_frame
                    reconstructed[i][0] = edge_piece
                    edge_pieces.remove(edge_piece)
                    break
                elif(frame_edges[2] == edge_to_match):
                    tiles[edge_piece] = flip_x(last_frame)
                    reconstructed[i][0] = edge_piece
                    edge_pieces.remove(edge_piece)
                    break
                elif(frame_edges[0][::-1] == edge_to_match):
                    tiles[edge_piece] = flip_y(last_frame)
                    reconstructed[i][0] = edge_piece
                    edge_pieces.remove(edge_piece)
                    break
                last_frame = rot90(last_frame)
    #form the right side
    log(reconstructed)
    for i in range(1, recon_size):
        edge_to_match = getEdges(tiles[reconstructed[i - 1][-1]])[2]
        for edge_piece in edge_pieces:
            edge_frame = tiles[edge_piece]
            last_frame = copy.deepcopy(edge_frame)
            for j in range(4):
                frame_edges = getEdges(last_frame)
                if(frame_edges[0] == edge_to_match):
                    tiles[edge_piece] = last_frame
                    reconstructed[i][-1] = edge_piece
                    edge_pieces.remove(edge_piece)
                    break
                elif(frame_edges[2] == edge_to_match):
                    tiles[edge_piece] = flip_x(last_frame)
                    reconstructed[i][-1] = edge_piece
                    edge_pieces.remove(edge_piece)
                    break
                elif(frame_edges[0][::-1] == edge_to_match):
                    tiles[edge_piece] = flip_y(last_frame)
                    reconstructed[i][-1] = edge_piece
                    edge_pieces.remove(edge_piece)
                    break
                last_frame = rot90(last_frame)
    #form the bottom
    log(reconstructed)
    for i in range(1, recon_size):
        edge_to_match = getEdges(tiles[reconstructed[-1][i - 1]])[1]
        for edge_piece in edge_pieces:
            edge_frame = tiles[edge_piece]
            last_frame = copy.deepcopy(edge_frame)
            for j in range(4):
                frame_edges = getEdges(last_frame)
                if(frame_edges[3] == edge_to_match):
                    tiles[edge_piece] = last_frame
                    reconstructed[-1][i] = edge_piece
                    edge_pieces.remove(edge_piece)
                    break
                elif(frame_edges[1] == edge_to_match):
                    tiles[edge_piece] = flip_y(last_frame)
                    reconstructed[-1][i] = edge_piece
                    edge_pieces.remove(edge_piece)
                    break
                elif(frame_edges[3][::-1] == edge_to_match):
                    tiles[edge_piece] = flip_x(last_frame)
                    reconstructed[-1][i] = edge_piece
                    edge_pieces.remove(edge_piece)
                    break
                last_frame = rot90(last_frame)
    log(reconstructed)
    #Get the middle
    for i in range(1, recon_size -1):
        for j in range(1, recon_size -1):
            top_edge_to_match = getEdges(tiles[reconstructed[i-1][j]])[2]
            left_edge_to_match = getEdges(tiles[reconstructed[i][j-1]])[1]
            done = False
            for unpl_p in unplaced:
                if(done):
                    break
                unpl_frame = tiles[unpl_p]
                last_frame = copy.deepcopy(unpl_frame)
                for k in range(4):
                    frame_edges = getEdges(last_frame)
                    if(frame_edges[0] == top_edge_to_match and frame_edges[3] == left_edge_to_match):
                        tiles[unpl_p] = last_frame
                        reconstructed[i][j] = unpl_p
                        unplaced.remove(unpl_p)
                        done = True
                        break
                    elif(frame_edges[2] == top_edge_to_match and frame_edges[3][::-1] == left_edge_to_match):
                        tiles[unpl_p] = flip_x(last_frame)
                        reconstructed[i][j] = unpl_p
                        unplaced.remove(unpl_p)
                        done = True
                        break
                    elif(frame_edges[0][::-1] == top_edge_to_match and frame_edges[1] == left_edge_to_match):
                        tiles[unpl_p] = flip_y(last_frame)
                        reconstructed[i][j] = unpl_p
                        unplaced.remove(unpl_p)
                        done = True
                        break
                    last_frame = rot90(last_frame)
    log(reconstructed)
    
    for k in tiles:
        tiles[k] = removeBorders(tiles[k])
    
    fullFrame = reconstructFrame(reconstructed)
    #for row in reconstructed:
        #for id in row:
           # printFrame(tiles[id])
    totalHash = 0
    printFrame(fullFrame)
    for line in fullFrame:
        totalHash+= line.count("#")
    log(totalHash)
    for a in range(4):
        #printFrame(fullFrame)
        #printFrame(flip_x(fullFrame))
        #printFrame(flip_y(fullFrame))
        basic = findSeaMonsters(fullFrame)
        x_flipped = findSeaMonsters(flip_x(fullFrame))
        y_flipped = findSeaMonsters(flip_y(fullFrame))
        if(basic > 0):
            return totalHash - 15 * basic
        elif(x_flipped > 0):
            return totalHash - 15 * x_flipped
        elif(y_flipped > 0):
            return totalHash - 15 * y_flipped
           
        fullFrame = rot90(fullFrame)

   
print("Part 1 " + str(part1()))
print("Part 2 " + str(part2()))

