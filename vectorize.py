#!/usr/bin/env python
#
# this is ugly, experimental, slow, unoptimized code.
# its purpose is to verify my (propably) stupid idea
# of an "image to hatching pen plotter drawing".
#
# for now the script finds edges and fills areas in between
# with colors
# edge detection works as expected, but drawn edges
# (black lines...) are not handled in a special way
# = handled like a normal area/fill = results in double
# lines detected for comic like input drawings
#
# motion vector recovery works ok-ish.
#
# this script now generates lots of data from an image file
# next, yet unimplemented, step is to combine all this data
# and generate polygon lines
#
# another, yet unimplemented, part is to write all the polygons
# out in HPGL form.
#
#
# see main() function for actual high level description of what is going on
#
# we start with a few simple image manipulation functions:
#

import sys

from lib_console import *

from lib_gui_eyecandy import *
from lib_imagefile import *
from lib_colors import *
from lib_image_filters import *
from lib_paths import *
from lib_motionvectors import *




from lib_hpgl import *









def facewalk(img_in, mask, motionvectors):
   '''trace hatching paths'''
   mask_clone = pygame.Surface(mask.get_size())
   mask_clone.blit(mask,(0,0))

   radius = 5

   paths = []

   width, height = mask_clone.get_size()

   while True:
      path = []
      position = find_pixel_with_color(mask_clone,(255,255,255))
      if not position:
         break

      path.append(position)

      mask_clone.set_at(position,(0,0,0)) # deactivate pixel
      # now, find next pixel
      while True:
         vector = interpolate_motionvectors(motionvectors,position)
         angle = vector[1]
         #print "!!!",vector
         dp = [math.cos(angle*2*math.pi/360)*radius,math.sin(angle*2*math.pi/360)*radius]
         position = [position[0]+int(dp[0]),position[1]+int(dp[1])]

         if position[0]<0 or position[0]>width-1 or position[1]<0 or position[1]>height-1:
            break
         if mask_clone.get_at(position) == (0,0,0):
            break
         path.append(position)
         mask_clone.set_at(position,(0,0,0))
         pygame.draw.circle(mask_clone, (0,0,0), position, radius-1, 0)



      paths.append(path)
   return paths
                  


def main():
   '''main routine'''
   if len(sys.argv)>=2: # 1 parameters

      pygame.init()



      # the idea is as follows:
      # 1. find/mark edges, because edges mark areas

      input_file = sys.argv[1]


      bnw_mode = False
      if len(sys.argv)>=3:
          bnw_mode = (sys.argv[2]=="bw")

      img_in = image_load(input_file)
      insize = img_in.get_size()

      maxdsize = [1024,600]

      dsize = [insize[0]*4,insize[1]*4]
      inratio = float(insize[1])/float(insize[0])
      if dsize[0]>maxdsize[0]:
         dsize[0]=maxdsize[0]
         dsize[1]=int(dsize[0]*inratio)
      if dsize[1]>maxdsize[1]:
         dsize[1]=maxdsize[1]
         dsize[0]=int(dsize[1]/inratio)
 
      
      display = pygame.display.set_mode(dsize)


      ### motion vector rainbow test
      if False:
         vectors = []
         for y in range(0,500,50):
             for x in range(0,500,50):
                 vec = [[x,y],math.atan2(x-250,y-250)*360/math.pi,0,0,0,1]
                 #vec = [[x,y],random.random()*360,0,0,0,1]
                 vectors.append(vec)

         motionvector_r = motionvector_rainbow(vectors,(500,500))
         show_image(display, motionvector_r, True)
         image_save(motionvector_r,"vectom-test.png")


      ###


      show_image(display, img_in, False)

      #img_blurx = lazyblur(img_in,3)
      #show_image(display,img_blurx, True)
      #time.sleep(5)


      # a) first we run an median filter to get rid of noise but keep edges
      # as the median filter already gets a list of all pixels around the analyzed coordinate
      # it got an additional part to calculate the contrast.

      if bnw_mode == False:
         img_in, img_border = median(img_in,3,"c",3)
         show_image(display, img_in, True)
         show_image(display, img_border, True)
         image_save(img_border,fn_comb(sys.argv[1],"bordem"))
      else:
         # just create inverted image...
         img_white = image_show(img_in.get_size(),(255,255,255))
         img_border = addmul(img_in,img_white,1.0,-1.0)
         show_image(display, img_border, True)




      # b) edge detection in x direction
      #img_edge1 = edgedetect(img_in,1,(1,0))
      #show_image(display, img_edge1, True)

      # c) edge detection in y direction
      #img_edge2 = edgedetect(img_in,1,(0,1))
      #show_image(display, img_edge2, False)

      # d) blend x and y edge detection images
      #img_blend = blend(img_edge1, img_edge2)
      #show_image(display, img_blend, False)

      #image_save(img_blend,"border-"+sys.argv[1])

      img_blend = img_border 

      # e) create blured image (average of local area)
      img_blur = img_blend
      for i in range(0,3):
         img_blur = lazyblur(img_blur, 3)
         show_image(display, img_blur, False)

      # f) unblured - blured edge image = better image for threshold usage (adapts to local variations)
      img_blurdif = addmul(img_blend, img_blur, -1)
      show_image(display, img_blurdif, True)




      # j) walk the line

      edgepaths = edgewalk(img_blurdif)
      rz=4
      rendersize = [img_in.get_size()[0]*rz,img_in.get_size()[1]*rz]
      img_edgepath = pygame.Surface(rendersize)
      for polygon in edgepaths:
         lastpoint = False
         if len(polygon)>1:
            for point in polygon:
               if not lastpoint:
                  lastpoint = point
               pygame.draw.circle(img_edgepath, (0,128,0),[point[0]*rz,point[1]*rz], 5)
               pygame.draw.line(img_edgepath, (255,0,0), [lastpoint[0]*rz,lastpoint[1]*rz], [point[0]*rz,point[1]*rz], 1)
               lastpoint = point

      show_image(display, img_edgepath, True)
      image_save(img_edgepath,fn_comb(sys.argv[1],"epath"))



      c = hpgl_usepen(1,(0,0,0))
      c+= hpgl_frompaths(edgepaths)
      hpgl_tofile(c, fn_comb(sys.argv[1],"epath","hpgl"))

      # print edge paths 




      # g) bolden edges
      img_bold = bolden(img_blurdif,1)
      show_image(display, img_bold, True)

      # h) convert to black and white via limit
      img_bnw = blacknwhite(img_bold,12)  
      show_image(display, img_bnw, True)
      show_image(display, img_bnw, True)


      # i) isles smaller than limit get eliminated
      while True:
         position = find_pixel_with_color(img_bnw,(255,255,255))
         if not position:
            break
         pixelcount = floodfill(img_bnw, position, (128,128,128))
         if pixelcount < 100:
            print "isle at %s, %i pixels below limit"%(str(position), pixelcount)
            floodfill(img_bnw, position, (0,0,0)) # eliminate it

      img_bnw = blacknwhite(img_bnw,4)



      # 2. for the room between edges: flood fill until no space left

      facecount = 0

      while True:
         position = find_pixel_with_color(img_bnw,(0,0,0))
         if not position:
            break
         #print position
         pixelcount = floodfill(img_bnw, position, id_to_color(facecount))
         if pixelcount < 25:
            print "isle at %s, %i pixels below limit"%(str(position), pixelcount)
            floodfill(img_bnw, position, (255,255,255))
         else:
            facecount+=1
         show_image(display, img_bnw, False)

      print "filled %i faces"%facecount


      # 3. with each flood fill a seperate area/mask is defined
      masks = []
      masks_drawtmp = pygame.Surface(img_bnw.get_size())
      for i in range(0,facecount):
         masks.append(bolden( mask(img_bnw,id_to_color(i)) ,2))
         masks_drawtmp = blend(masks_drawtmp, masks[i])
         show_image(display, masks_drawtmp, False)


      # 4. get average brightness from this area

      masked_originals = []
      masked_originals_drawtmp = pygame.Surface(img_bnw.get_size())

      avgcolors = []
 
      for i in range(0,facecount):
         avgcolor = get_avg_color(img_in, masks[i])
         avgcolors.append(avgcolor)
         print avgcolor
         masked_originals.append(   multiply(  image_show(img_bnw.get_size(),avgcolor), masks[i])     )
         #masked_originals.append(multiply(masks[i],img_in))
         masked_originals_drawtmp = blend(masked_originals_drawtmp, masked_originals[i])

         show_image(display, masked_originals_drawtmp, False)

      image_save(masked_originals_drawtmp,fn_comb(sys.argv[1],"tmp"))


      # 5. motion vector find
      motionvector_drawtmp = pygame.Surface(img_bnw.get_size())


      motionvectorss = []
      for i in range(0,facecount):
         print "motion vector face %i"%i
         motionvectors = motionsfind(img_in, bolden(masks[i],5),10) # 10px radius
         motionvectorss.append(motionvectors)





         cormax = 0
         corvar_max = 0
         for vector in motionvectors:
            pos,ang,ofs,cor,corvar = vector

            # correlation: smaller = smaller difference in picture comparison 0 = identical, which is good
            # corvar: correlation variance, bigger =  better because we dont just probe signle colored surface...
            #
            
            # correlation needs normalisation
            if cormax<cor:
               cormax=cor

            if corvar_max<corvar:
               corvar_max=corvar

         for vector in motionvectors:
            pos,ang,ofs,cor,corvar = vector

            # brightness of contrast image correlates to "roughness" at this location
            #roughness = float(255-max(img_blur.get_at(pos)[:2]))/255

            rel_cor = float(cor)/float(cormax)
            rel_corvar = float(corvar)/float(corvar_max)
            ofs=ofs*(1-rel_cor) * rel_corvar
            vector.append(ofs)

            ofs+=5

            if ofs>0:
               endpos = math.cos(ang*2*math.pi/360)*ofs+pos[0],math.sin(ang*2*math.pi/360)*ofs+pos[1]
               pygame.draw.line(motionvector_drawtmp, avgcolors[i], pos, endpos, 1)

         show_image(display, motionvector_drawtmp, True)
      image_save(motionvector_drawtmp,fn_comb(sys.argv[1],"vector"))


      combv = []
      for motionvectors in motionvectorss:
         combv+=motionvectors
      #print combv
      motionvector_r = motionvector_rainbow(combv,img_bnw.get_size())
      show_image(display, motionvector_r, True)
      image_save(motionvector_r,fn_comb(sys.argv[1],"vectom"))

     


      # 6. generate strokes/hatching for each area. it is not necessary to know the area outline as polygon, just check the individual pixels


      img_strokepath = pygame.Surface(img_in.get_size())
      strokepathss = []
      #if False:
      for i in range(0,len(masks)):
         strokepaths = facewalk(img_in, masks[i], motionvectorss[i])
         for polygon in strokepaths:
            lastpoint = False
            if len(polygon)>1:
               for point in polygon:
                  if not lastpoint:
                     lastpoint = point
                  #pygame.draw.circle(img_strokepath, (0,255,0),point, 3)
                  pygame.draw.line(img_strokepath, avgcolors[i], lastpoint, point, 1)
                  lastpoint = point
         strokepathss.append(strokepaths)

      show_image(display, img_strokepath, True)
      image_save(img_strokepath,fn_comb(sys.argv[1],"fpath"))


      # todo.

      # 7. generate strokes for borders.

      # see 1 j)

      # 8. push polygons to HPGL

      # todo

      pygame.display.flip()
      time.sleep(10)

if __name__ == "__main__":
   import pygame
   import sys
   import time
   import math
   import random
   main()
