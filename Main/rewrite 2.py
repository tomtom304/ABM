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
        while world.smap.tiles[self.x,self.y].owner!=-1 or world.smap.tiles[self.x,self.y].ttype in ["sea","alpine"]:
            self.x=randint(0,ntiles[0]-1)
            self.y=randint(0,ntiles[1]-1)
        world.smap.tiles[self.x,self.y].owner=self.no
        world.smap.tiles[self.x,self.y].population=100
        self.squares=[[self.x,self.y]]
        self.travel=3
    def tick(self):
        for square in self.squares:
            tile=world.smap.tiles[tuple(square)]
            tile.pop*=popgrowth
            if tile.pop>tile.ttype["food"]:
                new=world.smap.tiles[tuple(choice(tile.neighbours))]
                if new.owner != self.no and new.ttype not in ["alpine","sea"]:
                    self.gainsquare(new)
                moving = (tile.pop-tile.ttype["food"])*(1+random())
                new.pop+=moving
                tile.pop-=moving
##    def combat(self,targetagent,targetsquare,terrain):
##        return self.c.combat2(self,targetagent,targetsquare)
    def gainsquare(self,target):
        target.owner=self.no
        self.squares+=[[target.x,target.y]]
##    def losesquare(self,a,x,y,square):
##        self.edgesquares=self.edgesquares[self.edgesquares!=[x,y]]
##        self.squares=self.squares[self.squares!=[x,y]]
##        for i in world.tiles[x,y].neighbours:
##            if i not in self.edgesquares and i in self.squares:
##                    self.edgesquares+=[[x,y]]


ntiles   = (200, 100)
tilesize      = (8, 8)
margin  = 1
maptype = 'continent'

popgrowth=1.05

   
n=8

world = map(maptype,ntiles)
world.init_display(tilesize,margin)
agents=[]
for i in range(n):    
    a=civ(i)
    agents.append(a)
world.draw()
while True:
    
    for a in agents:
        a.tick()
    world.draw()
    print("tick")
print("fin")



