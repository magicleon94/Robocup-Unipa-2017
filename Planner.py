# Author: Christian Careaga (christian.careaga7@gmail.com)
# A* Pathfinding in Python (2.7)
# Please give credit if used

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
        self.start = (1,1)
        self.goal  = (1,3)
        self.current_position = self.start
        self.current_theta = 90

        self.nmap =  numpy.array([#0     1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19
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

    def plan(self,leftObstacle,rightObstacle):
        if self.current_position == self.goal:
            return 0
        try:
            next_move = self.astar(self.nmap,self.current_position,self.goal)[-1]
        except:
            print "No path found"
            return 0

        if self.start == self.goal:
            print "END"
            return 0
        dx = next_move[1]-self.current_position[1]
        dy = next_move[0]-self.current_position[0]

        if dx > 0:
            if self.current_theta == 0:
                return constants.FORWARD
            elif self.current_theta == 90:
                return constants.RIGHT_AND_FORWARD
            elif self.current_theta == 180:
                if not rightObstacle:
                    return constants.RIGHT_180_AND_FORWARD
                if not leftObstacle:
                    return constants.LEFT_180_AND_FORWARD
            elif self.current_theta == 270:
                return constants.LEFT_AND_FORWARD

            self.current_theta = 0

        elif dx < 0:
            if self.current_theta == 180:
                return constants.FORWARD
            elif self.current_theta == 270:
                return constants.RIGHT_AND_FORWARD
            elif self.current_theta == 0:
                if not rightObstacle:
                    return constants.RIGHT_180_AND_FORWARD
                if not leftObstacle:
                    return constants.LEFT_180_AND_FORWARD
            elif self.current_theta == 90:
                return constants.LEFT_AND_FORWARD

            self.current_theta = 180

        elif dy > 0:
            if self.current_theta == 90:
                return constants.FORWARD
            elif self.current_theta == 180:
                return constants.RIGHT_AND_FORWARD
            elif self.current_theta == 270:
                if not rightObstacle:
                    return constants.RIGHT_180_AND_FORWARD
                if not leftObstacle:
                    return constants.LEFT_180_AND_FORWARD
            elif self.current_theta == 0:
                return constants.LEFT_AND_FORWARD

            self.current_theta = 90

        elif dy < 0:
            if self.current_theta == 270:
                return constants.FORWARD
            elif self.current_theta == 0:
                return constants.RIGHT_AND_FORWARD
            elif self.current_theta == 90:
                if not rightObstacle:
                    return constants.RIGHT_180_AND_FORWARD
                if not leftObstacle:
                    return constants.LEFT_180_AND_FORWARD
            elif self.current_theta == 180:
                return constants.LEFT_AND_FORWARD
            self.current_theta = 270
        self.current_position = next_move
