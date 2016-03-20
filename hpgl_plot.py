#!/usr/bin/env python
import pygame
import math

class virtualpen:
    def __init__(self,definition_file,number,surface,pxpermm):
        self.pxpermm = pxpermm
        self.load(definition_file,number)
        self.position=[0,0]
        self.surface=surface
        self.zpos=1
        self.ztarget=1
        self.zacc=0
        return

    def gen_sprite(self):
        self.sprite = pygame.Surface(size)

    def load(self,definition_file,number):
        f = file(definition_file)
        lines = f.readlines()
        f.close()
    
        others_follow = False    
        for line in lines:
            ls=line.split()
            if len(ls)>1:
                if str(number) == ls[0]:
                    #print ls
                    self.number = int(ls[0])
                    self.thickness = float(ls[1]) * self.pxpermm
                    self.rel_r = float(ls[2])
                    self.rel_g = float(ls[3])
                    self.rel_b = float(ls[4])
                    self.color = [255*self.rel_r,255*self.rel_g,255*self.rel_b]
                    others_follow = False
                    print "pen %i is %i px wide and of color (%03i %03i %03i)"%(self.number,self.thickness,self.color[0],self.color[1],self.color[2])
                else:
                    if len(ls) == 5:
                        others_follow = True
        return others_follow
        
    def ztick(self):
    
    
        if self.zpos<self.ztarget:
            self.zacc+=0.1
            #self.zacc+=0.001            
        if self.zpos>self.ztarget:
            self.zacc-=0.05
            #self.zacc-=0.005
            
        self.zpos+=self.zacc
        
        if self.zpos<-0.5:
            self.zpos=0.5
            self.zacc=math.fabs(self.zacc)*0.3
            
        if self.zpos<0.0:
            self.zpos*=0.5
            self.zacc*=0.5
        #    self.zpos-=0.05

        if self.zpos>1:
            self.zpos=1.0
            self.zacc=-math.fabs(self.zacc)*0.5
            
        self.zacc*=0.95
        
        
        
    def up(self):
        self.ztarget=1.0
        return
        
    def down(self):
        self.ztarget=-0.5
        return
    
    def goto(self,pos):
        self.draw_line(pos)
        
        #pygame.draw.circle(self.surface, (128,0,0), (int(pos[0]),int(pos[1])), 50)

        return
        
    def move_towards(self,pos):
        #print pos
        stepsize=self.thickness*0.25
        dx = (pos[0] - self.position[0])
        dy = (pos[1] - self.position[1])
        
        reached = dx*dx+dy*dy < stepsize*stepsize 
        
        ang = math.atan2(dx,dy)
        
        
        dx = math.sin(ang)*stepsize
        dy = math.cos(ang)*stepsize
        
        
        self.position[0]+=dx
        self.position[1]+=dy
        return reached
        
    def draw_line(self,pos):
    
        #pygame.draw.line(self.surface, (128,128,255), (int(self.position[0]),int(self.position[1])), (int(pos[0]),int(pos[1])), 3)
    
        reached = False
        i=0
        while reached == False:
            i+=1
        #for i in range(0,10):
            self.ztick()
            reached = self.move_towards(pos)
            #print i,r
            self.draw(self.position,i+1)
        #self.position=pos
        return
        
    def draw(self,pos,w=10):
        x,y = int(pos[0]),int(pos[1])
        dmax= int((self.thickness/2)*(1-self.zpos))+2 #5
        if self.zpos<0.5:
            #pygame.draw.circle(self.surface, (255-(255/float(w)),0,0), (x,y), int(self.zpos*10+2))
            
            for xx in range(x-dmax,x+dmax):
                for yy in range(y-dmax,y+dmax):
                    self.draw_pixel((x,y),(xx,yy),dmax)
        #print x,y        
        return
        
    def draw_pixel(self,cpos,pos,dmax):
        fadeout_pixel = 3
        x,y = pos
        if x<0 or y<0 or x>self.surface.get_width()-1 or y>self.surface.get_height()-1:
            return
            
        dist_abs = math.pow( math.pow(cpos[0]-pos[0],2) + math.pow(cpos[1]-pos[1],2) ,0.5)
        
        dist_rel = dist_abs/float(dmax)
    
        c = self.surface.get_at(pos)
        
        mix = (1.0/float(fadeout_pixel))*(float(dmax)-dist_abs) #+ (1-dist*dist)
        if mix>1:
            mix=1
        if mix<0:
            mix=0
        
        col = self.color
        
        c= (col[0]*mix + c[0]*(1-mix),col[1]*mix + c[1]*(1-mix),col[2]*mix + c[2]*(1-mix)) 
        
        
        
        self.surface.set_at(pos,c)

class virtualplotter:
    def __init__(self,pen_file,scale=2.0):
        self.surface=False
        self.pens = []
        self.scale=scale
        self.dpi=1016.0
        self.size_mm =[416,276]
        self.size_inch=[self.size_mm[0]/25.4,self.size_mm[1]/25.4]
        self.size_px=[int(self.size_inch[0]*self.dpi/self.scale),int(self.size_inch[1]*self.dpi/self.scale)]
        
        self.surface = pygame.Surface(self.size_px)
        self.surface.fill((255,255,255))
        
        self.pxpermm = 1/((25.4/self.dpi)*self.scale)
        
        print "output dimensions are %i x %i px"%(self.size_px[0],self.size_px[1])
        
        
        for i in range(0,8):
            self.pens.append(virtualpen(pen_file,i,self.surface,self.pxpermm))
        return
        
        
    def h2x(self,hpgl_number):
        return (hpgl_number  / self.scale) # *self.dpi
        
    def h22x(self,p):
        return [self.h2x(float(p[0])),self.size_px[1]-self.h2x(float(p[1]))]
        
    def PU(self,pos):
        self.pen.up()
        self.pen.goto(self.h22x(pos))
        return
        
    def PD(self,pos):
        self.pen.down()
        self.pen.goto(self.h22x(pos))
        return
        
    def SP(self,no):
        self.pen = self.pens[no]
        return
        
    def cmd(self,c):
        if len(c)==0:
            return
        #print c
        cmdname = c[:2]
        args = c[2:]
        if "," in args: # got args comma seperated
            args = args.split(",")
        else:
            args = [args]
            
            
        if cmdname=="PU":
            self.PU(args)
        if cmdname=="PD":
            self.PD(args)
        if cmdname=="SP":
            self.SP(int(args[0]))
        
        
        
    def cmds(self,cd):
        cd=cd.replace("\r","\n").replace("\n",";").split(";")
        
        for i in range(0,len(cd)):
            c=cd[i]
            print "\rplotting... %3.2f %% (line %i of %i): %s"%(100.0*(float(i)/len(cd)),i,len(cd),c),
            self.cmd(c)
        
    def save(self,filename):
        if self.surface:
            pygame.image.save(self.surface,filename)
        

        
        
def main(hpgl_file,pen_file,image_file,size):
    plotter = virtualplotter(pen_file,size)
    
    f = file(hpgl_file)
    hpgl_code = f.read()
    f.close()
    
    plotter.cmds(hpgl_code)
    
    plotter.save(image_file)
    
    


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 5:
        main(sys.argv[1],sys.argv[2],sys.argv[3],float(sys.argv[4]))
    else:
        print "this.py input.hpgl HPGLPENS.PS output.png 2(size reduction)"
