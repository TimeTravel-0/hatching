#!/usr/bin/env python

import sys

def cw(text, curr, max):
   '''console status output function'''
   print "%s [%3i] %i of %i   \r"%(text,100*curr/max,curr,max),

   if curr >= max-1:
      print "\n",

   sys.stdout.flush()


if __name__ == "__main__": # test
   print "testing cw"

   for i in range(0,123):
      cw("testing cw",i,123)
   print "ok."
