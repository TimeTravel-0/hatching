#!/usr/bin/env python

#import colorsys
import math

# test present
def lcol(a):
   '''limits the range of a value to 0...255 to prevent overflow/out of range errors'''
   if a<0:
      return 0
   if a>255:
      return 255
   return a


# test present
def id_to_color(id):
   '''calculated unique color from id'''
   return (id%254+1,(id/254)%255,(id/254/255)%255)

# test present
def color_to_id(color):
   '''calculated unique id from color'''
   return color[0]-1 + color[1]*254 + color[2]*254*255
   
# test NOT present
def angle_to_color(angle,length=1):
   '''calculates color based on anlge'''

   #r,g,b = colorsys.hsv_to_rgb(angle/360.0 , length, length)

   r = int(lcol( (math.sin(angle*2*math.pi/360.0)+1)*0.5*255*length ))
   g = int(lcol( (math.sin((angle+120)*2*math.pi/360.0)+1)*0.5*255*length ))
   b = int(lcol( (math.sin((angle+240)*2*math.pi/360.0)+1)*0.5*255*length ))
   return [r,g,b]

   return [lcol(r*255),lcol(g*255),lcol(b*255)]




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


   print "testing angle_to_color"
   for i in range(0,360):
      a = angle_to_color(i)
      b = angle_to_color(i-360)
      c = angle_to_color(i+360)

      if a != b:
         print "Error."
         break
      if b != c:
         print "Error."
         break
   print "ok."
