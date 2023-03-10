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
        return smaps.Map(ntiles,maptype)
            

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
        if tile.pop==0:
            tile.set_population(40*random())
        tile.food=food[tile.ttype]
        self.squares=[tile]
        self.travel=5
        self.towntithe=1
        self.town=False
        self.army=0
        tile.neighbours=[]
        for i in (-1,0,1):
            for j in (-1,0,1):
                newx=self.x+i
                newy=self.y+j
                if abs(i+j)==1 and -1<newx and newx<ntiles[0] and newy>-1 and newy<ntiles[1] and world.smap.tiles[newx,newy].ttype not in ("sea","alpine"):
                    crossing=False
                    for river in world.smap.rivers:
                        if [max(self.x,newx),max(self.y,newy)] in river.links:
                            crossing=True
                    tile.neighbours.append((world.smap.tiles[newx,newy],crossing))
        self.nomad=False
        if tile.ttype=="desert":
            self.nomad=True
    def tilefull(self,tile,moving,travel):
        new,crossing=choice(tile.neighbours)
        if new.coastal:
            travel-=1
        else:
            travel-=move[new.ttype]
        if travel>-1 and moving>0:
            if new.owner==-1:
                new.pop=moving
                self.gainsquare(new)
                return False,False,False
            elif new.owner==self.no:
                if new.town:
                    settling=tile.food+self.produce*(1-maxtax)-new.pop
                else:
                    settling=new.food*self.towntithe-new.pop
                if settling>0:
                    new.pop+=min(settling,moving)
                    moving=max(0,moving-settling)
                return self.tilefull(new,moving,travel)
            else:
                        
                return new,moving,crossing
        else:
            return False,False,False
                
    def tick(self):
        full=0
        targets={}
        self.produce=max(1,sum([source.food for source in self.squares if not source.town]))
        for tile in self.squares:
            #If empty
            if tile.pop<0:
                tile.owner=-1
                tile.pop=0
                self.squares=[owned for owned in self.squares if owned!=tile]
            elif tile.town==True:
                self.towntithe=1-max(0,(tile.pop-tile.food))/self.produce
                self.army=tile.pop*militia
                if self.towntithe<maxtax:
                    new,moving,crossing=self.tilefull(tile,self.produce*(maxtax-self.towntithe),self.travel)
                    tile.pop=tile.food+self.produce*(1-maxtax)
                    self.towntithe=maxtax
                    if new:
                        targets[new] = (targets.get(new, (0,False))[0] + moving,crossing)
            elif tile.pop>tile.food-self.towntithe:
                if not self.town:
                    full+=1
                    if full>4:
                        sites=[site for site in self.squares if site.coastal]
                        if sites:
                            capital=choice(sites)
                            capital.town=True
                            self.town=capital
                            self.homeland=capital.findneighbours(self.travel,ntiles,world.smap)
                            self.produce=max(1,sum([source.food for source in self.squares if not source.town]))
                new,moving,crossing=self.tilefull(tile,tile.pop-tile.food*self.towntithe,self.travel)
                tile.pop=min(tile.pop,tile.food*self.towntithe)
                if new:
                    targets[new] = (targets.get(new, (0,False))[0] + moving,crossing)
                
        newcivs=[]
        if targets:
            rebel=0
            for target,army in targets.items():
                newciv = self.combat(target,army[0]+self.army/len(targets),army[1])
                if newciv:
                    newcivs.append(newciv)
                if self.town:
                    if target not in self.homeland:
                        rebel+=1
            if rebel and len(targets)!=rebel:
                if (math.tanh(combatmod*math.log(rebel/(len(targets)-rebel)))+1)/2>=random():
                    rebellion=choice(list(targets.keys()))
                    newcivs.append(rebellion)
        if newcivs:
            return newcivs
        elif not self.squares:
            return "del"
        else:
            return False
    def combat(self,target,army,crossing):
        targetagent=agents[target.owner]
        defence=target.pop*militia#+targetagent.army
        defence*=(defencebonus[target.ttype]+riverbonus*crossing)
        if defence<=0:
            victorychance=1
        else:
        
            victorychance=(math.tanh(combatmod*math.log(army*armybonus/defence))+1)/2
        if targetagent.town:
            targetagent.town.pop*(1-random()*militia*loss)
        if victorychance>=random():
            newciv=self.gainsquare(target)
            if newciv:
                target.pop+=self.produce/10
                for square in self.squares:
                    square.pop*=0.9
            target.pop=target.pop*(1-random()*militia*loss)+army*(1-random()*loss)
            return newciv
        else:
            target.pop=target.pop*(1-random()*militia*loss)
        return False
            
    def gainsquare(self,target):
        if self.nomad and target.ttype!="desert":
            target.town=False
            return target
            
        elif self.nomad or target.ttype!="desert":
            if target.owner!=-1:
                targetagent=agents[target.owner]
                targetagent.squares=[square for square in targetagent.squares if square!=target]
                if target.town:
                    targetagent.town=False
            target.owner=self.no
            self.squares.append(target)
            target.town=False
        return False
        
        


ntiles   = (150, 80)
tilesize      = (12, 12)
margin  = 1
maptype = "continent"

popgrowth=1.05
food={"plains":1000,"desert":200,"mountain":100,"alpine":0,"sea":0}
defencebonus={"plains":1,"desert":1.2,"mountain":2}
riverbonus=2
armybonus=1
move={"plains":2,"desert":2,"mountain":3,"sea":4}
combatmod=3
loss=0.5
militia=0.1
maxtax=0.8


world = map(maptype,ntiles)
world.init_display(tilesize,margin)
nomadcount=1
agents={}
for i in range(ntiles[0]):
    for j in range(ntiles[1]):
        if world.smap.tiles[(i,j)].ttype not in ["sea","alpine"]:
            agents[i+j*ntiles[0]]=civ(i+j*ntiles[0],i,j)
world.draw()
while True:
    for i in range(ntiles[0]):
        for j in range(ntiles[1]):
            world.smap.tiles[(i,j)].pop*=popgrowth
    remove,add=[],[]
    for key,a in agents.items():
        changes=a.tick()
        if changes=="del":
            remove.append(key)
        elif changes:
            add+=changes
    for key in remove:
        del agents[key]
    for new in add:
        agents[ntiles[0]*ntiles[1]+nomadcount]=civ(ntiles[0]*ntiles[1]+nomadcount,new.pos[0],new.pos[1])
        nomadcount+=1
    world.draw()
print("fin")



