from random import *
import matplotlib.pyplot as plt
import numpy as np      
import synthetic_maps as smaps 
import pygame
import time


class map():
    def __init__(self,maptype,ntiles):
        self.smap          = self.init_map()
    
    def init_map(self):
        return smaps.Map(ntiles,maptype,n)
            
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
        tile=world.smap.tiles[self.x,self.y]
        tile.owner=self.no
        tile.set_population(100)
        self.squares=[tile.pos]
        self.travel=3
        tile.neighbours=tile.findneighbours(self.travel,ntiles,world.smap)
    def tick(self):
        for square in self.squares:
            tile=world.smap.tiles[square]
            if not tile.surrounded:
                tile.set_population(tile.pop*popgrowth)
                if tile.pop>food[tile.ttype]:
                    tile.full=True
                    targets=[tuple([k,v]) for k,v in tile.neighbours if world.smap.tiles[tuple([k,v])].owner!=self.no or not world.smap.tiles[tuple([k,v])].full]
                    if len(targets)==0:
                        tile.surrounded=True
                    else:
                        
                        new=world.smap.tiles[choice(targets)]
                        if new.ttype not in ["alpine","sea"]:
                            if new.owner!=-1:
                                pass
                                ##combat##
                            else:
                                self.gainsquare(new)
                                moving = (tile.pop-food[tile.ttype])*(1+random())
                                new.pop+=moving
                                tile.pop-=moving
                        else:
                            tile.pop==food[tile.ttype]
##    def combat(self,targetagent,targetsquare,terrain):
##        return self.c.combat2(self,targetagent,targetsquare)
    def gainsquare(self,target):
        target.owner=self.no
        self.squares+=[target.pos]
        target.neighbours=target.findneighbours(self.travel,ntiles,world.smap)
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
food={"plains":1000,"desert":200,"mountain":100,"alpine":0,"sea":0}
defence={"plains":1,"desert":2,"mountain":3}
move={"plains":1,"desert":1,"mountain":2,"sea":3}
   
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
print("fin")



