#!/usr/bin/env python


def lcol(a):
   '''limits the range of a value to 0...255 to prevent overflow/out of range errors'''
   if a<0:
      return 0
   if a>255:
      return 255
   return a


def id_to_color(id):
   '''calculated unique color from id'''
   return (id%254+1,(id/254)%255,(id/254/255)%255)

def color_to_id(color):
   '''calculated unique id from color'''
   return color[0]-1 + color[1]*255 + color[2]*255*255
