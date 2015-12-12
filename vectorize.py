#!/usr/bin/env python
#
# this is ugly, experimental, slow, unoptimized code.
# its purpose is to verify my (propably) stupid idea
# of an "image to hatching pen plotter drawing".
#
# for now the script finds edges and fills areas in between
# with random colors
# edge detection works as expected, but drawn edges
# (black lines...) are not handled in a special way
# = handled like a normal area/fill = results in double
# lines detected
#
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

         # slow like hell. generate one blured image and diff them would be better
         #avgb = get_average_brightness(img_in,(x,y),32) # radius 3

         #limit = avgb/2	

         color_out = (255,255,255)
         if color_in[0]+color_in[1]+color_in[2] < limit*3:
            color_out = (0,0,0)

         img_out.set_at((x,y),color_out)
   return img_out

def get_median_color(img_in,pos,radius, mode = "g"):
   '''returns the average color of a circular area'''
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

   # brightness approach

   if mode == "g":
      brightness = []
      for color in colors:
         brightness.append(color[0]+color[1]+color[2])
   
      combined = zip(colors, brightness)
      combined.sort()
      colors_sorted = [item[0] for item in combined]
      median_color = colors_sorted[len(colors_sorted)/2]

   return median_color


def median(img_in, radius, mode):
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      for x in range(0,width):
         color_out = get_median_color(img_in,(x,y),radius,mode)
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
   '''take max val for each pixel from each image'''
   width,height = img1.get_size()
   img_out = pygame.Surface(img1.get_size())
   for y in range(0,height):
      for x in range(0,width):
         color_in1 = img1.get_at((x,y))
         color_in2 = img2.get_at((x,y))

         color_out = [max(color_in1[0],color_in2[0]),max(color_in1[1],color_in2[1]),max(color_in1[2],color_in2[2])]

         img_out.set_at((x,y),color_out)
   return img_out



def bolden(img_in, r=3):
   '''draw along maximum brightness with circle radius r'''
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

def id_to_color(id):
   return (id%254+1,(id/254)%255,(id/254/255)%255)

def color_to_id(color):
   return color[0]-1 + color[1]*255 + color[2]*255*255


def mask(img_in, color_mask):
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      for x in range(0,width):
         color_in = img_in.get_at((x,y))
         if color_in[:2] == color_mask[:2]: # color of img is same as color specified, copy!
            color_out = (255,255,255)
         else:
            color_out = (0,0,0)
         img_out.set_at((x,y), color_out)
   return img_out

def get_avg_color(img_in, mask):
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

def gen_single_color(size, color):
   img_out = pygame.Surface(size)
   img_out.fill(color)
   return img_out

def multiply(img_in1, img_in2):
   width,height = img_in1.get_size()
   img_out = pygame.Surface(img_in1.get_size())
   for y in range(0,height):
      for x in range(0,width):
         color_in1 = img_in1.get_at((x,y))
         color_in2 = img_in2.get_at((x,y))
         color_out = [ color_in1[0] * color_in2[0] / 255 , color_in1[1] * color_in2[1] / 255 , color_in1[2] * color_in2[2] / 255 ] 
         img_out.set_at((x,y), color_out)
   return img_out


def main():
   if len(sys.argv)==2: # 1 parameters



      # the idea is as follows:
      # 1. find/mark edges, because edges mark areas

      input_file = sys.argv[1]
      img_in = load_image(input_file)

      #img_in = blur(img_in,3)

      img_in = median(img_in,3,"c")

      pygame.init()
      insize = img_in.get_size()
      display = pygame.display.set_mode((insize[0]*3,insize[1]*3))

      display.blit(img_in,(0,0))
      pygame.display.flip()

      img_edge1 = edgedetect(img_in,1,(1,0))
      display.blit(img_edge1,(insize[0],0))
      pygame.display.flip()

      img_edge2 = edgedetect(img_in,1,(0,1))
      display.blit(img_edge2,(insize[0]*1,0))
      pygame.display.flip()

      img_blend = blend(img_edge1, img_edge2)
      display.blit(img_blend,(insize[0]*1,insize[1]*0))
      pygame.display.flip()

      img_bold = bolden(img_blend,1)
      display.blit(img_bold,(insize[0]*2,insize[1]*0))
      pygame.display.flip()

      img_bnw = blacknwhite(img_bold,10)
      display.blit(img_bnw,(insize[0]*0,insize[1]*1))
      pygame.display.flip()

      # 2. for the room between edges: flood fill until no space left

      facecount = 0

      while True:
         position = find_pixel_with_color(img_bnw,(0,0,0))
         if not position:
            break
         #print position
         pixelcount = floodfill(img_bnw, position, id_to_color(facecount))
         if pixelcount < 50:
            floodfill(img_bnw, position, (255,255,255))
         else:
            facecount+=1

         display.blit(img_bnw,(insize[0]*0,insize[1]*1))
         pygame.display.flip()



      print "filled %i faces"%facecount


      # 3. with each flood fill a seperate area/mask is defined
      masks = []
      masks_drawtmp = pygame.Surface(img_bnw.get_size())
      for i in range(0,facecount):
         masks.append(bolden( mask(img_bnw,id_to_color(i)) ,2))
         masks_drawtmp = blend(masks_drawtmp, masks[i])
         display.blit(masks_drawtmp,(insize[0]*1,insize[1]*1))
         pygame.display.flip()


      # 4. get average brightness from this area, check for gradient

      masked_originals = []
      masked_originals_drawtmp = pygame.Surface(img_bnw.get_size())
 
      for i in range(0,facecount):
         avgcolor = get_avg_color(img_in, masks[i])
         print avgcolor
         masked_originals.append(   multiply(  gen_single_color(img_bnw.get_size(),avgcolor), masks[i])     )
         #masked_originals.append(multiply(masks[i],img_in))
         masked_originals_drawtmp = blend(masked_originals_drawtmp, masked_originals[i])
         display.blit(masked_originals_drawtmp,(insize[0]*1,insize[1]*1))
         pygame.display.flip()

      pygame.image.save(masked_originals_drawtmp,"tmp-"+sys.argv[1])


      # todo.

      # 5. for each mask, apply to original image and do a simple auto-correlation:
      # 5.1: first by xy offset (varied) but 0deg rotation: peak = hatching direction
      # 5.2: 2nd by xy offset (from 4.1) but rotation varied: peak = defines slight bend

      # todo.

      # 6. generate strokes/hatching for each area. it is not necessary to know the area outline as polygon, just check the individual pixels

      # todo.

      # 7. generate strokes for borders.

      # todo.



      pygame.display.flip()
      time.sleep(10)

if __name__ == "__main__":
   import pygame
   import sys
   import time
   import math
   import random
   main()
