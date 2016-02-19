#!/usr/bin/env python


def hpgl_cmd(c,point=[]):
   '''create an command from txt and point'''
   if isinstance(point,list):
      npoint = [str(x) for x in point]
      return [c+",".join(npoint)+";"]
   else:
      return [c+str(point)+";"]

def hpgl_frompaths(paths):
   '''takes an array of  paths and creates HPGL code from it. coordinates are used 1:1'''
   commandlist = []


   #commandlist.append(hpgl_cmd("PU"))
   for path in paths:
      pen_down = False
      for point in path:
         if not pen_down:
            # go to position
            commandlist+=hpgl_cmd("PU",point)
            pen_down = True
         # and then pen down
         commandlist+=hpgl_cmd("PD",point)
         
        

   return commandlist


def hpgl_tofile(commandlist, fn):
   f = file(fn,"w")
   for line in commandlist:
      f.write(line+"\n")
   f.close()
   return


def hpgl_bestpen(width, color):
   '''finds the best fitting pen from the pen specification file and returns its values'''
   width, color, id = 0,0, 0
   return width, color, id

def hpgl_usepen(width, color):
   '''select best fitting pen to specified value'''
   id = 1 # always 1 for now.
   return hpgl_cmd("SP",id)

if __name__ == "__main__": # test
   print "testing"

   paths = [[10,20],[30,45],[50,55],[77,32]],[[73,34],[120,47],[170,30],[234,65]],[[140,110],[170,120],[220,94],[230,63]],[[137,108],[120,80],[70,70],[40,90]],[[100,50],[150,60],[200,70],[150,80]]

   c = hpgl_usepen(1,(255,255,0))
   c+= hpgl_frompaths(paths)

   hpgl_tofile(c,"foobar.hpgl")


   print "NOT IMPLEMENTED"
