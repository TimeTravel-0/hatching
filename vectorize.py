#!/usr/bin/env python
#
# this is ugly, experimental, slow, unoptimized code.
# its purpose is to verify my (propably) stupid idea
# of an "image to hatching pen plotter drawing".
#
# we start with a few simple image manipulation functions:
#

def load_image(input_file):
   '''loads an image via pygame and returns the image object'''
   return pygame.image.load(input_file)

def blacknwhite(img_in,limit=32):
   '''converts an image to black and white pixels'''
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      for x in range(0,width):
         color_in = img_in.get_at((x,y))

         color_out = (255,255,255)
         if color_in[0]+color_in[1]+color_in[2] < limit*3:
            color_out = (0,0,0)

         img_out.set_at((x,y),color_out)
   return img_out

def get_maximum_brightness(img_in,pos,radius):
   '''returns the average color of a circular area'''
   width = radius*2
   height = radius*2

   brightness_max = 0

   for y in range(pos[1]-radius,pos[1]+radius):
      for x in range(pos[0]-radius,pos[0]+radius):
         distance = pow( pow(y-pos[1],2) + pow(x-pos[0],2) , 0.5)
         if distance < radius+0.5: # inside circle
            if x>=0 and y>=0 and x<img_in.get_width() and y<img_in.get_height():
               color = img_in.get_at((x,y))
               brightness = sum(color[:3])/3
        
               if brightness>brightness_max:
                  brightness_max = brightness
   return brightness_max

def get_average_brightness(img_in,pos,radius):
   '''returns the average color of a circular area'''
   width = radius*2
   height = radius*2

   brightness_divisor = 0
   brightness_sum = 0

   for y in range(pos[1]-radius,pos[1]+radius):
      for x in range(pos[0]-radius,pos[0]+radius):
         distance = pow( pow(y-pos[1],2) + pow(x-pos[0],2) , 0.5)
         if distance < radius: # inside circle
            if x>=0 and y>=0 and x<img_in.get_width() and y<img_in.get_height():
               color = img_in.get_at((x,y))
               brightness = sum(color[:3])/3
        
               brightness_sum+=brightness
               brightness_divisor+=1
   if brightness_divisor>0:
      return brightness_sum / brightness_divisor
   else:
      return 255

def edgedetect(img_in, r=1, offset=(0,0)):
   '''detects edges and marks them'''
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      for x in range(0,width):
         color_in = img_in.get_at((x,y))
         brightness_in = sum(color_in[:3])/3
         brightness_avg = get_average_brightness(img_in, (x-offset[0],y-offset[1]), r)
         brightness_difference = abs(brightness_in - brightness_avg)
         if brightness_difference > 255:
            brightness_difference = 255
         color_out = [brightness_difference]*3

         img_out.set_at((x,y),color_out)
   return img_out

def blur(img_in, r=3):
   '''detects edges and marks them'''
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      for x in range(0,width):
         color_in = img_in.get_at((x,y))
         brightness_in = sum(color_in)/3
         brightness_avg = get_average_brightness(img_in, (x,y), r)
         #print brightness_avg
         color_out = [brightness_avg]*3

         img_out.set_at((x,y),color_out)
   return img_out

def blend(img1,img2):
   width,height = img1.get_size()
   img_out = pygame.Surface(img1.get_size())
   for y in range(0,height):
      for x in range(0,width):
         color_in1 = img1.get_at((x,y))
         color_in2 = img2.get_at((x,y))
         brightness_in = max(max(color_in1[:2]),max(color_in2[:2]))
         color_out = [brightness_in]*3

         img_out.set_at((x,y),color_out)
   return img_out



def bolden(img_in, r=3):
   '''detects edges and marks them'''
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      for x in range(0,width):
         color_in = img_in.get_at((x,y))
         brightness_in = sum(color_in)/3
         brightness_max = get_maximum_brightness(img_in, (x,y), r)
         color_out = [brightness_max]*3

         img_out.set_at((x,y),color_out)
   return img_out


def find_pixel_with_color(img_in, color):
   '''returns the 1st coordinate of a pixel of specified color'''
   width,height = img_in.get_size()
   for y in range(0,height):
      for x in range(0,width):
         color_in = img_in.get_at((x,y))
         if color[:2] == color_in[:2]:
            # found.
            return (x,y)
   return False


def floodfill(img_in,startpos,color):
   '''floodfill from position with color'''
   positions_todo = [] # list of points to draw/check
   positions_todo.append(startpos)

   pixelcounter = 0

   width, height = img_in.get_size()

   startcolor = img_in.get_at(startpos)
   while len(positions_todo)>0:
      #print len(positions_todo)

      # get point from list:
      pos=positions_todo.pop()
      img_in.set_at(pos, color)
      pixelcounter+=1
      # offsets to try
      offsets = [[1,0],[0,1],[-1,0],[0,-1]]
      for offset in offsets:
         trypos = (pos[0]+offset[0],pos[1]+offset[1])
         #print trypos
         if trypos[0]>=0 and trypos[1]>=0 and trypos[0]<width and trypos[1]<height:
            if img_in.get_at(trypos) == startcolor: # color at offset is same as on start
               positions_todo.append(trypos)

   return pixelcounter


def main():
   if len(sys.argv)==2: # 1 parameters



      # the idea is as follows:
      # 1. find/mark edges, because edges mark areas

      input_file = sys.argv[1]
      img_in = load_image(input_file)

      #img_in = blur(img_in,1)

      pygame.init()
      insize = img_in.get_size()
      display = pygame.display.set_mode((insize[0]*3,insize[1]*3))

      display.blit(img_in,(0,0))
      pygame.display.flip()

      img_edge1 = edgedetect(img_in,1,(1,0))
      display.blit(img_edge1,(insize[0],0))
      pygame.display.flip()

      img_edge2 = edgedetect(img_in,1,(0,1))
      display.blit(img_edge2,(insize[0]*2,0))
      pygame.display.flip()

      img_blend = blend(img_edge1, img_edge2)
      display.blit(img_blend,(0,insize[1]))
      pygame.display.flip()

      img_bold = bolden(img_blend,1)
      display.blit(img_bold,(insize[0],insize[1]))
      pygame.display.flip()

      img_bnw = blacknwhite(img_bold,25)
      display.blit(img_bnw,(insize[0]*2,insize[1]))
      pygame.display.flip()

      # 2. for the room between edges: flood fill until no space left

      facecount = 0

      while True:
         position = find_pixel_with_color(img_bnw,(0,0,0))
         if not position:
            break
         #print position
         pixelcount = floodfill(img_bnw, position, (random.random()*253+1,random.random()*255,random.random()*255))
         if pixelcount < 50:
            floodfill(img_bnw, position, (255,255,255))
         else:
            facecount+=1

         display.blit(img_bnw,(insize[0]*2,insize[1]))
         pygame.display.flip()



      print "filled %i faces"%facecount

      pygame.image.save(img_bnw,"tmp-"+sys.argv[1])

      # 3. with each flood fill a seperate area/mask is defined

      # 4. for each mask, apply to original image and do a simple auto-correlation:
      # 4.1: first by xy offset (varied) but 0deg rotation: peak = hatching direction
      # 4.2: 2nd by xy offset (from 4.1) but rotation varied: peak = defines slight bend






      pygame.display.flip()
      time.sleep(10)

if __name__ == "__main__":
   import pygame
   import sys
   import time
   import math
   import random
   main()
