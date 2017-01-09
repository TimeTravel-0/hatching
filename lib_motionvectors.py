#!/usr/bin/env python

import pygame
from lib_image_filters import *
from lib_paths import *
import random


def motionprobe(img_in,mask,pos,radius,angle,shift):
   '''probes a motion vector for an specific point/radius'''

   offsetx,offsety = int(math.cos(angle*2*math.pi/360)*shift), int(math.sin(angle*2*math.pi/360)*shift)

   correlation_sum = 0
   correlation_count = 0

   for y in range(pos[1]-radius,pos[1]+radius):
      for x in range(pos[0]-radius,pos[0]+radius):
         distance = pow( pow(y-pos[1],2) + pow(x-pos[0],2) , 0.5)
         if distance < radius: # inside circle
            if x>=0 and y>=0 and x<img_in.get_width() and y<img_in.get_height():
               if sum(mask.get_at((x,y))[:3]) > 128:
                  # in mask
                  x2,y2 = x+offsetx, y+offsety
                  if x2>=0 and y2>=0 and x2<img_in.get_width() and y2<img_in.get_height():
                     color = img_in.get_at((x,y))
                     color2 = img_in.get_at((x2,y2))
                     # the correlation itself (difference between the two picture segments) lower is better
                     correlation = abs(color[0]-color2[0]) + abs(color[1]-color2[1]) + abs(color[2]-color2[2])

                     correlation_sum+=correlation
                     correlation_count+=1

   if correlation_count == 0:
      return -1

   return correlation_sum/correlation_count

def motionfind(img_in,mask,pos,radius):
   '''for one pos, run motionprobe for different angles/shifts'''

   cor_list = []

   min_cor = -1
   min_ang = 0
   min_ofs = 0

   for shift in range(2,radius*2,radius/3): # shift 2 to 20 in 2 steps
      startang = int(random.random()*360)
      for angle in range(0+startang,360+startang,5): # 10 degree steps to probe, start with random one
         cor = motionprobe(img_in,mask,pos,radius,angle,shift)
         print "probing shift %i  angle %i correlation %i position %s  \r"%(shift,angle,cor,str(pos)),

         if cor != -1:
            cor_list.append(cor)
            if cor < min_cor or min_cor == -1:
               min_cor = cor
               min_ang = angle
               min_ofs = shift

   print "\n",
   #print min_ang, min_ofs
   return min_ang%360, min_ofs, min_cor, (max(cor_list)-min(cor_list))

def motionsfind(img_in, mask, radius):
   '''finds points with distance "radius" within the mask and gets motion vectors for each'''

   # point must be in mask and "radius" away from other points
   found_points = []

   mask_clone = pygame.Surface(mask.get_size())
   mask_clone.blit(mask,(0,0))



   while True:
      position = find_pixel_with_color(mask_clone,(255,255,255))
      if not position:
         break
      ang,ofs,cor,corvar = motionfind(img_in, mask, position, radius)
      found_points.append([position,ang,ofs,cor,corvar])
      #print position, ang, ofs
      pygame.draw.circle(mask_clone, (0,0,0), position, radius, 0)

      #
  
   return found_points
   
def motionsfind_visualize(img_in, mask, radius, display):
   '''finds points with distance "radius" within the mask and gets motion vectors for each'''

   # point must be in mask and "radius" away from other points
   found_points = []

   mask_clone = pygame.Surface(mask.get_size())
   mask_clone.blit(mask,(0,0))



   while True:
      position = find_pixel_with_color(mask_clone,(255,255,255))
      if not position:
         break
      ang,ofs,cor,corvar = motionfind(img_in, mask, position, radius)
      found_points.append([position,ang,ofs,cor,corvar])
      #print position, ang, ofs
      pygame.draw.circle(mask_clone, (0,0,0), position, radius, 0)
      
      if cor>0.1:
          image_show(display,render_vector(display, [position[0]*2,position[1]*2], ang, cor*0.2), False, (1,1))  
          image_show(display,render_vector(display, [position[0]*2,position[1]*2], ang+180, cor*0.2), False, (1,1)) 
  
   return found_points
    

def anglecombiner(a1,a2):

   
   a1=a1%180
   a2=a2%180

   #if abs(a1-a2)>180:
   #   a2-=180

   
   return a1,a2


def interpolate_motionvectors(motionvectors, position):
   '''interpolates the given motion vectors for a specified target position'''

   dvpairs = [] # holds distance and vector pairs

   mindist = False
   minvec = False
   for v in motionvectors: # sort by distance and take 3 closest values
      x,y = v[0]
      distance = math.pow(math.pow(position[0]-x,2) + math.pow(position[1]-y,2),0.5)
      dvpairs.append([distance, v])

      if not mindist or distance < mindist :
         mindist = distance
         minvec = v

   sortedpairs = sorted(dvpairs, key=lambda  l:l[0])[:3] # first 3 values of ascending sorted list by distance

   #print sortedpairs

   if sortedpairs[0][0] == 0:
      d1=9999
   else:
      d1 = 1/sortedpairs[0][0]
   if sortedpairs[1][0] == 0:
      d2=9999
   else:
      d2 = 1/sortedpairs[1][0]
   if sortedpairs[2][0] == 0:
      d3 = 9999
   else:
      d3 = 1/sortedpairs[2][0]

   ang1 = sortedpairs[0][1][1]
   ang2 = sortedpairs[1][1][1]
   ang3 = sortedpairs[2][1][1]
   rel1 = sortedpairs[0][1][-1]
   rel2 = sortedpairs[1][1][-1]
   rel3 = sortedpairs[2][1][-1]
   
   ang1,ang2 = anglecombiner(ang1,ang2)
   ang2,ang3 = anglecombiner(ang2,ang3)
   ang3,ang1 = anglecombiner(ang3,ang1)


   avg_ang = (ang1*d1+ang2*d2+ang3*d3)/(d1+d2+d3)

   avg_rel = (rel1*d1+rel2*d2+rel3*d3)/(d1+d2+d3)
   
   #return [ang1,rel1]
   

   return [avg_ang, avg_rel]


   return minvec

def motionvector_rainbow(motionvectors,size):
   '''render motionvectors into a rainbow image (angl. to color mapping)'''
   img = pygame.Surface(size)
   
   for y in range(0,size[1]):
      cw("motionvector rainbow",y,size[1])
      for x in range(0,size[0]):
         v = interpolate_motionvectors(motionvectors,(x,y))
         angle = v[0]
         ampl = v[-1]
         color = angle_to_color(angle*2,ampl)
         img.set_at((x,y),color)
   return img
