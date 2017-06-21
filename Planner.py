# Author: Christian Careaga (christian.careaga7@gmail.com)
# A* Pathfinding in Python (2.7)
# Please give credit if used

# Revised and adapted by Vizeta Team (De Gregorio- Galipo' - Palmeri)

import numpy
import heapq
import constants

class Planner:

    def heuristic(self,a, b):
        return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

    def astar(self,array, start, goal):

        neighbors = [(0,1),(0,-1),(1,0),(-1,0)]

        close_set = set()
        came_from = {}
        gscore = {start:0}
        fscore = {start:self.heuristic(start, goal)}
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
                tentative_g_score = gscore[current] + self.heuristic(current, neighbor)
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
                    fscore[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))

        return False

######## y-axis
#
#
#
#
#x-axis
    def __init__(self):
        self.start = (16,1)
        self.goal  = (1,12)
        self.current_position = self.start
        self.current_theta = 180
                                #Aggiornare la mappa
        self.nmap =  numpy.array([#0    1   2   3   4   5   6   7   8   9   10  11  12  13
                                 [10,   10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],#0
                                 [10,   0,  0,  0,  0,  0,  0,  0,  1,  1,  0,  0,  0,  10],#1
                                 [10,   0,  0,  0,  0,  0,  0,  0,  1,  1,  0,  0,  0,  10],#2
                                 [10,   0,  0,  0,  0,  1,  1,  0,  0,  0,  1,  1,  0,  10],#3
                                 [10,   0,  0,  0,  0,  1,  1,  0,  0,  0,  1,  1,  0,  10],#4
                                 [10,   1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#5
                                 [10,   1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  10],#6
                                 [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  10],#7
                                 [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#8
                                 [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#9
                                 [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#10
                                 [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#11
                                 [10,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  10],#12
                                 [10,   0,  0,  0,  0,  0,  0,  0,  1,  1,  0,  0,  0,  10],#13
                                 [10,   0,  0,  0,  0,  0,  0,  0,  1,  1,  0,  0,  0,  10],#14
                                 [10,   0,  0,  0,  0,  0,  0,  0,  1,  1,  0,  0,  0,  10],#15
                                 [10,   0,  0,  0,  0,  0,  0,  0,  1,  1,  0,  0,  0,  10],#16
                                 [10,   10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]])#17

        #FOR TESTING
        #while(self.current_position != self.goal):
        #    self.plan(False,False)

    def plan(self,leftObstacle,rightObstacle):

        if self.current_position == self.goal:
            print "END"
            return 0

        try:
            # next_position[0] x-axis next_position[1] y-axis
            next_position = self.astar(self.nmap,self.current_position,self.goal)[-1]
        except:
            print "No path found"
            return 0

    #JUNK CODE INITIALLY current_position IS STILL EQUAL TO start
    #    if self.start == self.goal:
    #        print "END"
    #        return 0

        dx = next_position[0]-self.current_position[0]
        dy = next_position[1]-self.current_position[1]

        print "-------"
        print "Current position: " + str(self.current_position)
        print "Current theta: " + str(self.current_theta)
        #UPDATE POSITION
        self.current_position = next_position

        server_msg = ''

        if dx == -1: #GO UP
            if self.current_theta == 180:
                print "GO UP - FORWARD"
                server_msg = "constants.FORWARD"
            #    return constants.FORWARD
            elif self.current_theta == 270:
                print "GO UP - RIGHT AND FORWARD"
                server_msg = "constants.RIGHT_AND_FORWARD"
                #return constants.RIGHT_AND_FORWARD
            elif self.current_theta == 0:
                if not rightObstacle:
                    print "GO UP - RIGHT 180 AND FORWARD"
                    server_msg = "constants.RIGHT_180_AND_FORWARD"
                #    return constants.RIGHT_180_AND_FORWARD
                if not leftObstacle:
                    print "GO UP - LEFT_180_AND_FORWARD"
                    server_msg = "constants.LEFT_180_AND_FORWARD"
                    #return constants.LEFT_180_AND_FORWARD
                #DEVO CONSIDERARE SE HO UN OSTACOLO A SINISTRA E A DESTRA?
                #CASOMAI VADO INDIETRO E POI GIRO...CONSIDERARE ANCHE
                #NEGLI ALTRI CASI
            #elif self.current_theta == 90:
            else:
                print "GO UP - LEFT_AND_FORWARD"
                server_msg = "constants.LEFT_AND_FORWARD"
                #return constants.LEFT_AND_FORWARD

            self.current_theta = 180

        elif dx == 1: #GO DOWN
            if self.current_theta == 0:#180:
                print "GO DOWN - FORWARD"
                server_msg = "constants.FORWARD"
                #return constants.FORWARD
            elif self.current_theta == 90:
                print "GO DOWN - RIGHT_AND_FORWARD"
                server_msg = "constants.RIGHT_AND_FORWARD"
                #return constants.RIGHT_AND_FORWARD
            elif self.current_theta == 180:
                if not rightObstacle:
                    print "GO DOWN - RIGHT_180_AND_FORWARD"
                    server_msg = "constants.RIGHT_180_AND_FORWARD"
                    #return constants.RIGHT_180_AND_FORWARD
                if not leftObstacle:
                    print "GO DOWN - LEFT_180_AND_FORWARD"
                    server_msg = "constants.LEFT_180_AND_FORWARD"
                    #return constants.LEFT_180_AND_FORWARD
            #elif self.current_theta == 270:
            else:
                print "GO DOWN - LEFT_AND_FORWARD"
                server_msg = "constants.LEFT_AND_FORWARD"
                #return constants.LEFT_AND_FORWARD

            self.current_theta = 0

        elif dy == 1: #GO RIGHT
            if self.current_theta == 90:
                print "GO RIGHT - FORWARD"
                server_msg = "constants.FORWARD"
                #return constants.FORWARD
            elif self.current_theta == 180:
                print "GO RIGHT - RIGHT_AND_FORWARD"
                server_msg = "constants.RIGHT_AND_FORWARD"
                #return constants.RIGHT_AND_FORWARD
            elif self.current_theta == 270:
                if not rightObstacle:
                    print "GO RIGHT - RIGHT_180_AND_FORWARD"
                    server_msg = "constants.RIGHT_180_AND_FORWARD"
                    #return constants.RIGHT_180_AND_FORWARD
                if not leftObstacle:
                    print "GO RIGHT - LEFT_180_AND_FORWARD"
                    server_msg = "constants.LEFT_180_AND_FORWARD"
                    #return constants.LEFT_180_AND_FORWARD
            #elif self.current_theta == 0:
            else:
                print "GO RIGHT - LEFT_AND_FORWARD"
                server_msg = "constants.LEFT_AND_FORWARD"
                #return constants.LEFT_AND_FORWARD

            self.current_theta = 90

        #elif dy == -1: #GO LEFT
        else:
            if self.current_theta == 270:
                print "GO LEFT - FORWARD"
                server_msg = "constants.FORWARD"
                #return constants.FORWARD
            elif self.current_theta == 0:
                print "GO LEFT - RIGHT_AND_FORWARD"
                server_msg = "constants.RIGHT_AND_FORWARD"
                #return constants.RIGHT_AND_FORWARD
            elif self.current_theta == 90:
                if not rightObstacle:
                    print "GO LEFT - RIGHT_180_AND_FORWARD"
                    server_msg = "constants.RIGHT_180_AND_FORWARD"
                    #return constants.RIGHT_180_AND_FORWARD
                if not leftObstacle:
                    print "GO LEFT - LEFT_180_AND_FORWARD"
                    server_msg = "constants.LEFT_180_AND_FORWARD"
                    #return constants.LEFT_180_AND_FORWARD
            #elif self.current_theta == 180:
            else:
                print "GO LEFT - LEFT_AND_FORWARD"
                server_msg = "constants.LEFT_AND_FORWARD"
                #return constants.LEFT_AND_FORWARD

            self.current_theta = 270

          #else:
        #    print "STOPPED" #current_position == goal
        #    return 0

        print "Next position: " + str(self.current_position)
        print "Next theta: " + str(self.current_theta)
        return server_msg
