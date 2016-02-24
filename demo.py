#!/usr/bin/env python

import sys

from lib_console import *
from lib_imagefile import *
from lib_colors import *
from lib_image_filters import *
from lib_paths import *
from lib_motionvectors import *
from lib_hpgl import *





def main(input_file,mode=""):
   '''main routine'''

   pygame.init()
      

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













