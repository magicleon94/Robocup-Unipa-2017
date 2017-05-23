import time,os
from matplotlib import pyplot
from BlockSparseMatrix import BlockSparseMatrix
from BresenhamAlgorithms import BresenhamLine,BresenhamTriangle,BresenhamPolygon
from gridmap import GridMap,SonarSensor
import numpy
#set this true and have mencoder to create a video of the test
makevideo = True

#set up the map and scale
scale = 100.0
groundtruth = ((1,1,1,1,1),
               (1,0,0,0,1),
               (1,0,1,0,1),
               (1,0,0,0,1),
               (1,1,1,1,1))
gridScale = 0.5
#set up the grid map on a 2cm scale (half the input resolution)
estmap = GridMap(scale=gridScale)

#this is the set of positions the rover moves between
tour = ((150.0,150.0,0.0),(350.0,150.0,0.0),
        (350.0,150.0,numpy.pi/2.0),(350.0,350.0,numpy.pi/2.0),
        (350.0,350.0,numpy.pi),(150.0,350.0,numpy.pi),
        (150.0,350.0,numpy.pi*1.5),(150.0,150.0,numpy.pi*1.5),(150.0,150.0,numpy.pi*2))

#this is the number of steps along each part of the tour
divs =100
vals = []
for i in xrange(len(tour)-1):


    for j in xrange(divs):
        position = numpy.array(tour[i])*(1.-j/float(divs))+numpy.array(tour[(i+1)%len(tour)])*(j/float(divs))

        p = position[:2]
        a = -position[2]+numpy.pi
        offset = numpy.array([numpy.sin(a),numpy.cos(a)])*20.

        for k in xrange(4):

            #simulate each of the sonar sensor sweeps and see if we hit anything.
            sensor = SonarSensor
            sensorangle = numpy.pi/2*k
            thetamax = position[2] + sensor["spread"]/2. + sensorangle
            thetamin = position[2] - sensor["spread"]/2. + sensorangle
            baseB = numpy.array([numpy.cos(thetamax),numpy.sin(thetamax)])
            baseC = numpy.array([numpy.cos(thetamin),numpy.sin(thetamin)])
            hit = False
            for distance in xrange(int(sensor["range"])):
                B = numpy.round(baseB*distance + position[:2]).astype(numpy.int32)
                C = numpy.round(baseC*distance + position[:2]).astype(numpy.int32)

                for pos in BresenhamLine(B,C):
                    if groundtruth[int((pos[0]/scale))][int((pos[1]/scale))] == 1:
                        distance = numpy.linalg.norm(position[:2] - pos) #add noise in here if you want noise
                        hit = True
                        break
                if hit:
                    t0 = time.time()
                    estmap.update(position,distance,sensorangle,sensor)
                    vals.append(time.time()-t0)
                    break
            if not hit:
                t0 = time.time()
                estmap.update(position,distance,sensorangle,sensor)
                vals.append(time.time()-t0)

        if makevideo: #save out png's for the video
            fname = 'lullotest.png'
            tl = (95,95)
            print (i*divs+j)
            robot = (numpy.array([p+offset,p-offset,p+numpy.array([-offset[1],offset[0]])])*gridScale-numpy.array(tl)*gridScale).astype(numpy.int64)
            emap = numpy.clip(estmap.getRange(tl,(405,405)), -1000,1000 )
            for cell in BresenhamTriangle(robot[0],robot[1],robot[2]):
                emap[cell[0],cell[1]] = 120
            pyplot.imsave(fname,emap)
            pyplot.clf()

print "Mean Sensor Update Time:", numpy.mean(vals)
