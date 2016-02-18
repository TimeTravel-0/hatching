#!/usr/bin/env python

import math


def optimizepaths(paths):
   '''removes redundant polygon points, decrease count, increase error '''
   newpaths = []
   for path in paths:
      newpath = []
      for position in path:
         lastangle = 360
         lastdistance = 999
         if len(newpath)>1:
            lastdistance = math.pow(math.pow(position[0]-newpath[-1][0],2) + math.pow(position[1]-newpath[-1][1],2),0.5)
            angle1 = math.atan2(position[1]-newpath[-1][1],position[0]-newpath[-1][0])
            angle2 = math.atan2(newpath[-1][1]-newpath[-2][1],newpath[-1][0]-newpath[-2][0])
            lastangle = abs(angle1-angle2)*float(360)/(2*math.pi)
   
         if float(lastdistance)*lastangle > 100:
            newpath.append(position)
      newpaths.append(newpath)
   return newpaths

def pathcombiner(paths):
   '''for all given paths, combine them if possible to reduce number and increase length'''
   # now we could check each start/end of every path and combine the two paths if they are closer together than a threshold
   # if start/end of same path are together closer than threshold but not equal, add first point to end to close the path

   while True:

      # collect all the start/end points
      startend_points = []
      for i in range(0,len(paths)):
         path = paths[i]
         if len(path)>1:
            startend_points.append([i,0,path[0]])
            startend_points.append([i,-1,path[-1]])

      redo = False
      # check each to start/end points
      for i in range(0,len(startend_points)):
         for j in range(0,len(startend_points)):
            point1 = startend_points[i]
            point2 = startend_points[j]

            distance = math.pow(math.pow(point1[2][0]-point2[2][0],2) + math.pow(point1[2][1]-point2[2][1],2),0.5)


            if distance < 10 and distance > 2: # magic values, snap below 10, but ignore below 2
               if point1[0] == point2[0]: # same path
                  if point1[1] == 0 and point2[1] == -1: # but start/end selected
                     paths[point1[0]].append(paths[point2[0]][0])
                     redo = True
                  if point1[1] == -1 and point2[1] == 0: # but end/start selected
                     paths[point2[0]].append(paths[point1[0]][0])

               else: # different paths
                  if point1[1] == 0 and point2[1] == 0: # heading face to face
                     paths[point2[0]]+=list(reversed(paths[point1[0]]))
                     paths[point1[0]] = []
                     redo = True
                  if point1[1] == -1 and point2[1] == -1: # heading tail to tail
                     paths[point1[0]]+=list(reversed(paths[point2[0]]))
                     paths[point2[0]] = []
                     redo = True
                  if point1[1] == 0 and point2[1] == -1: # heading face to tail
                     paths[point2[0]]+=paths[point1[0]]
                     paths[point1[0]] = []
                     redo = True
                  if point1[1] == -1 and point2[1] == 0: # heading tail to face
                     paths[point1[0]]+=paths[point2[0]]
                     paths[point2[0]] = []
                     redo = True
            if redo:
               break
         if redo:
            break

      if not redo:
         newpaths = []
         for path in paths:
            if len(path)>1:
               newpaths.append(path)

         return newpaths
