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
        self.travel=6
        tile.neighbours=tile.findneighbours(self.travel,ntiles,world.smap)
    def tick(self):
        for square in self.squares:
            tile=world.smap.tiles[square]
            if not tile.surrounded:
                tile.set_population(tile.pop*popgrowth)
                if tile.pop>food[tile.ttype]:
                    targets=[tuple([k,v]) for k,v in tile.neighbours if world.smap.tiles[tuple([k,v])].owner!=self.no and world.smap.tiles[tuple([k,v])].ttype not in ["alpine","sea"]]
                    if len(targets)==0:
                        tile.surrounded=True
                        tile.pop==food[tile.ttype]
                    else:
                        new=world.smap.tiles[choice(targets)]
                            #if new.owner!=-1:
                                #pass
                                ##combat##
                            #else:
                        self.gainsquare(new)
                            #moving = (tile.pop-food[tile.ttype])
                        moving=10
                        new.pop+=moving
                        tile.pop-=moving
##    def combat(self,targetagent,targetsquare,terrain):
##        return self.c.combat2(self,targetagent,targetsquare)
    def gainsquare(self,target):
        if target.owner!=-1:
            targetagent=agents[target.owner]
            targetagent.squares=[pos for pos in targetagent.squares if pos!=target.pos]
            if targetagent.travel!=self.travel:
                target.neighbours=target.findneighbours(self.travel,ntiles,world.smap)
        else:
            target.neighbours=target.findneighbours(self.travel,ntiles,world.smap)
        target.owner=self.no
        self.squares+=[target.pos]
        


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



