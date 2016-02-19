#!/usr/bin/env python

import pygame


def fn_comb(filename_in,addition):
   '''inserts addition right before the suffix'''
   filename_split = filename_in.split(".")
   new_filename=".".join(filename_split[:-1]) +"-"+addition +"." + filename_split[-1]
   return new_filename

def load_image(input_file):
   '''loads an image via pygame and returns the image object'''
   print "loading \"%s\""%input_file # should use cw command
   return pygame.image.load(input_file)

def save_image(img, output_file):
   '''saves an image via pygame to a file'''
   print "saving \"%s\""%output_file # should use cw command
   pygame.image.save(img,output_file)

# rename...   
def gen_single_color(size, color):
   '''generates image with single color'''
   img_out = pygame.Surface(size)
   img_out.fill(color)
   return img_out
   


if __name__ == "__main__": # test!
    
    print "testing fn_comb"
    a = fn_comb("../foo/bar/xd.jpg","wasd123")
    b = "../foo/bar/xd-wasd123.jpg"
    if a != b:
       print "Error: %s %s"%(a,b)
    print "ok."

    print "testing gen_single_color, save_image and load_image"
    a = gen_single_color((320,240),(255,0,255))
    save_image(a, "/tmp/hatching_test.jpg")
    b = load_image("/tmp/hatching_test.jpg")
    print "ok."
    
    
