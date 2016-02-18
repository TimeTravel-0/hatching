#!/usr/bin/env python


def fn_comb(filename_in,addition):
   '''inserts addition right before the suffix'''
   filename_split = filename_in.split(".")
   new_filename=".".join(filename_split[:-1]) +"-"+addition +"." + filename_split[-1]
   return new_filename

def load_image(input_file):
   '''loads an image via pygame and returns the image object'''
   print "loading \"%s\""%input_file
   return pygame.image.load(input_file)

def save_image(img, output_file):
   '''saves an image via pygame to a file'''
   print "saving \"%s\""%output_file
   pygame.image.save(img,output_file)
