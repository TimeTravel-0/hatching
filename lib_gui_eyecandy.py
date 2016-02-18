#!/usr/bin/env python

import pygame

def show_image(display, img, reloc):
      '''shifts images in display and adds the new one ; fifo-like'''
      w,h = 3,3

      d = display.get_size()

      # scale img to display/3th
      newsize = [d[0]/w,d[1]/h]
      resimg = pygame.transform.scale(img,newsize)
      s = resimg.get_size()

      if reloc:
         display.blit(display,(-s[0]*(w-1),s[1]))
         display.blit(display,(s[0],0))

      display.blit(resimg,(0,0))
      pygame.display.flip()
