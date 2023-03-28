from random import *
import matplotlib.pyplot as plt
import numpy as np      
import real_maps as smaps 
import pygame
import time
import math


class map():
    def __init__(self):
        self.smap          = self.init_map()
    
    def init_map(self):
        return smaps.Map()
            

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
        tile.neighbours=tile.findneighbours(self.travel,ntiles,world.smap)
        self.nomad=False
        if tile.ttype=="desert":
            self.nomad=True
        tile.touching=[]
        for i in (-1,0,1):
            for j in (-1,0,1):
                newx=self.x+i
                newy=self.y+j
                if abs(i+j)==1 and -1<newx and newx<ntiles[0] and newy>-1 and newy<ntiles[1] and world.smap.tiles[newx,newy].ttype not in ("sea","alpine"):
                    if world.smap.tiles[newx,newy].ttype!="desert" or self.nomad:
                        crossing=False
                        for river in world.smap.rivers:
                            if [max(self.x,newx),max(self.y,newy)] in river.links:
                                crossing=True
                        tile.touching.append([world.smap.tiles[newx,newy],crossing])
        self.towntithe=1
        self.town=False
        self.army=0
    def tilefull(self,tile,moving,travel):
        if tile.touching:
            new,crossing=choice(tile.touching)
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
                            self.produce=max(1,sum([source.food for source in self.squares if not source.town]))
                new,moving,crossing=self.tilefull(tile,tile.pop-tile.food*self.towntithe,self.travel)
                tile.pop=min(tile.pop,tile.food*self.towntithe)
                if new:
                    targets[new] = (targets.get(new, (0,False))[0] + moving,crossing)
                
                    


        newcivs=[]
        if targets:
            armytarget=[]
            rebel=0
            if self.town:
                targetsize=ntiles[1]*ntiles[0]
                
                civtarget=-1
                for target,army in targets.items():
                    if target.owner!=-1:
                        if target.town:
                            armytarget=[target]
                            targetsize=1
                        elif len(agents[target.owner].squares)<targetsize and agents[target.owner].nomad==self.nomad :
                            targetsize=len(agents[target.owner].squares)
                            armytarget=[target]
                            civtarget=target.owner
                        elif target.owner==civtarget:
                            armytarget+=[target]
                        
            for target,army in targets.items():
                if target.owner==-1:
                    newciv=self.gainsquare(target)
                    if newciv:
                        newcivs.append(newciv)
                elif target.owner!=self.no:
                    if target in armytarget:
                        newciv = self.combat(target,army[0],self.army/len(armytarget),army[1])
                    else:
                        newciv = self.combat(target,army[0],0,army[1])
                    if newciv:
                        newcivs.append(newciv)
                    if self.town:
                        if target not in self.town.neighbours:
                            rebel+=1
                
            if rebel and len(targets)!=rebel:
                if (math.tanh(combatmod*math.log(rebel/(len(targets)-rebel)))+1)/2>=random():
                    rebellion=choice(list(targets.keys()))
                    rebellion.pop+=self.army*rebel/(len(targets))
                    self.town.pop-=self.army*rebel/(len(targets))
                                                    
                    newcivs.append(rebellion)
        if newcivs:
            return newcivs
        elif not self.squares:
            return "del"
        else:
            return False
    def combat(self,target,mob,army,crossing):
        targetagent=agents[target.owner]
        attackers=[pos for pos in target.neighbours if pos.owner == self.no]
        defenders=[pos for pos in target.neighbours if pos.owner == targetagent.no]
        defendingarmy=0
        if mob>target.pop*militia:
            defendingarmy=targetagent.army
        attack=sum(pos.pop*militia for pos in attackers)+mob+army*armybonus
        defence=sum(pos.pop*militia for pos in defenders)+defendingarmy*armybonus
        defence*=(defencebonus[target.ttype]+riverbonus*crossing)
        if defence<=0:
            victorychance=1
        elif attack<=0:
            victorychance=0
        else:
            victorychance=(math.tanh(combatmod*math.log(attack/defence))+1)/2
        if victorychance>=random():
            newciv=self.gainsquare(target)
            if newciv and self.nomad:
                exodus=0
                for square in self.squares:
                    exodus+=square.pop*0.1
                    square.pop*=0.9
                target.pop+=exodus
            for pos in attackers:
                pos.pop*=(1-random()*victoryloss*militia)
            for pos in defenders:
                pos.pop*=(1-random()*defeatloss*militia)
            if targetagent.town:
                targetagent.town.pop-=defendingarmy*(1-random()*defeatloss)
            target.pop+=mob*(1-random()*victoryloss)
            if self.town:
                self.town.pop-=army*(1-random()*victoryloss)
            return newciv
        else:
            for pos in attackers:
                pos.pop*=(1-random()*stalemate*militia)
            for pos in defenders:
                pos.pop*=(1-random()*stalemate*militia)
            if targetagent.town:
                targetagent.town.pop-=defendingarmy*(1-random()*stalemate)
            if self.town:
                self.town.pop-=army*(1-random()*stalemate)
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
        


ntiles   = (400, 200)
tilesize      = (6, 6)
margin  = 1

popgrowth=1.05
food={"plains":1000,"desert":50,"mountain":100,"alpine":0,"sea":0,"forest":200}
defencebonus={"plains":1,"desert":1.2,"mountain":2,"forest":2}
riverbonus=2
armybonus=10
move={"plains":2,"desert":2,"mountain":3,"sea":4,"forest":3}
combatmod=3
militia=0.05
victoryloss=0.1
defeatloss=0.5
stalemate=0.2
maxtax=0.8
world = map()
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



