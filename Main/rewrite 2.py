from random import *
import matplotlib.pyplot as plt
import numpy as np      
import synthetic_maps as smaps 
import pygame
import time



##class tile():
##    def __init__(self,x,y):
##        self.terrain=plain
##        self.x,self.y=x,y
##        self.river=""
##        self.neighbours=[]
##        for i in (-1,0,1):
##            for j in (-1,0,1):
##                if abs(i+j)==1 and -1<x+i and x+i<ntiles[0] and y+j>-1 and y+j<ntiles[1]:
##                    self.neighbours.append([x+i,y+j])
##        self.neighbours=np.array(self.neighbours)
##        self.owner=-1
##        self.pop=0
##class world():
##    def __init__(self,ntiles):
##        self.tiles=self.generate(ntiles)
##    def generate(self, ntiles):
##        tiles=np.empty( (ntiles[0],ntiles[1]), dtype=object)
##        for x in range(ntiles[0]):
##            for y in range(ntiles[1]):
##                tiles[x,y]=tile(x,y)
##        return tiles

class map():
    def __init__(self,maptype,ntiles):
        self.smap          = self.init_map()
    
    def init_map(self):
        return smaps.Map(maptype,ntiles)
            
##    def init_pops(self):
##        pass

    def init_display(self,tilesize,margin):
        self.smap.init_display(tilesize,margin)

    def draw(self):
        self.smap.draw_display()
        
class civ():
    def __init__(self,no):
        self.no=no
        self.x=randint(0,ntiles[0]-1)
        self.y=randint(0,ntiles[1]-1)
        while world.smap.tiles[self.x,self.y].owner!=-1 or world.smap.tiles[self.x,self.y].ttype=="sea":
            self.x=randint(0,ntiles[0]-1)
            self.y=randint(0,ntiles[1]-1)
        world.smap.tiles[self.x,self.y].owner=self.no
        world.smap.tiles[self.x,self.y].population=100
        self.edgesquares=[[self.x,self.y]]
        self.squares=[[self.x,self.y]]
    def tick(self):
        for square in self.squares:
            tile=world.smap.tiles[tuple(square)]
            tile.pop*=popgrowth
            if tile.pop>tile.terrain["food"]:
                if square in self.edgesquares:
                    self.expand(tile)
                else:
                    new=world.smap.tiles[tuple(choice(tile.neighbours))]
                    new.pop+=10
                    tile.pop-=10
##    def combat(self,targetagent,targetsquare,terrain):
##        return self.c.combat2(self,targetagent,targetsquare)
    def gainsquare(self,target):
        target.owner=self.no
        target.pop+=10
        self.squares+=[[target.x,target.y]]
        self.edgesquares+=[[target.x,target.y]]
##    def losesquare(self,a,x,y,square):
##        self.edgesquares=self.edgesquares[self.edgesquares!=[x,y]]
##        self.squares=self.squares[self.squares!=[x,y]]
##        for i in world.tiles[x,y].neighbours:
##            if i not in self.edgesquares and i in self.squares:
##                    self.edgesquares+=[[x,y]]
    def expand(self,target):
##        surrounded=True
##        while surrounded:
##            square=choice(self.edgesquares)
##            targets=[world.tiles[tuple(newsquare)] for newsquare in world.tiles[tuple(square)].neighbours if not any((newsquare == x).all() for x in self.squares)]
##            if len(targets)!=0:
##                surrounded=False
##            else:
##                self.edgesquares.remove(square)
##                if len(self.edgesquares)==0:
##                    surrounded=False
##                    new=1
        targets=[world.smap.tiles[tuple(newsquare)] for newsquare in target.neighbours if not any((newsquare == x).all() for x in self.squares)]
        if len(targets)==0:
            self.edgesquares.remove([target.x,target.y])
        else:
            new=choice(targets)
            if new.owner==-1:
                self.gainsquare(new)
                target.pop-=10
##                elif self.combat(targetagent,newsquare,terrain):
##                    self.gainsquare(x,y,newsquare)
##                    targetagent.losesquare(self,x,y,newsquare)

ntiles   = (200, 100)
tilesize      = (8, 8)
margin  = 1
maptype = 'continent'

popgrowth=1.05
plain={"food":100,"defence":1,"move":1}
desert={"food":10,"defence":2,"move":1}
mountain={"food":20,"defence":3,"move":2}
   
n=8

world = map(maptype,ntiles)
world.init_display(tilesize,margin)
##fig,ax=plt.subplots(2)
##ax[0].set_ylim(0,ntiles[1], auto=False)
##ax[0].set_xlim(0,ntiles[0], auto=False)
##fig.set_size_inches(5.25, 6.75)
##fig.set_tight_layout(True)
##fig.set_dpi(125)
##world = world(ntiles)
agents=[]
for i in range(n):    
    a=civ(i)
    agents.append(a)
    #ax[0].scatter([i[0] for i in a.squares],[i[1] for i in a.squares],marker="s",s=16)
#ax[1].set_ylim(0,ntiles[0]*ntiles[1], auto=True)


world.draw()


#while True:
##    print("tick")
##    ax[0].clear()
##    ax[0].set_ylim(-1,ntiles[1], auto=False)
##    ax[0].set_xlim(-1,ntiles[0], auto=False)
##    for a in agents:
##        a.tick()
##        ax[0].scatter([i[0] for i in a.squares],[i[1] for i in a.squares],marker="s",s=16)
##        #ax[0].scatter([i[0] for i in a.edgesquares],[i[1] for i in a.edgesquares],marker="s",s=16, color="C%d" %int(a.no+1))
##    plt.show(block=False)
##    plt.pause(0.001)
print("fin")



