#!/usr/bin/env python

from lib_console import *
from lib_colors import *
from lib_imagefile import *

import math
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

# works on image, so image function
import colorsys
def get_median_color(img_in,pos,radius, mode = "g", borders=4):
   '''returns the median color of a circular area'''
   width = radius*2
   height = radius*2

   colors = []

   for y in range(pos[1]-radius,pos[1]+radius):
      for x in range(pos[0]-radius,pos[0]+radius):
         distance = pow( pow(y-pos[1],2) + pow(x-pos[0],2) , 0.5)
         if distance < radius+0.5: # inside circle
            if x>=0 and y>=0 and x<img_in.get_width() and y<img_in.get_height():
               color = img_in.get_at((x,y))
               
               colors.append(color)

   # sort colors by some means 

   # single color approach

   if mode == "c":

      color_r = [key[0] for key in colors]
      color_g = [key[1] for key in colors]
      color_b = [key[2] for key in colors]

      color_r.sort()
      color_g.sort()
      color_b.sort()

      median_color = color_r[len(color_r)/2], color_g[len(color_g)/2], color_b[len(color_b)/2]

      border_offset = borders

      idx_prev = len(color_r)/2-border_offset
      idx_next = len(color_r)/2+border_offset
      if idx_prev <0:
         idx_prev = 0
      if idx_next > len(color_r)-1:
         idx_next = -1


      prev_color = color_r[idx_prev], color_g[idx_prev], color_b[idx_prev]
      next_color = color_r[idx_next], color_g[idx_next], color_b[idx_next]

      contrast_color = [abs(prev_color[0]-next_color[0]), abs(prev_color[1]-next_color[1]),abs(prev_color[2]-next_color[2]) ]

      prev_hsv = colorsys.rgb_to_hsv(prev_color[0],prev_color[1],prev_color[2])
      next_hsv = colorsys.rgb_to_hsv(next_color[0],next_color[1],next_color[2])

      hue_difference = abs(prev_hsv[0]-next_hsv[0])*360.0/(2*math.pi)

      saturation_difference = abs(prev_hsv[1]-next_hsv[1])

      if hue_difference>180:
         hue_difference = 360-hue_difference

      hue_difference = hue_difference*255/180 # normalize...
      #print hue_difference, prev_hsv, next_hsv
      #if saturation_difference>0:
      #   print saturation_difference

      contrast_color.append(hue_difference*saturation_difference)

   # brightness approach

   if mode == "g":
      brightness = []
      for color in colors:
         brightness.append(color[0]+color[1]+color[2])
   
      combined = zip(colors, brightness)
      combined.sort()
      colors_sorted = [item[0] for item in combined]
      median_color = colors_sorted[len(colors_sorted)/2]

   return median_color, contrast_color



# works on image, so image function
def median(img_in, radius, mode, borders):
   '''applies median filter to an image'''
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   img_border = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      cw("median",y,height)

      for x in range(0,width):
         color_out, color_contrast = get_median_color(img_in,(x,y),radius,mode,borders)
         img_out.set_at((x,y),color_out)
         color_contrast = [max(color_contrast)]*3
         img_border.set_at((x,y),color_contrast)

   return img_out, img_border


# works on image, so image function
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


# works on image, so image function
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

def get_avg_color(img_in, mask):
   '''get average color for mask area'''
   width,height = img_in.get_size()
   color_avg_sum = [0,0,0]
   color_avg_cnt = 0
   for y in range(0,height):
      for x in range(0,width):
         if max(mask.get_at((x,y))[:2]) > 128:
            # mask slected
            color_in = img_in.get_at((x,y))
            color_avg_sum[0]+=color_in[0]
            color_avg_sum[1]+=color_in[1]
            color_avg_sum[2]+=color_in[2]
            color_avg_cnt+=1
   if color_avg_cnt == 0:
      return [0,0,0]
   return [color_avg_sum[0]/color_avg_cnt, color_avg_sum[1]/color_avg_cnt, color_avg_sum[2]/color_avg_cnt]



# works on image, so image function
# propably old unused code?
def edgedetect(img_in, r=1, offset=(0,0)):
   '''detects edges and marks them'''
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      cw("edge detect",y,height)
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

# image_filters
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

def bolden(img_in, r=3):
   '''draw along maximum brightness with circle radius r'''
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      cw("bolden",y,height)
      for x in range(0,width):
         color_in = img_in.get_at((x,y))
         brightness_in = sum(color_in)/3
         brightness_max = get_maximum_brightness(img_in, (x,y), r)
         color_out = [brightness_max]*3

         img_out.set_at((x,y),color_out)
   return img_out

def count_pixels_with_color(img_in, color):
   '''returns the count of pixels of specified color'''
   count = 0
   width,height = img_in.get_size()
   for y in range(0,height):
      for x in range(0,width):
         color_in = img_in.get_at((x,y))
         if color[:2] == color_in[:2]:
            # found.
            count+=1
   return count


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

def find_brightest_pixel(img_in):
   '''returns the coordinate of brightest pixel found'''

   maxbr = 0
   maxpos = False

   width,height = img_in.get_size()
   for y in range(0,height):
      for x in range(0,width):
         color_in = img_in.get_at((x,y))
         brightness = sum(color_in[:2])/3
         if brightness > maxbr:
            maxbr = brightness
            maxpos = (x,y)
   return maxpos, maxbr


def find_brightest_pixel_with_spiral(img_in,startpos,maxlen,startang):
   '''returns the coordinate of brightest pixel in spiral described by startpos, maxlen, startang'''
   width,height = img_in.get_size()

   maxbr = 0
   maxpos = False
   maxang = startang

   for r in range(1,maxlen):
      for a in range(0+int(startang),360+int(startang)):
         probepos = [int(startpos[0] + math.cos(a*2*math.pi/360)*r),int(startpos[1] + math.sin(a*2*math.pi/360)*r) ]
         x,y = probepos
         if x>=0 and y>=0 and x<width and y<height:
               color = img_in.get_at((x,y))

               brightness = sum(color[:2])/3
               if brightness > maxbr:
                  maxbr = brightness
                  maxpos = probepos
                  maxang = a
   return maxpos, maxbr, maxang

         
def image_filter_zoomgrid(img_in,zoom=10,spacing=1):
   new_img = image_create((img_in.get_width()*zoom,img_in.get_height()*zoom),(128,0,128))
   for y in range(0,img_in.get_height()):
      for x in range(0,img_in.get_width()):
         in_col = img_in.get_at((x,y))
         for yy in range(0,zoom-spacing):
            for xx in range(0,zoom-spacing):
               new_img.set_at((x*zoom+xx,y*zoom+yy),in_col)
   return new_img


def image_gausscircle(img_in,position=[0,0],radius=10.0,color=[0,0,0],intensity=0.5): # works on input image!
   for x in range(position[0]-radius,position[0]+radius):
      for y in range(position[1]-radius,position[1]+radius):
         if x<0 or x>img_in.get_width():
            break
         if y<0 or y>img_in.get_height():
            break
        
         in_col = img_in.get_at((x,y))
         
         distance_from_center = ( (x-position[0])**2 + (y-position[1])**2 )**0.5
         distance_from_center_relative = distanc_from_center / radius
         
         if distance_from_center_relative > 1.0:
            break
         inverse_distance_from_center_relative = 1.0 - distance_from_center_relative
               
         new_col = color
         
         mix_ratio_new = ( 1.0 * inverse_distance_from_center_relative**2 ) * intensity
         mix_ratio_old = 1.0 - mix_ratio_new
         
         out_col = [ in_col[0]*mix_ratio_old + new_col[0]*mix_ratio_new, in_col[1]*mix_ratio_old + new_col[1]*mix_ratio_new, in_col[2]*mix_ratio_old + new_col[2]*mix_ratio_new ] 
         
         img_in.set_at((x,y),out_col)
   return img_in
         
