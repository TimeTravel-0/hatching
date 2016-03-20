#!/usr/bin/env python

import math
import pygame
from lib_image_filters import *


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

         # removal should not only be based on the angle to the last point but on the angle to the next point, too (e.g. keep sharp edges!)
         if lastdistance > 10 or lastangle > 5:
#         if float(lastdistance)*lastangle > 100:
            newpath.append(position)
      newpaths.append(newpath)
   return newpaths



def pathcombiner(paths_in):
   '''for all given paths, combine them if possible to reduce number and increase length'''
   # now we could check each start/end of every path and combine the two paths if they are closer together than a threshold
   # if start/end of same path are together closer than threshold but not equal, add first point to end to close the path
   # for now it takes the FIRST candidate that fits, not the best (=nearest) one!

   paths = []
   for p in paths_in:
      paths.append(p[:])

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
                  if point1[1] == 0 and point2[1] == -1: # but start/end selected = close loop
                     paths[point1[0]].append(paths[point2[0]][0])
                     print "loop closed start-end"
                     redo = True
                  if point1[1] == -1 and point2[1] == 0: # but end/start selected = close loop
                     paths[point2[0]].append(paths[point1[0]][0])
                     print "loop closed end-start"
                     redo = True

               else: # different paths
                  if point1[1] == 0 and point2[1] == 0: # heading face to face
                     paths[point2[0]] =list(reversed(paths[point1[0]])) + paths[point2[0]]
                     paths[point1[0]] = []
                     print "head-head"
                     redo = True

                  if point1[1] == -1 and point2[1] == -1: # heading tail to tail
                     paths[point1[0]]+=list(reversed(paths[point2[0]]))
                     paths[point2[0]] = []
                     print "tail tail. ok."
                     redo = True

                  if point1[1] == 0 and point2[1] == -1: # heading face to tail
                     paths[point2[0]]+=paths[point1[0]]
                     paths[point1[0]] = []
                     print "head tail"
                     redo = True

                  if point1[1] == -1 and point2[1] == 0: # heading tail to face
                     paths[point1[0]]+=paths[point2[0]]
                     paths[point2[0]] = []
                     print "tail head. ok."
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

         print "reduced %i paths to %i paths"%(len(paths_in),len(newpaths))
	
         return newpaths
         


def edgewalk(img):
   '''in image showing edges, walks along the edge and creates a polygon path'''

   img_clone = pygame.Surface(img.get_size())
   img_clone.blit(img,(0,0))


   paths = []

   radius = 3

   brightness_min = 5

   while True:
      position, br = find_brightest_pixel(img_clone)
      print position, br
      if not position or br < brightness_min:
         break
      path = []
      path.append(position)
      # position is the first pixel we started at.
      img_clone.set_at(position,(0,0,0)) # deactivate pixel
      # now, in a spiralish way, find next pixel
      angle2 = 0
      while True:
         position, br = find_brightest_pixel_with_spiral(img_clone,position,radius+3,angle2)
         if not position or br < brightness_min:
            break
         #lastdistance = math.pow(math.pow(position[0]-path[-1][0],2) + math.pow(position[1]-path[-1][1],2),0.5)
         #lastangle = 360
         #if len(path)>1:
         #   angle1 = math.atan2(position[1]-path[-1][1],position[0]-path[-1][0])
            angle2 = math.atan2(path[-1][1]-path[-2][1],path[-1][0]-path[-2][0])
         #   lastangle = abs(angle1-angle2)*float(360)/(2*math.pi)
            
         
         #if float(lastdistance)*lastangle > 1:
         if True:
            path.append(position)
         pygame.draw.circle(img_clone, (0,0,0), position, radius, 0)

      if len(path)>2:
         paths.append(path)



   print "found %i paths"%len(paths)

   paths = pathcombiner(paths)
   paths = optimizepaths(paths)

   print "optimized to %i paths"%len(paths)

   return paths
   
def render_vector(img,pos,angle,length):
    '''draw a nice arrow in image at position with angle'''
    color=(255,0,0)
    angle=angle/360.0*2*math.pi
    dy = math.sin(angle)*length
    dx = math.cos(angle)*length
    endpos=[pos[0]+dx,pos[1]+dy]
    
    peak1pos = [endpos[0]-math.cos(angle+0.3)*10,endpos[1]-math.sin(angle+0.3)*10]
    peak2pos = [endpos[0]-math.cos(angle-0.3)*10,endpos[1]-math.sin(angle-0.3)*10]

    img_clone = pygame.Surface(img.get_size())
    img_clone.blit(img,(0,0))    
    
    pygame.draw.line(img_clone,color,pos,endpos,2)
    pygame.draw.line(img_clone,color,peak1pos,endpos,2)
    pygame.draw.line(img_clone,color,peak2pos,endpos,2)
    
    
    return img_clone

def edgewalk_visualize(img, display, radius=3):
   '''in image showing edges, walks along the edge and creates a polygon path'''

   img_clone = pygame.Surface(img.get_size())
   img_clone.blit(img,(0,0))


   paths = []

   #radius = 3

   brightness_min = 5
   
   render_cnt = 0

   while True:
      position, br = find_brightest_pixel(img_clone)
      print position, br
      if not position or br < brightness_min:
         break
      path = []
      path.append(position)
      # position is the first pixel we started at.
      img_clone.set_at(position,(0,0,0)) # deactivate pixel
      # now, in a spiralish way, find next pixel
      angle2 = 0
      while True:
         position, br, a = find_brightest_pixel_with_spiral(img_clone,position,radius+3,angle2-180)
         if not position or br < brightness_min:
            break
         #lastdistance = math.pow(math.pow(position[0]-path[-1][0],2) + math.pow(position[1]-path[-1][1],2),0.5)
         #lastangle = 360
         if len(path)>1:
         #   angle1 = math.atan2(position[1]-path[-1][1],position[0]-path[-1][0])
             #angle2 = math.atan2(path[-1][1]-path[-2][1],path[-1][0]-path[-2][0])*180.0/math.pi # !!!
             angle2 = a
         #   lastangle = abs(angle1-angle2)*float(360)/(2*math.pi)
            
         
         #if float(lastdistance)*lastangle > 1:
         if True:
            path.append(position)
         pygame.draw.circle(img_clone, (0,0,0), position, radius, 0)
         
         image_show(display,img_clone,True,(2,1))
         xpaths = paths+[path]
         #pathr1 = image_render_paths(paths,img_clone.get_size(),1,(0,64,0),(128,0,0))
         #pathr2 = image_render_paths([path],img_clone.get_size(),1,(0,128,0),(255,0,0))
         #pathr = blend(pathr1,pathr2)
         #image_show(display,pathr,True,(2,1))
         #image_show(display,image_render_paths(xpaths,img_clone.get_size(),1,(0,64,0),(128,0,0)),True,(2,1))
         image_show(display,render_vector(image_render_paths(xpaths,img_clone.get_size(),1,(0,64,0),(128,0,0)),position,angle2,20),True,(2,1))
         image_save(display,"render/linefollow-%09i.jpg"%render_cnt)
         render_cnt+=1

      if len(path)>2:
         paths.append(path)



   print "found %i paths"%len(paths)

   #paths = pathcombiner(paths)
   #paths = optimizepaths(paths)

   print "optimized to %i paths"%len(paths)

   return paths


if __name__ == "__main__": # test
   print "Testing optimizepaths"


   print "NOT IMPLEMENTED"



   print "Testing pathcombiner"


   path1=[[10,20],[30,45],[50,55],[77,32]]

   path2=[[73,34],[120,47],[170,30],[234,65]]

   path3=[[140,110],[170,120],[220,94],[230,63]]

   path4=[[137,108],[120,80],[70,70],[40,90]]

   path5=[[100,50],[150,60],[200,70],[150,80]]

   # we test by providing a few paths that form a closed loop. they should be wired up correctly.
   # additional paths are provided that are far away and do not match as sanity check.



   test_paths = [path1, path2, path3, path4, path5]

   test_paths2 = test_paths[:]

   test_paths2.reverse() # retry with reverse path order to make other parts of the combiner tick

   print "\ninput paths:"
   for l in test_paths:
      print l

   result_paths = pathcombiner(test_paths)

   print "\noutput paths:"
   for l in result_paths:
      print l
   if len(result_paths) == 2:
      print "found two output paths. correct."
   else:
      print "something went wrong, other than two paths resulted!"

   print "\ninput paths:"
   for l in test_paths2:
      print l

   result_paths = pathcombiner(test_paths2)

   print "\noutput paths:"
   for l in result_paths:
      print l
   if len(result_paths) == 2:
      print "found two output paths. correct."
   else:
      print "something went wrong, other than two paths resulted!"



   print "\n\n"

   print "NOT IMPLEMENTED"



   print "Tesging edgewalk"

   print "NOT IMPLEMENTED"
