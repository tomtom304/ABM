from random import *
#import matplotlib.pyplot as plt
import numpy as np      
import real_maps_data as smaps 
import time
import math

class map():
    def __init__(self):
        self.smap          = self.init_map()
    
    def init_map(self):
        return smaps.Map()
            
        
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
                    settling=new.food-new.pop
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
        for tile in self.squares:
            #If empty
            if tile.pop<0:
                tile.owner=-1
                tile.pop=0
                self.squares=[owned for owned in self.squares if owned!=tile]
            if tile.pop>tile.food:
                new,moving,crossing=self.tilefull(tile,tile.pop-tile.food,self.travel)
                tile.pop=min(tile.pop,tile.food)
                if new:
                    targets[new] = (targets.get(new, (0,False))[0] + moving,crossing)
                
                    


        newcivs=[]
        rebel=0
        conflictlist=[]
        for target,army in targets.items():
            if target.owner!=-1:
                newciv = self.combat(target,army[0],army[1])
                if self.nomad==agents[target.owner].nomad:
                    conflictlist+=[target]
                if newciv:
                    newcivs.append(newciv)
                    
                
            else:
                self.gainsquare(target)
        if newcivs:
            return newcivs,conflictlist
        elif not self.squares:
            return "del",conflictlist
        else:
            return False,conflictlist
    def combat(self,target,mob,crossing):
        targetagent=agents[target.owner]
        attackers=[pos for pos in target.neighbours if pos.owner == self.no]
        defenders=[pos for pos in target.neighbours if pos.owner == targetagent.no]
        attack=sum(pos.pop*militia for pos in attackers)+mob
        defence=sum(pos.pop*militia for pos in defenders)
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
            target.pop+=mob*(1-random()*victoryloss)
            return newciv
        else:
            for pos in attackers:
                pos.pop*=(1-random()*stalemate*militia)
            for pos in defenders:
                pos.pop*=(1-random()*stalemate*militia)
        return False
    def gainsquare(self,target):
        if self.nomad and target.ttype!="desert":
            return target
            
        elif self.nomad or target.ttype!="desert":
            if target.owner!=-1:
                targetagent=agents[target.owner]
                targetagent.squares=[square for square in targetagent.squares if square!=target]
            target.owner=self.no
            self.squares.append(target)
        return False
        


ntiles   = (400, 200)
tilesize      = (6, 6)
margin  = 1

popgrowth=1.05
food={"plains":1000,"desert":50,"mountain":100,"alpine":0,"sea":0,"forest":200}
defencebonus={"plains":1,"desert":1.2,"mountain":2,"forest":2}
riverbonus=2
move={"plains":2,"desert":2,"mountain":3,"sea":4,"forest":3}
combatmod=1
militia=0.05
victoryloss=0.1
defeatloss=0.5
stalemate=0.3
maxtax=0.8
#fig,ax=plt.subplots()
#fig.set_tight_layout(True)
world = map()
nomadcount=1


agents={}
for i in range(ntiles[0]):
    for j in range(ntiles[1]):
        if world.smap.tiles[(i,j)].ttype not in ["sea","alpine"]:
            agents[i+j*ntiles[0]]=civ(i+j*ntiles[0],i,j)
#print("civs init")
time=1
popdist=[]
longevitydata=np.array([[0 for i in range(ntiles[1])] for j in range(ntiles[0])])
conflictdata=np.array([[0 for i in range(ntiles[1])] for j in range(ntiles[0])])
popdata=np.array([[0 for i in range(ntiles[1])] for j in range(ntiles[0])])
sizedata=[]
end=2000
while time<end:
    time+=1
    for i in range(ntiles[0]):
        for j in range(ntiles[1]):
            currenttile=world.smap.tiles[(i,j)]
            currenttile.pop*=popgrowth
            if currenttile.owner!=-1:
                longevitydata[(i,j)]+=len(agents[currenttile.owner].squares)
                popdata[(i,j)]+=min(currenttile.pop,food[currenttile.ttype])/food[currenttile.ttype]
    remove,add=[],[]
    for key,a in agents.items():
        changes,fights=a.tick()
        if changes=="del" or len(a.squares)==0:
            remove.append(key)
        elif changes:
            add+=changes
        for fight in fights:
            conflictdata[fight.pos]+=1
    for key in remove:
        del agents[key]
    for new in add:
        agents[ntiles[0]*ntiles[1]+nomadcount]=civ(ntiles[0]*ntiles[1]+nomadcount,new.pos[0],new.pos[1])
        nomadcount+=1
    #sizedata+=[np.sort(-np.partition(-np.array([len(a.squares) for a in agents.values()]),5)[:5])]
    #popdist+=[np.sort(-np.partition(-np.array([sum([tile.pop for tile in a.squares]) for a in agents.values()]),5)[:5])]
    sizedata+=[np.percentile(np.array([len(a.squares) for a in agents.values() if len(a.squares)>1]+[1]),[1,25,50,75,100])]
    popdist+=[np.percentile(np.array([sum([tile.pop for tile in a.squares]) for a in agents.values() if len(a.squares)>0]),[0,25,50,75,100])]
np.save("longevity",longevitydata)
np.save("pop",popdata)
np.save("conflict",conflictdata)
sizedata=np.array(sizedata)
np.save("sizedist",sizedata)
popdist=np.array(popdist)
np.save("popdist",popdist)
#for i in range(5):
#    plt.plot(range(end-1),sizedata[:,i],label="mean size")
#plt.show()
    
print("fin")



