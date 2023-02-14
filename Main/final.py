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
    def __init__(self,no,x,y):
        self.draw=False
        self.no=no
        self.x=x
        self.y=y
        tile=world.smap.tiles[self.x,self.y]
        tile.owner=self.no
        tile.set_population(30+40*random())
        self.squares=[tile.pos]
        self.travel=5
        tile.neighbours=tile.findneighbours(self.travel,ntiles,world.smap)
        self.tech={"agri":1,"combat":1}
        self.towntithe=0
    def tilefull(self,tile,moving):
        emptytarget,selftarget,target=[],[],[]
        for pos in tile.neighbours:
            new=world.smap.tiles[pos]
            if new.ttype in ["alpine","sea"]:
                pass
            elif new.owner==-1:
                emptytarget+=[pos]
            elif new.owner==self.no and new.pop<new.food:
                selftarget+=[pos]
            else:
                target+=[pos]
        if emptytarget:
            new=world.smap.tiles[choice(emptytarget)]
            self.gainsquare(new)
            new.pop+=moving
            tile.pop-=moving
        elif selftarget:
            new=world.smap.tiles[choice(selftarget)]
            new.pop+=moving
            tile.pop-=moving
        elif target:
            new=world.smap.tiles[choice(target)]
            self.combat(new)
        else:
            tile.surrounded=True
    def checktech(self,full):
        if full>2:
            hometerrain=world.smap.tiles[(self.x,self.y)].ttype
            if hometerrain=="desert":
                self.travel=8
            elif hometerrain=="mountain":
                self.tech["combat"]=2
            elif hometerrain=="plains":
                self.tech["agri"]=2
        #if full>4:
            #world.smap.tiles[(self.x,self.y)].town=True
    def tick(self):
        full=0
        for square in self.squares:
            tile=world.smap.tiles[square]
            tile.food=food[tile.ttype]*self.tech["agri"]
            if tile.pop<0:
                tile.owner=-1
                tile.pop=0
                self.squares=[pos for pos in self.squares if pos!=tile.pos]
            if not tile.surrounded:
                tile.set_population(tile.pop*popgrowth)
                if tile.town==True:
                    self.towntithe=(tile.pop-tile.food)/len(self.squares)
                    if self.towntithe>20:
                        self.tilefull(tile)
                        tile.pop=tile.food+20*len(self.squares)
                elif tile.pop>tile.food-self.towntithe:
                    full+=1
                    if world.smap.tiles[(self.x,self.y)].town==False:
                        self.checktech(full)
                    self.tilefull(tile,tile.pop-tile.food+self.towntithe)
                    tile.pop=min(tile.pop,tile.food-self.towntithe)
            else:
                full+=1
                    


        if not self.squares:
            return True
        else:
            return False
    def combat(self,target):
        targetagent=agents[target.owner]
        if targetagent.travel!=self.travel:
            attackers=[pos for pos in target.findneighbours(self.travel,ntiles,world.smap) if world.smap.tiles[pos].owner == self.no]
        else:
            attackers=[pos for pos in target.neighbours if world.smap.tiles[pos].owner == self.no]
        defenders=[pos for pos in target.neighbours if world.smap.tiles[pos].owner == targetagent.no]
        #attack=sum(world.smap.tiles[pos].army for pos in attackers)
        #defence=sum(world.smap.tiles[pos].army+world.smap.tiles[pos].pop*0.05 for pos in defenders)
        attack=sum(world.smap.tiles[pos].pop*0.05 for pos in attackers)*self.tech["combat"]
        defence=sum(world.smap.tiles[pos].pop*0.05 for pos in defenders)*targetagent.tech["combat"]
        defence*=defencebonus[target.ttype]
        if defence<=0:
            victorychance=1
        elif attack<=0:
            victorychance=0
        else:
            victorychance=(math.tanh(combatmod*math.log(attack/defence))+1)/2
        if victorychance>=random():
            self.gainsquare(target)
            for pos in attackers:
                #world.smap.tiles[pos].army*=(1-random()*0.05)
                world.smap.tiles[pos].pop*=(1-random()*0.05)
            for pos in defenders:
                world.smap.tiles[pos].pop*=(1-random()*0.3)
                world.smap.tiles[pos].surrounded=False
        else:
            for pos in attackers:
                #world.smap.tiles[pos].army*=(1-random()*0.05)
                world.smap.tiles[pos].pop*=(1-random()*0.15)
            for pos in defenders:
                world.smap.tiles[pos].pop*=(1-random()*0.1)
                world.smap.tiles[pos].surrounded=False
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
        
        


ntiles   = (150, 80)
tilesize      = (12, 12)
margin  = 1
maptype = 'med'

popgrowth=1.05
food={"plains":1000,"desert":200,"mountain":100,"alpine":0,"sea":0}
defencebonus={"plains":1,"desert":1.2,"mountain":2}
move={"plains":1,"desert":1,"mountain":2,"sea":3}
combatmod=3
   
n=8

world = map(maptype,ntiles)
world.init_display(tilesize,margin)
agents={}
for i in range(ntiles[0]):
    for j in range(ntiles[1]):
        if world.smap.tiles[(i,j)].ttype not in ["sea","alpine"]:
            agents[i+j*ntiles[0]]=civ(i+j*ntiles[0],i,j)
world.draw()
while True:
    remove=[]
    for key,a in agents.items():
        if a.tick():
            remove.append(key)
    for key in remove:
        del agents[key]
    world.draw()
print("fin")



