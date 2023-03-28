import pygame
import numpy as np
import random as rnd
import time
import mapdisplay as display
import rivers  as rivers
import csv

# dimensions of map in tiles
#NTILES   = (30, 20)
#TDIM      = (10, 10)
#MARGIN  = 2
# display for executable test?
#DISPLAY = True
#DISPTIME = 100
# type of map: 'continent' or "med"

food={"plains":1000,"desert":50,"mountain":100,"alpine":0,"sea":0,"none":0,"forest":200}
move={"plains":2,"desert":2,"mountain":3,"sea":4,"alpine":100,"forest":3}


class Tile:
    def __init__(self, pos = (0,0), ttype = 'none'):
        self.pos   = pos
        self.ttype = ttype
        self.pop = 0
        self.owner=-1
        self.neighbours=[]
        self.town=False
        self.coastal=False
    def set_basics(self, pos = (0,0), ttype = 'none'):
        self.pos   = pos
        self.ttype = ttype
        self.pop = 0
        
    def set_population(self,pop):
        self.pop = pop

    def set_owner(self,owner):
        self.owner=owner

    def findneighbours(self,travel,size,world):
        shortest={}
        neighbours=[]
        for i in range(max(self.pos[0]-travel-1,0),min(self.pos[0]+travel+1,size[0])):
            for j in range(max(self.pos[1]-travel-1,0),min(self.pos[1]+travel+1,size[1])):
                shortest[(i,j)]=[size[0]*size[1],False]
        shortest[self.pos][0]=0
        running=True
        while running:
            shortestdist=min([v[0] for v in shortest.values() if not v[1]])
            current=[k for k,v in shortest.items() if v[0]==shortestdist and not v[1]][0]
            if shortest[current][0]>=travel:
                running=False
            else:
                for i in (-1,0,1):
                    for j in (-1,0,1):
                        if abs(i+j)==1 and -1<current[0]+i and current[0]+i<size[0] and current[1]+j>-1 and current[1]+j<size[1]:
                            x,y=current[0]+i,current[1]+j
                            if world.tiles[x,y].coastal:
                                new=shortest[current][0]+1
                            else:
                                new=shortest[current][0]+move[world.tiles[x,y].ttype]
                            if new<shortest[(x,y)][0]:
                                shortest[x,y][0]=new
                shortest[current][1]=True
                if len([1 for v in shortest.values() if not v[1]])==0:
                    running=False
            
        return {world.tiles[k] for k,v in shortest.items() if v[0]<=travel}
                    
class Map:
    def __init__(self):
        print ('--------------------------------------------------------------------------------------------------------------')
        print ('Init map: reading file')
        print ('--------------------------------------------------------------------------------------------------------------')
        self.ntiles    = (400,200)
        self.nsize     = 80000
        self.rivers    = []
        self.tiles=self.generate()
        self.read_file()
        #self.define_alpine()
        self.add_rivers()
        self.display = None
        self.time=0
        print ('--------------------------------------------------------------------------------------------------------------')
        print ('Done.')
        print ('--------------------------------------------------------------------------------------------------------------')


    def generate(self):
        tiles=np.empty( (400,200), dtype=object)
        for x in range(400):
            for y in range(200):
                tiles[x,y]=Tile((x,y))
        return tiles      
    
    
    def read_file(self):
        with open("Biome_Data.csv") as rawdata:
            data = csv.reader(rawdata, delimiter=',')
            for row in data:
                x,y=int(row[0])-1,200-int(row[1])
                if int(row[4]) in (200,80,90):
                    self.tiles[x,y].ttype="sea"
                    for i in range(4):
                        self.tiles[(x-(i//2)),(y-(i%2))].coastal=True
                elif int(row[4])==60:
                    self.tiles[x,y].ttype="desert"
                elif int(row[4]) in (40,50):
                    self.tiles[x,y].ttype="plains"
                elif int(row[4]) in (20,30):
                    self.tiles[x,y].ttype="mountain"
                elif int(row[4]) in (70,100):
                    self.tiles[x,y].ttype="alpine"
                elif int(row[4]) >100 and int(row[4])<130:
                    self.tiles[x,y].ttype="forest"
                else:
                    self.tiles[x,y].ttype="mountain"

    def add_rivers(self):
        with open("rivers final.csv") as rawdata:
            data = csv.reader(rawdata, delimiter=',')
            for row in data:
                self.rivers.append(realriver(row,self))
        

    def check_for_river(self,tile):
        return (tile.ttype in PRIVER and PRIVER[tile.ttype]>rnd.random())

    def make_river(self,rid,pos):
        river = rivers.River(rid,pos,self)
        river.meander(self)
        for pos in river.links:
            for i in range(4):
                current=self.tiles[(pos[0]-(i//2),pos[1]-(i%2))]
                current.coastal=True
                #if current.ttype=="desert":
                 #   current.ttype="plains"
        return river

    
    def init_display(self,tdim,margin):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Synthetic Map Generation')
        screen = pygame.display.set_mode( (400*tdim[0], 200*tdim[1]) )
        self.display = display.MapDisplay(self,screen,tdim,margin)

    def draw_display(self):
        self.time+=1
        if self.display:
            self.display.draw_map(self.time)

class realriver:
    def __init__(self,row,atlas):
        self.links=[]
        newrow=""
        for i in row[0]:
            if i in ("(",",",")"):
                newrow+=" "
            else:
                newrow+=i
        coords=newrow.split()
        for i in range(0,len(coords)-1,2):
            x,y=int((float(coords[i])+20.1)*5),int(200-(float(coords[i+1])-20.1)*5)
            self.links.append([x,y])
            for j in range(4):
                try:
                    current=atlas.tiles[(x-(j//2),y-(j%2))]
                    current.coastal=True
                except:
                    pass

if __name__ == '__main__' :
    #print ("Testing map generation")
    synth_map = Map()
    if DISPLAY:
        synth_map.init_display(TDIM,MARGIN)
        synth_map.draw_display()
    
