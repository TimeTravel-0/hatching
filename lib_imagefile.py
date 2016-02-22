#!/usr/bin/env python

import pygame


def fn_comb(filename_in,addition,newsuffix=""):
   '''inserts addition right before the suffix'''
   filename_split = filename_in.split(".")
   if newsuffix == "":
      newsuffix = filename_split[-1]
   new_filename=".".join(filename_split[:-1]) +"-"+addition +"." + newsuffix
   return new_filename

def image_load(input_file):
   '''loads an image via pygame and returns the image object'''
   print "loading \"%s\""%input_file # should use cw command
   return pygame.image.load(input_file)

def image_save(img, output_file):
   '''saves an image via pygame to a file'''
   print "saving \"%s\""%output_file # should use cw command
   pygame.image.save(img,output_file)

.   
def image_show(size, color=(0,0,0)):
   '''generates image with single color'''
   img_out = pygame.Surface(size)
   img_out.fill(color)
   return img_out
   
def image_show(display, img, reloc=True, dims=(3,3)):
   '''shifts images in display and adds the new one ; fifo-like'''
   w,h = dims

   d = display.get_size()

   # scale img to display/3th
   newsize = [d[0]/w,d[1]/h]
   resimg = pygame.transform.scale(img,newsize)
   s = resimg.get_size()

   if reloc:
      storepic = image_show((newsize[0],d[1]))# store right row
      storepic.blit(display,(-(d[0]-newsize[0]),0))
      display.blit(display,(s[0],0)) # move display one line to the right
      display.blit(storepic,(0,newsize[1]))

   display.blit(resimg,(0,0))
   pygame.display.flip()



if __name__ == "__main__": # test!
    
   print "testing fn_comb"
   a = fn_comb("../foo/bar/xd.jpg","wasd123")
   b = "../foo/bar/xd-wasd123.jpg"
   if a != b:
      print "Error: %s %s"%(a,b)
   print "ok."

   print "testing image_show, image_save and image_load"
   a = image_show((320,240),(255,0,255))
   image_save(a, "/tmp/hatching_test.jpg")
   b = image_load("/tmp/hatching_test.jpg")
   print "ok."
    
   from lib_colors import *
   from time import sleep
   print "testing image_show"    
   # prepare
   pygame.init()
 
   dsize=(640,460)
   display = pygame.display.set_mode(dsize)


   for keepflop in range(0,3):
      for j in range(1,5,1):
         d=2**j
         keep = True

         # clear screen
         image_show(display,image_show((1,1)),True,(1,1))
         for i in range(0,d*d):

            if keepflop == 1 or (keepflop == 2 and keep):
               img = image_show((640,480),angle_to_color(360*i/(d*d)+180))
               image_show(display, img, keepflop != 1,(d,d))
               sleep(2.0/(d*d))



            img = image_show((640,480),angle_to_color(360*i/(d*d)))
            image_show(display, img, True,(d,d))
            sleep(2.0/(d*d))


    
