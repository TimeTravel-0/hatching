#!/usr/bin/env python

from console import *
from colors import *
import pygame

def blacknwhite(img_in,limit=32):
   '''converts an image to black and white pixels by threshold'''
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      cw("blacknwhite",y,height)
      for x in range(0,width):
         color_in = img_in.get_at((x,y))

         # slow like hell. generate one blured image and diff them would be better
         #avgb = get_average_brightness(img_in,(x,y),32) # radius 3

         #limit = avgb/2	

         color_out = (255,255,255)
         if color_in[0]+color_in[1]+color_in[2] < limit*3:
            color_out = (0,0,0)

         img_out.set_at((x,y),color_out)
   return img_out
   
# needs avg brightness!
def blur(img_in, r=3):
   '''blurs an image with defined averaging radius'''
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      cw("blur",y,height)
      for x in range(0,width):

         brightness_avg = get_average_brightness(img_in, (x,y), r)

         color_avg = [brightness_avg]*3

         color_out = color_avg

         img_out.set_at((x,y),color_out)
   return img_out

def lazyblur(img_in, r=3):
   '''blurs an image with defined averaging radius'''
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())

   # for each direction x/y +/- do running average per r,g,b

   sm = 1-1/float(r)

   # x positive
   img_blur1 = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      cw("lazyblur a",y,height)
      r,g,b = img_in.get_at((0,y))[:3]
      for x in range(0,width):
         r2,g2,b2 = img_in.get_at((x,y))[:3]
         r=float(r*sm)+float(r2*(1-sm))
         g=float(g*sm)+float(g2*(1-sm))
         b=float(b*sm)+float(b2*(1-sm))
         img_blur1.set_at((x,y),(r,g,b))

   # x negative
   img_blur2 = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      cw("lazyblur b",y,height)
      r,g,b = img_in.get_at((width-1,y))[:3]
      for x in list(reversed(range(0,width))):
         r2,g2,b2 = img_in.get_at((x,y))[:3]
         r=float(r*sm)+float(r2*(1-sm))
         g=float(g*sm)+float(g2*(1-sm))
         b=float(b*sm)+float(b2*(1-sm))
         img_blur2.set_at((x,y),(r,g,b))

   # y positive
   img_blur3 = pygame.Surface(img_in.get_size())
   for x in range(0,width):
      cw("lazyblur c",x,width)
      r,g,b = img_in.get_at((x,0))[:3]
      for y in range(0,height):
         r2,g2,b2 = img_in.get_at((x,y))[:3]
         r=float(r*sm)+float(r2*(1-sm))
         g=float(g*sm)+float(g2*(1-sm))
         b=float(b*sm)+float(b2*(1-sm))
         img_blur3.set_at((x,y),(r,g,b))

   # y negative
   img_blur4 = pygame.Surface(img_in.get_size())
   for x in range(0,width):
      cw("lazyblur d",x,width)
      r,g,b = img_in.get_at((x,height-1))[:3]
      for y in list(reversed(range(0,height))):
         r2,g2,b2 = img_in.get_at((x,y))[:3]
         r=float(r*sm)+float(r2*(1-sm))
         g=float(g*sm)+float(g2*(1-sm))
         b=float(b*sm)+float(b2*(1-sm))
         img_blur4.set_at((x,y),(r,g,b))

   img_out = addmul( addmul(img_blur1,img_blur2,0.5,0.5) , addmul(img_blur3,img_blur4,0.5,0.5) , 0.5,0.5)

   return img_out



def blend(img1,img2):
   '''take max val for each pixel from each image'''
   width,height = img1.get_size()
   img_out = pygame.Surface(img1.get_size())
   for y in range(0,height):
      cw("blend",y,height)
      for x in range(0,width):
         color_in1 = img1.get_at((x,y))
         color_in2 = img2.get_at((x,y))

         color_out = [max(color_in1[0],color_in2[0]),max(color_in1[1],color_in2[1]),max(color_in1[2],color_in2[2])]

         img_out.set_at((x,y),color_out)
   return img_out

def addmul(img1,img2,m=1,n=1):
   '''img1 *n + img2*m'''
   width,height = img1.get_size()
   img_out = pygame.Surface(img1.get_size())
   for y in range(0,height):
      cw("addmul",y,height)
      for x in range(0,width):
         color_in1 = img1.get_at((x,y))
         color_in2 = img2.get_at((x,y))

         color_out = [lcol(color_in1[0]*n+color_in2[0]*m),lcol(color_in1[1]*n+color_in2[1]*m),lcol(color_in1[2]*n+color_in2[2]*m)]

         img_out.set_at((x,y),color_out)
   return img_out




def floodfill(img_in,startpos,color):
   '''floodfill from position with color'''
   positions_todo = [] # list of points to draw/check
   positions_todo.append(startpos)

   pixelcounter = 0

   width, height = img_in.get_size()

   startcolor = img_in.get_at(startpos)
   while len(positions_todo)>0:

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

def mask(img_in, color_mask):
   '''create mask (if color at pixel = function parameter white, else black)'''
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      cw("mask",y,height)
      for x in range(0,width):
         color_in = img_in.get_at((x,y))
         if color_in[:2] == color_mask[:2]: # color of img is same as color specified, copy!
            color_out = (255,255,255)
         else:
            color_out = (0,0,0)
         img_out.set_at((x,y), color_out)
   return img_out
   
def multiply(img_in1, img_in2):
   '''img1 * img2'''
   width,height = img_in1.get_size()
   img_out = pygame.Surface(img_in1.get_size())
   for y in range(0,height):
      cw("multiply",y,height)
      for x in range(0,width):
         color_in1 = img_in1.get_at((x,y))
         color_in2 = img_in2.get_at((x,y))
         color_out = [ color_in1[0] * color_in2[0] / 255 , color_in1[1] * color_in2[1] / 255 , color_in1[2] * color_in2[2] / 255 ] 
         img_out.set_at((x,y), color_out)
   return img_out

