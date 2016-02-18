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
   return color[0]-1 + color[1]*254 + color[2]*254*255


if __name__ == "__main__": # test!

   print "testing id_to_color and color_to_id"
   for id in range(0,254*255*255):
      color = id_to_color(id)
      id_re = color_to_id(color)
      if id != id_re:
         print "Error: id=%i, color=%s, id=%i"%(id, color, id_re)
         break
   print "ok."


   print "testing lcol"
   for z in range(-255,255+255):
      y = lcol(z)
      if y<0 or y>255:
         print "Error: %z %i"%(z,y) 
         break
   print "ok."
