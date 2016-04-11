#!/usr/bin/env python

import sys

from lib_console import *
from lib_imagefile import *
from lib_colors import *
from lib_image_filters import *
from lib_paths import *
from lib_motionvectors import *
from lib_hpgl import *


def blurmedian(input_file):
    
     

   img_in = image_load(input_file)

   img_in_grid  =image_filter_zoomgrid(img_in,10,1)
   img_in_gridn =image_filter_zoomgrid(img_in,10,0)
   image_save(img_in_grid,fn_comb(input_file,"in-grid"))
   image_save(img_in_gridn,fn_comb(input_file,"in-gridn"))


   display = image_gui((1000,1000))
   image_show(display,image_filter_zoomgrid(img_in))

   img_blur = blur(img_in,3)
   img_blur_grid  =image_filter_zoomgrid(img_blur,10,1)
   img_blur_gridn =image_filter_zoomgrid(img_blur,10,0)

   image_save(img_blur_grid,fn_comb(input_file,"blur-grid"))
   image_save(img_blur_gridn,fn_comb(input_file,"blur-gridn"))



   image_show(display,img_blur_grid)
 
   img_median, img_border = median(img_in,3,"c",3)
   img_median_grid = image_filter_zoomgrid(img_median,10,1)
   img_median_gridn = image_filter_zoomgrid(img_median,10,0)
   img_border_grid = image_filter_zoomgrid(img_border,10,1)
   img_border_gridn = image_filter_zoomgrid(img_border,10,0)

   image_save(img_median_grid,fn_comb(input_file,"median-grid"))
   image_save(img_median_gridn,fn_comb(input_file,"median-gridn"))
   image_save(img_border_grid,fn_comb(input_file,"border-grid"))
   image_save(img_border_gridn,fn_comb(input_file,"border-gridn"))



   image_show(display,img_median_grid)
   image_show(display,img_border_grid)



def edgewalker(input_file):
   img_in = image_load(input_file)
    
   display = image_gui((img_in.get_width()*2,img_in.get_height()*1),False)
   
   img_in = blacknwhite(img_in,12) 
    
   img_median, img_border = median(img_in,3,"c",3)
    
   paths = edgewalk_visualize(img_border,display,3)
   
   
   c1 = hpgl_usepen(1,(255,255,0))
   c1+=hpgl_frompaths(paths)
   hpgl_tofile(c1,"b1.hpgl")
   
   paths2 = pathcombiner(paths)

   c2 = hpgl_usepen(1,(255,255,0))
   c2+=hpgl_frompaths(paths)
   hpgl_tofile(c2,"b2.hpgl")
      
   paths3 = optimizepaths(paths2)

   c3 = hpgl_usepen(1,(255,255,0))
   c3+=hpgl_frompaths(paths)
   hpgl_tofile(c3,"b3.hpgl")     
   
def facewalker(input_file):
   img_in = image_load(input_file)
    
   display = image_gui((img_in.get_width()*2,img_in.get_height()*1),False)
   
   img_in = blacknwhite(img_in,12) 
    
   #img_median, img_border = median(img_in,3,"c",3)
   img_median=img_in
   paths = edgewalk_visualize(img_median,display,3)
   
   c1 = hpgl_usepen(1,(255,255,0))
   c1+=hpgl_frompaths(paths)
   hpgl_tofile(c1,"a1.hpgl")
   
   paths2 = pathcombiner(paths)

   c2 = hpgl_usepen(1,(255,255,0))
   c2+=hpgl_frompaths(paths)
   hpgl_tofile(c2,"a2.hpgl")
      
   paths3 = optimizepaths(paths2)

   c3 = hpgl_usepen(1,(255,255,0))
   c3+=hpgl_frompaths(paths)
   hpgl_tofile(c3,"a3.hpgl")   
   

def scribbler(input_file):
   img_in = image_load(input_file)
    
   display = image_gui((img_in.get_width()*2,img_in.get_height()*1),False)
   
   #img_in = blacknwhite(img_in,12) 
    
   #img_median, img_border = median(img_in,3,"c",3)
   img_median=addmul(image_create(img_in.get_size(),(255,255,255)),img_in,-1,1)
   paths = scribble_visualize(img_median,display,3)
   
   return
   
   c1 = hpgl_usepen(1,(255,255,0))
   c1+=hpgl_frompaths(paths)
   hpgl_tofile(c1,"a1.hpgl")
   
   paths2 = pathcombiner(paths)

   c2 = hpgl_usepen(1,(255,255,0))
   c2+=hpgl_frompaths(paths)
   hpgl_tofile(c2,"a2.hpgl")
      
   paths3 = optimizepaths(paths2)

   c3 = hpgl_usepen(1,(255,255,0))
   c3+=hpgl_frompaths(paths)
   hpgl_tofile(c3,"a3.hpgl")      
   
def arrowdraw(input_file):
   img_in = image_load(input_file)
    
   display = image_gui((img_in.get_width()*3,img_in.get_height()*3))
   
   for angle in range(-360*4,360*4):
       rotimg=render_vector(img_in, (img_in.get_width()/2,img_in.get_height()/2), angle, 20)
       image_show(display,rotimg,False,(1,1))
    

def main(input_file,mode=""):
   '''main routine'''

   pygame.init()
   
   if mode == "blurmedian" or mode =="":
       blurmedian(input_file)
 
   if mode == "edgewalker" or mode =="":
       edgewalker(input_file)

   if mode == "facewalker" or mode =="":
       facewalker(input_file)   
       
   if mode == "scribbler" or mode =="":
       scribbler(input_file)         
       
   if mode == "arrow":
       arrowdraw(input_file)
   
  

   pygame.display.flip()
   time.sleep(10)

  


if __name__ == "__main__":
   import pygame
   import sys
   import time
   import math
   import random
   if len(sys.argv) == 2:
       main(sys.argv[1])
   if len(sys.argv) == 3:
       main(sys.argv[1],sys.argv[2])













