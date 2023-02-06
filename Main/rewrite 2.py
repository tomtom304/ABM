from random import *
import matplotlib.pyplot as plt
import numpy as np      
import synthetic_maps as smaps 
import pygame
import time
import math


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
        self.travel=5
        tile.neighbours=tile.findneighbours(self.travel,ntiles,world.smap)
    def tick(self):
        for square in self.squares:
            tile=world.smap.tiles[square]
            if tile.pop<0:
                tile.owner=-1
                tile.pop=0
                self.squares=[pos for pos in self.squares if pos!=tile.pos]
            if not tile.surrounded:
                tile.set_population(tile.pop*popgrowth)
                if tile.pop>food[tile.ttype]:
                    emptytarget,selftarget,target=[],[],[]
                    #targets=[tuple([k,v]) for k,v in tile.neighbours if (world.smap.tiles[tuple([k,v])].owner!=self.no or world.smap.tiles[tuple([k,v])].pop<world.smap and world.smap.tiles[tuple([k,v])].ttype not in ["alpine","sea"]]
                    for pos in tile.neighbours:
                        new=world.smap.tiles[pos]
                        if new.ttype in ["alpine","sea"]:
                            pass
                        elif new.owner==-1:
                            emptytarget+=[pos]
                        elif new.owner==self.no and new.pop<food[new.ttype]/2:
                            selftarget+=[pos]
                        else:
                            target+=[pos]
                    if emptytarget:
                        new=world.smap.tiles[choice(emptytarget)]
                        self.gainsquare(new,tile)
                    elif selftarget:
                        new=world.smap.tiles[choice(selftarget)]
                        new.pop+=10
                        tile.pop-=10
                    elif target:
                        new=world.smap.tiles[choice(target)]
                        self.combat(new)
                    else:
                        tile.surrounded=True

                    tile.pop=min(tile.pop,food[tile.ttype])        
    def combat(self,target):
        targetagent=agents[target.owner]
        attackers=[pos for pos in target.findneighbours(self.travel,ntiles,world.smap) if world.smap.tiles[pos].owner == self.no]
        defenders=[pos for pos in target.findneighbours(targetagent.travel,ntiles,world.smap) if world.smap.tiles[pos].owner == targetagent.no]
        #attack=sum(world.smap.tiles[pos].army for pos in attackers)
        #defence=sum(world.smap.tiles[pos].army+world.smap.tiles[pos].pop*0.05 for pos in defenders)
        attack=sum(world.smap.tiles[pos].pop*0.05 for pos in attackers)
        defence=sum(world.smap.tiles[pos].pop*0.05 for pos in defenders)
        defence*=defencebonus[target.ttype]
        if defence<=0:
            victorychance=1
        elif attack<=0:
            victorychance=0
        else:
            victorychance=(math.tanh(combatmod*math.log(attack/defence))+1)/2
        if victorychance>=random():
            self.gainsquare(target,world.smap.tiles[choice(attackers)])
            for pos in attackers:
                #world.smap.tiles[pos].army*=(1-random()*0.05)
                world.smap.tiles[pos].pop*=(1-random()*0.05)
            for pos in defenders:
                world.smap.tiles[pos].pop*=(1-random()*0.3)
                world.smap.tiles[pos].surrounded=False
        else:
            for pos in attackers:
                #world.smap.tiles[pos].army*=(1-random()*0.05)
                world.smap.tiles[pos].pop*=(1-random()*0.1)
            for pos in defenders:
                world.smap.tiles[pos].pop*=(1-random()*0.1)
                world.smap.tiles[pos].surrounded=False
    def gainsquare(self,target,source):
        if target.owner!=-1:
            targetagent=agents[target.owner]
            targetagent.squares=[pos for pos in targetagent.squares if pos!=target.pos]
            if targetagent.travel!=self.travel:
                target.neighbours=target.findneighbours(self.travel,ntiles,world.smap)
        else:
            target.neighbours=target.findneighbours(self.travel,ntiles,world.smap)
        target.owner=self.no
        self.squares+=[target.pos]
        moving=10


        target.pop+=moving
        source.pop-=moving
        
        


ntiles   = (160, 90)
tilesize      = (12, 12)
margin  = 1
maptype = 'continent'

popgrowth=1.05
food={"plains":1000,"desert":200,"mountain":100,"alpine":0,"sea":0}
defencebonus={"plains":1,"desert":1.2,"mountain":2}
move={"plains":1,"desert":1,"mountain":2,"sea":3}
combatmod=1
   
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



