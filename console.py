#!/usr/bin/env python

import sys

def cw(text, curr, max):
   '''console status output function'''
   print "%s [%3i] %i of %i   \r"%(text,100*curr/max,curr,max),

   if curr >= max-1:
      print "\n",

   sys.stdout.flush()
