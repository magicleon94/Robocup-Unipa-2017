# Author: Christian Careaga (christian.careaga7@gmail.com)
# A* Pathfinding in Python (2.7)
# Please give credit if used

import numpy
import heapq
import os

def heuristic(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

def astar(array, start, goal):

    neighbors = [(0,1),(0,-1),(1,0),(-1,0)]

    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:

        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] > 0:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False

######## y-axis
#
#
#
#
#x-axis
start = (18,1)
goal  = (1,18)
current_position = start
current_theta = 0

nmap =  numpy.array([#    0     1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19
                         [10,   10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],#0
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#1
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#2
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#3
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#4
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#5
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#6
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#7
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#8
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#9
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#10
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#11
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#12
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#13
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#14
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#15
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#16
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#17
                         [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#18
                         [10,   10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]])#19

nmap[start] = 9

def updateMap(x,y,theta,IRleft,IRfront,IRright):
    if theta == 0:
        nmap[x+1,y+1] = IRleft
        nmap[x+1,y] = IRfront
        nmap[x+1,y-1] = IRright
    elif theta == 90:
        nmap[x-1,y+1] = IRleft
        nmap[x,y+1] = IRfront
        nmap[x+1,y+1] = IRright
    elif theta == 180:
        nmap[x-1,y-1] = IRleft
        nmap[x-1,y] = IRfront
        nmap[x-1,y+1] = IRright
    elif theta == 270:
        nmap[x+1,y-1] = IRleft
        nmap[x,y-1] = IRfront
        nmap[x-11,y-1] = IRright

os.system("clear")
print nmap
print start
while current_position != goal:
    choice = int(raw_input("1. Nothing\n2. Insert obstacle\n").strip())
    if choice == 2:
        obstacleCoords = tuple(int(x) for x in raw_input("Insert coordinates separated by a space\n").strip().split(" "))
        nmap[obstacleCoords] = 1
    else:
        try:
            next_move = astar(nmap, start, goal)[-1]
        except IndexError:
            break;
        nmap[start] = 0
        start = next_move
        nmap[start] = 9
    os.system("clear")
    print nmap
    print start