#!/usr/bin/env python

import pygame

def show_image(display, img, reloc=True, dims=(3,3)):
      '''shifts images in display and adds the new one ; fifo-like'''
      w,h = dims

      d = display.get_size()

      # scale img to display/3th
      newsize = [d[0]/w,d[1]/h]
      resimg = pygame.transform.scale(img,newsize)
      s = resimg.get_size()

      if reloc:
         storepic = gen_single_color((newsize[0],d[1]))# store right row
         storepic.blit(display,(-(d[0]-newsize[0]),0))


        # display.blit(display,(-s[0]*(w-1),s[1])) # move lower line one lower
         display.blit(display,(s[0],0)) # move display one line to the right
         display.blit(storepic,(0,newsize[1]))

      display.blit(resimg,(0,0))
      pygame.display.flip()


if __name__ == "__main__": # test

   from lib_imagefile import *
   from lib_colors import *
   from time import sleep
   print "testing show_image"


   # prepare
   pygame.init()
 
   dsize=(640,460)
   display = pygame.display.set_mode(dsize)


   for keepflop in range(0,3):
      for j in range(1,5,1):
         d=2**j
         keep = True

         # clear screen
         show_image(display,gen_single_color((1,1)),True,(1,1))
         for i in range(0,d*d):

            if keepflop == 1 or (keepflop == 2 and keep):
               img = gen_single_color((640,480),angle_to_color(360*i/(d*d)+180))
               show_image(display, img, keepflop != 1,(d,d))
               sleep(2.0/(d*d))



            img = gen_single_color((640,480),angle_to_color(360*i/(d*d)))
            show_image(display, img, True,(d,d))
            sleep(2.0/(d*d))

