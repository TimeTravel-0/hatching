#!/usr/bin/env python
#
# this is ugly, experimental, slow, unoptimized code.
# its purpose is to verify my (propably) stupid idea
# of an "image to hatching pen plotter drawing".
#
# for now the script finds edges and fills areas in between
# with colors
# edge detection works as expected, but drawn edges
# (black lines...) are not handled in a special way
# = handled like a normal area/fill = results in double
# lines detected for comic like input drawings
#
# motion vector recovery works ok-ish.
#
# this script now generates lots of data from an image file
# next, yet unimplemented, step is to combine all this data
# and generate polygon lines
#
# another, yet unimplemented, part is to write all the polygons
# out in HPGL form.
#
#
# see main() function for actual high level description of what is going on
#
# we start with a few simple image manipulation functions:
#

import sys
def cw(text, curr, max):
   print "%s [%3i] %i of %i   \r"%(text,100*curr/max,curr,max),

   if curr >= max-1:
      print "\n",

   sys.stdout.flush()

def show_image(display, img, reloc):

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



def load_image(input_file):
   '''loads an image via pygame and returns the image object'''
   print "loading \"%s\""%input_file
   return pygame.image.load(input_file)

def save_image(img, output_file):
   '''saves an image via pygame to a file'''
   print "saving \"%s\""%output_file
   pygame.image.save(img,output_file)

def lcol(a):
   '''limits the range of a value to 0...255 to prevent overflow/out of range errors'''
   if a<0:
      return 0
   if a>255:
      return 255
   return a

def blacknwhite(img_in,limit=32):
   '''converts an image to black and white pixels by threshold'''
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      cw("blacknwhite",y,height)
      for x in range(0,width):
         color_in = img_in.get_at((x,y))

         # slow like hell. generate one blured image and diff them would be better
         #avgb = get_average_brightness(img_in,(x,y),32) # radius 3

         #limit = avgb/2	

         color_out = (255,255,255)
         if color_in[0]+color_in[1]+color_in[2] < limit*3:
            color_out = (0,0,0)

         img_out.set_at((x,y),color_out)
   return img_out

def get_median_color(img_in,pos,radius, mode = "g", borders=4):
   '''returns the median color of a circular area'''
   width = radius*2
   height = radius*2

   colors = []

   for y in range(pos[1]-radius,pos[1]+radius):
      for x in range(pos[0]-radius,pos[0]+radius):
         distance = pow( pow(y-pos[1],2) + pow(x-pos[0],2) , 0.5)
         if distance < radius+0.5: # inside circle
            if x>=0 and y>=0 and x<img_in.get_width() and y<img_in.get_height():
               color = img_in.get_at((x,y))
               
               colors.append(color)

   # sort colors by some means 

   # single color approach

   if mode == "c":

      color_r = [key[0] for key in colors]
      color_g = [key[1] for key in colors]
      color_b = [key[2] for key in colors]

      color_r.sort()
      color_g.sort()
      color_b.sort()

      median_color = color_r[len(color_r)/2], color_g[len(color_g)/2], color_b[len(color_b)/2]

      border_offset = borders

      idx_prev = len(color_r)/2-border_offset
      idx_next = len(color_r)/2+border_offset
      if idx_prev <0:
         idx_prev = 0
      if idx_next > len(color_r)-1:
         idx_next = -1


      prev_color = color_r[idx_prev], color_g[idx_prev], color_b[idx_prev]
      next_color = color_r[idx_next], color_g[idx_next], color_b[idx_next]

      contrast_color = [abs(prev_color[0]-next_color[0]), abs(prev_color[1]-next_color[1]),abs(prev_color[2]-next_color[2]) ]

   # brightness approach

   if mode == "g":
      brightness = []
      for color in colors:
         brightness.append(color[0]+color[1]+color[2])
   
      combined = zip(colors, brightness)
      combined.sort()
      colors_sorted = [item[0] for item in combined]
      median_color = colors_sorted[len(colors_sorted)/2]

   return median_color, contrast_color


def median(img_in, radius, mode, borders):
   '''applies median filter to an image'''
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   img_border = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      cw("median",y,height)

      for x in range(0,width):
         color_out, color_contrast = get_median_color(img_in,(x,y),radius,mode,borders)
         img_out.set_at((x,y),color_out)
         color_contrast = [max(color_contrast)]*3
         img_border.set_at((x,y),color_contrast)
   return img_out, img_border



def get_maximum_brightness(img_in,pos,radius):
   '''returns the average color of a circular area'''
   width = radius*2
   height = radius*2

   brightness_max = 0

   for y in range(pos[1]-radius,pos[1]+radius):
      for x in range(pos[0]-radius,pos[0]+radius):
         distance = pow( pow(y-pos[1],2) + pow(x-pos[0],2) , 0.5)
         if distance < radius+0.5: # inside circle
            if x>=0 and y>=0 and x<img_in.get_width() and y<img_in.get_height():
               color = img_in.get_at((x,y))
               brightness = sum(color[:3])/3
        
               if brightness>brightness_max:
                  brightness_max = brightness
   return brightness_max

def get_average_brightness(img_in,pos,radius):
   '''returns the average color of a circular area'''
   width = radius*2
   height = radius*2

   brightness_divisor = 0
   brightness_sum = 0

   for y in range(pos[1]-radius,pos[1]+radius):
      for x in range(pos[0]-radius,pos[0]+radius):
         distance = pow( pow(y-pos[1],2) + pow(x-pos[0],2) , 0.5)
         if distance < radius: # inside circle
            if x>=0 and y>=0 and x<img_in.get_width() and y<img_in.get_height():
               color = img_in.get_at((x,y))
               brightness = sum(color[:3])/3
        
               brightness_sum+=brightness
               brightness_divisor+=1
   if brightness_divisor>0:
      return brightness_sum / brightness_divisor
   else:
      return 255

def edgedetect(img_in, r=1, offset=(0,0)):
   '''detects edges and marks them'''
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      cw("edge detect",y,height)
      for x in range(0,width):
         color_in = img_in.get_at((x,y))
         brightness_in = sum(color_in[:3])/3
         brightness_avg = get_average_brightness(img_in, (x-offset[0],y-offset[1]), r)
         brightness_difference = abs(brightness_in - brightness_avg)
         if brightness_difference > 255:
            brightness_difference = 255
         color_out = [brightness_difference]*3

         img_out.set_at((x,y),color_out)
   return img_out

def blur(img_in, r=3):
   '''blurs an image with defined averaging radius'''
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      cw("blur",y,height)
      for x in range(0,width):

         brightness_avg = get_average_brightness(img_in, (x,y), r)

         color_avg = [brightness_avg]*3

         color_out = color_avg

         img_out.set_at((x,y),color_out)
   return img_out

def lazyblur(img_in, r=3):
   '''blurs an image with defined averaging radius'''
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())

   # for each direction x/y +/- do running average per r,g,b

   sm = 1-1/float(r)

   # x positive
   img_blur1 = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      cw("lazyblur a",y,height)
      r,g,b = img_in.get_at((0,y))[:3]
      for x in range(0,width):
         r2,g2,b2 = img_in.get_at((x,y))[:3]
         r=float(r*sm)+float(r2*(1-sm))
         g=float(g*sm)+float(g2*(1-sm))
         b=float(b*sm)+float(b2*(1-sm))
         img_blur1.set_at((x,y),(r,g,b))

   # x negative
   img_blur2 = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      cw("lazyblur b",y,height)
      r,g,b = img_in.get_at((width-1,y))[:3]
      for x in list(reversed(range(0,width))):
         r2,g2,b2 = img_in.get_at((x,y))[:3]
         r=float(r*sm)+float(r2*(1-sm))
         g=float(g*sm)+float(g2*(1-sm))
         b=float(b*sm)+float(b2*(1-sm))
         img_blur2.set_at((x,y),(r,g,b))

   # y positive
   img_blur3 = pygame.Surface(img_in.get_size())
   for x in range(0,width):
      cw("lazyblur c",x,width)
      r,g,b = img_in.get_at((x,0))[:3]
      for y in range(0,height):
         r2,g2,b2 = img_in.get_at((x,y))[:3]
         r=float(r*sm)+float(r2*(1-sm))
         g=float(g*sm)+float(g2*(1-sm))
         b=float(b*sm)+float(b2*(1-sm))
         img_blur3.set_at((x,y),(r,g,b))

   # y negative
   img_blur4 = pygame.Surface(img_in.get_size())
   for x in range(0,width):
      cw("lazyblur d",x,width)
      r,g,b = img_in.get_at((x,height-1))[:3]
      for y in list(reversed(range(0,height))):
         r2,g2,b2 = img_in.get_at((x,y))[:3]
         r=float(r*sm)+float(r2*(1-sm))
         g=float(g*sm)+float(g2*(1-sm))
         b=float(b*sm)+float(b2*(1-sm))
         img_blur4.set_at((x,y),(r,g,b))

   img_out = addmul( addmul(img_blur1,img_blur2,0.5,0.5) , addmul(img_blur3,img_blur4,0.5,0.5) , 0.5,0.5)

   return img_out


def blend(img1,img2):
   '''take max val for each pixel from each image'''
   width,height = img1.get_size()
   img_out = pygame.Surface(img1.get_size())
   for y in range(0,height):
      cw("blend",y,height)
      for x in range(0,width):
         color_in1 = img1.get_at((x,y))
         color_in2 = img2.get_at((x,y))

         color_out = [max(color_in1[0],color_in2[0]),max(color_in1[1],color_in2[1]),max(color_in1[2],color_in2[2])]

         img_out.set_at((x,y),color_out)
   return img_out

def addmul(img1,img2,m=1,n=1):
   '''take max val for each pixel from each image'''
   width,height = img1.get_size()
   img_out = pygame.Surface(img1.get_size())
   for y in range(0,height):
      cw("addmul",y,height)
      for x in range(0,width):
         color_in1 = img1.get_at((x,y))
         color_in2 = img2.get_at((x,y))

         color_out = [lcol(color_in1[0]*n+color_in2[0]*m),lcol(color_in1[1]*n+color_in2[1]*m),lcol(color_in1[2]*n+color_in2[2]*m)]

         img_out.set_at((x,y),color_out)
   return img_out



def bolden(img_in, r=3):
   '''draw along maximum brightness with circle radius r'''
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      cw("bolden",y,height)
      for x in range(0,width):
         color_in = img_in.get_at((x,y))
         brightness_in = sum(color_in)/3
         brightness_max = get_maximum_brightness(img_in, (x,y), r)
         color_out = [brightness_max]*3

         img_out.set_at((x,y),color_out)
   return img_out

def count_pixels_with_color(img_in, color):
   '''returns the count of pixels of specified color'''
   count = 0
   width,height = img_in.get_size()
   for y in range(0,height):
      for x in range(0,width):
         color_in = img_in.get_at((x,y))
         if color[:2] == color_in[:2]:
            # found.
            count+=1
   return count


def find_pixel_with_color(img_in, color):
   '''returns the 1st coordinate of a pixel of specified color'''
   width,height = img_in.get_size()
   for y in range(0,height):
      for x in range(0,width):
         color_in = img_in.get_at((x,y))
         if color[:2] == color_in[:2]:
            # found.
            return (x,y)
   return False


def floodfill(img_in,startpos,color):
   '''floodfill from position with color'''
   positions_todo = [] # list of points to draw/check
   positions_todo.append(startpos)

   pixelcounter = 0

   width, height = img_in.get_size()

   startcolor = img_in.get_at(startpos)
   while len(positions_todo)>0:

      # get point from list:
      pos=positions_todo.pop()
      img_in.set_at(pos, color)
      pixelcounter+=1
      # offsets to try
      offsets = [[1,0],[0,1],[-1,0],[0,-1]]
      for offset in offsets:
         trypos = (pos[0]+offset[0],pos[1]+offset[1])
         #print trypos
         if trypos[0]>=0 and trypos[1]>=0 and trypos[0]<width and trypos[1]<height:
            if img_in.get_at(trypos) == startcolor: # color at offset is same as on start
               positions_todo.append(trypos)

   return pixelcounter

def id_to_color(id):
   return (id%254+1,(id/254)%255,(id/254/255)%255)

def color_to_id(color):
   return color[0]-1 + color[1]*255 + color[2]*255*255


def mask(img_in, color_mask):
   width,height = img_in.get_size()
   img_out = pygame.Surface(img_in.get_size())
   for y in range(0,height):
      cw("mask",y,height)
      for x in range(0,width):
         color_in = img_in.get_at((x,y))
         if color_in[:2] == color_mask[:2]: # color of img is same as color specified, copy!
            color_out = (255,255,255)
         else:
            color_out = (0,0,0)
         img_out.set_at((x,y), color_out)
   return img_out

def get_avg_color(img_in, mask):
   width,height = img_in.get_size()
   color_avg_sum = [0,0,0]
   color_avg_cnt = 0
   for y in range(0,height):
      for x in range(0,width):
         if max(mask.get_at((x,y))[:2]) > 128:
            # mask slected
            color_in = img_in.get_at((x,y))
            color_avg_sum[0]+=color_in[0]
            color_avg_sum[1]+=color_in[1]
            color_avg_sum[2]+=color_in[2]
            color_avg_cnt+=1
   if color_avg_cnt == 0:
      return [0,0,0]
   return [color_avg_sum[0]/color_avg_cnt, color_avg_sum[1]/color_avg_cnt, color_avg_sum[2]/color_avg_cnt]




def gen_single_color(size, color):
   img_out = pygame.Surface(size)
   img_out.fill(color)
   return img_out

def multiply(img_in1, img_in2):
   width,height = img_in1.get_size()
   img_out = pygame.Surface(img_in1.get_size())
   for y in range(0,height):
      cw("multiply",y,height)
      for x in range(0,width):
         color_in1 = img_in1.get_at((x,y))
         color_in2 = img_in2.get_at((x,y))
         color_out = [ color_in1[0] * color_in2[0] / 255 , color_in1[1] * color_in2[1] / 255 , color_in1[2] * color_in2[2] / 255 ] 
         img_out.set_at((x,y), color_out)
   return img_out



def motionprobe(img_in,mask,pos,radius,angle,shift):
   '''probes a motion vector for an specific point/radius'''

   offsetx,offsety = int(math.cos(angle*2*math.pi/360)*shift), int(math.sin(angle*2*math.pi/360)*shift)

   correlation_sum = 0
   correlation_count = 0

   for y in range(pos[1]-radius,pos[1]+radius):
      for x in range(pos[0]-radius,pos[0]+radius):
         distance = pow( pow(y-pos[1],2) + pow(x-pos[0],2) , 0.5)
         if distance < radius: # inside circle
            if x>=0 and y>=0 and x<img_in.get_width() and y<img_in.get_height():
               if sum(mask.get_at((x,y))[:3]) > 128:
                  # in mask
                  x2,y2 = x+offsetx, y+offsety
                  if x2>=0 and y2>=0 and x2<img_in.get_width() and y2<img_in.get_height():
                     color = img_in.get_at((x,y))
                     color2 = img_in.get_at((x2,y2))
                     # the correlation itself (difference between the two picture segments) lower is better
                     correlation = abs(color[0]-color2[0]) + abs(color[1]-color2[1]) + abs(color[2]-color2[2])

                     correlation_sum+=correlation
                     correlation_count+=1

   if correlation_count == 0:
      return -1

   return correlation_sum/correlation_count

def motionfind(img_in,mask,pos,radius):


   cor_list = []

   min_cor = -1
   min_ang = 0
   min_ofs = 0

   for shift in range(2,radius,radius/3): # shift 2 to 20 in 2 steps
      startang = int(random.random()*360)
      for angle in range(0+startang,360+startang,10): # 10 degree steps to probe, start with random one
         cor = motionprobe(img_in,mask,pos,radius,angle,shift)
         print "probing shift %i  angle %i correlation %i position %s  \r"%(shift,angle,cor,str(pos)),

         if cor != -1:
            cor_list.append(cor)
            if cor < min_cor or min_cor == -1:
               min_cor = cor
               min_ang = angle
               min_ofs = shift

   print "\n",
   #print min_ang, min_ofs
   return min_ang%360, min_ofs, min_cor, (max(cor_list)-min(cor_list))

def motionsfind(img_in, mask, radius):
   '''finds points with distance "radius" within the mask and gets motion vectors for each'''

   # point must be in mask and "radius" away from other points
   found_points = []

   mask_clone = pygame.Surface(mask.get_size())
   mask_clone.blit(mask,(0,0))



   while True:
      position = find_pixel_with_color(mask_clone,(255,255,255))
      if not position:
         break
      ang,ofs,cor,corvar = motionfind(img_in, mask, position, radius)
      found_points.append([position,ang,ofs,cor,corvar])
      #print position, ang, ofs
      pygame.draw.circle(mask_clone, (0,0,0), position, radius, 0)

      #
  
   return found_points

def main():
   if len(sys.argv)==2: # 1 parameters

      pygame.init()


      # the idea is as follows:
      # 1. find/mark edges, because edges mark areas

      input_file = sys.argv[1]
      img_in = load_image(input_file)
      insize = img_in.get_size()

      maxdsize = [1024,600]

      dsize = [insize[0]*4,insize[1]*4]
      inratio = float(insize[1])/float(insize[0])
      if dsize[0]>maxdsize[0]:
         dsize[0]=maxdsize[0]
         dsize[1]=int(dsize[0]*inratio)
      if dsize[1]>maxdsize[1]:
         dsize[1]=maxdsize[1]
         dsize[0]=int(dsize[1]/inratio)
 
      
      display = pygame.display.set_mode(dsize)


      show_image(display, img_in, False)

      #img_blurx = lazyblur(img_in,3)
      #show_image(display,img_blurx, True)
      #time.sleep(5)


      # a) first we run an median filter to get rid of noise but keep edges
      # as the median filter already gets a list of all pixels around the analyzed coordinate
      # it got an additional part to calculate the contrast.
      img_in, img_border = median(img_in,3,"c",3)
      show_image(display, img_in, True)
      show_image(display, img_border, True)

      save_image(img_border,"bordem-"+sys.argv[1])



      # b) edge detection in x direction
      #img_edge1 = edgedetect(img_in,1,(1,0))
      #show_image(display, img_edge1, True)

      # c) edge detection in y direction
      #img_edge2 = edgedetect(img_in,1,(0,1))
      #show_image(display, img_edge2, False)

      # d) blend x and y edge detection images
      #img_blend = blend(img_edge1, img_edge2)
      #show_image(display, img_blend, False)

      #save_image(img_blend,"border-"+sys.argv[1])

      img_blend = img_border 

      # e) create blured image (average of local area)
      img_blur = img_blend
      for i in range(0,3):
         img_blur = lazyblur(img_blur, 3)
         show_image(display, img_blur, False)

      # f) unblured - blured edge image = better image for threshold usage (adapts to local variations)
      img_blurdif = addmul(img_blend, img_blur, -1)
      show_image(display, img_blurdif, True)

      # g) bolden edges
      img_bold = bolden(img_blurdif,1)
      show_image(display, img_bold, True)

      # h) convert to black and white via limit
      img_bnw = blacknwhite(img_bold,12)  
      show_image(display, img_bnw, True)

      # i) isles smaller than limit get eliminated
      while True:
         position = find_pixel_with_color(img_bnw,(255,255,255))
         if not position:
            break
         pixelcount = floodfill(img_bnw, position, (128,128,128))
         if pixelcount < 100:
            print "isle at %s, %i pixels below limit"%(str(position), pixelcount)
            floodfill(img_bnw, position, (0,0,0)) # eliminate it

      img_bnw = blacknwhite(img_bnw,4)
      

      # 2. for the room between edges: flood fill until no space left

      facecount = 0

      while True:
         position = find_pixel_with_color(img_bnw,(0,0,0))
         if not position:
            break
         #print position
         pixelcount = floodfill(img_bnw, position, id_to_color(facecount))
         if pixelcount < 25:
            print "isle at %s, %i pixels below limit"%(str(position), pixelcount)
            floodfill(img_bnw, position, (255,255,255))
         else:
            facecount+=1
         show_image(display, img_bnw, False)

      print "filled %i faces"%facecount


      # 3. with each flood fill a seperate area/mask is defined
      masks = []
      masks_drawtmp = pygame.Surface(img_bnw.get_size())
      for i in range(0,facecount):
         masks.append(bolden( mask(img_bnw,id_to_color(i)) ,2))
         masks_drawtmp = blend(masks_drawtmp, masks[i])
         show_image(display, masks_drawtmp, False)


      # 4. get average brightness from this area

      masked_originals = []
      masked_originals_drawtmp = pygame.Surface(img_bnw.get_size())

      avgcolors = []
 
      for i in range(0,facecount):
         avgcolor = get_avg_color(img_in, masks[i])
         avgcolors.append(avgcolor)
         print avgcolor
         masked_originals.append(   multiply(  gen_single_color(img_bnw.get_size(),avgcolor), masks[i])     )
         #masked_originals.append(multiply(masks[i],img_in))
         masked_originals_drawtmp = blend(masked_originals_drawtmp, masked_originals[i])

         show_image(display, masked_originals_drawtmp, False)

      save_image(masked_originals_drawtmp,"tmp-"+sys.argv[1])


      # 5. motion vector find
      motionvector_drawtmp = pygame.Surface(img_bnw.get_size())


      for i in range(0,facecount):
         print "motion vector face %i"%i
         motionvectors = motionsfind(img_in, bolden(masks[i],5),10) # 10px radius




         cormax = 0
         corvar_max = 0
         for vector in motionvectors:
            pos,ang,ofs,cor,corvar = vector

            # correlation: smaller = smaller difference in picture comparison 0 = identical, which is good
            # corvar: correlation variance, bigger =  better because we dont just probe signle colored surface...
            #
            
            # correlation needs normalisation
            if cormax<cor:
               cormax=cor

            if corvar_max<corvar:
               corvar_max=corvar

         for vector in motionvectors:
            pos,ang,ofs,cor,corvar = vector

            # brightness of contrast image correlates to "roughness" at this location
            #roughness = float(255-max(img_blur.get_at(pos)[:2]))/255

            rel_cor = float(cor)/float(cormax)
            rel_corvar = float(corvar)/float(corvar_max)

            ofs=ofs*(1-rel_cor)*5 * rel_corvar


            if ofs>0:
               endpos = math.cos(ang*2*math.pi/360)*ofs+pos[0],math.sin(ang*2*math.pi/360)*ofs+pos[1]
               pygame.draw.line(motionvector_drawtmp, avgcolors[i], pos, endpos, 1)

         show_image(display, motionvector_drawtmp, True)
      save_image(motionvector_drawtmp,"vector-"+sys.argv[1])
     


      # 6. generate strokes/hatching for each area. it is not necessary to know the area outline as polygon, just check the individual pixels

      # todo.

      # 7. generate strokes for borders.

      # todo.

      # 8. push polygons to HPGL

      # todo

      pygame.display.flip()
      time.sleep(10)

if __name__ == "__main__":
   import pygame
   import sys
   import time
   import math
   import random
   main()
