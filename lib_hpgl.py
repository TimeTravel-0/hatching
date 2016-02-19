#!/usr/bin/env python

def hpgl_frompaths(paths):
   '''takes an array of  paths and creates HPGL code from it. coordinates are used 1:1'''
   commandlist = ["PU"]
   return commandlist


def hpgl_bestpen(width, color):
   '''finds the best fitting pen from the pen specification file and returns its values'''
   width, color = 0,0
   return width, color

def hpgl_usepen(width, color):
   '''select best fitting pen to specified value'''
   commandlist = ["PU"]
   return commandlist

if __name__ == "__main__": # test
   print "testing"
   print "NOT IMPLEMENTED"
