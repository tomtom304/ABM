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
        self.towntithe=1
        self.town=False
        self.army=0
        tile.neighbours=[]
        self.colour=(random(),random(),random())
        self.produce=1
        self.nomad=False
        if tile.ttype=="desert":
            self.nomad=True
        tile.neighbours=[]
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
                        tile.neighbours.append((world.smap.tiles[newx,newy],crossing))
    def tilefull(self,tile,moving,travel):
        if tile.neighbours:
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
                    tile.pop=tile.food*maxtax+self.produce*(1-maxtax)
                    self.towntithe=maxtax
                    if new:
                        targets[new] = (targets.get(new, (0,False))[0] + moving,crossing)
            elif tile.pop>tile.food*self.towntithe:
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
        rebel=0
        conflictlist=[]
        for target,army in targets.items():
            if target.owner!=-1:
                newciv = self.combat(target,army[0],self.army/len(targets),army[1])
                if self.nomad==agents[target.owner].nomad:
                    conflictlist+=[target]
                if newciv:
                    newcivs.append(newciv)
                if self.town:
                    if target not in self.homeland:
                        rebel+=1
            else:
                self.gainsquare(target)
        if targets:
            if rebel/len(targets)>0:
                victorychance=(math.tanh(combatmod*math.log(rebel/len(targets)))+1)/2
                if victorychance>=random():
                    rebellion=choice(list(targets.keys()))
                    rebellion.pop+=self.army-rebel/(len(targets))
                    self.town.pop-=self.army-rebel/(len(targets))

                    newcivs.append(rebellion)

        if newcivs:
            return newcivs,conflictlist
        elif not self.squares:
            return "del",conflictlist
        else:
            return False,conflictlist
    def combat(self,target,mob,army,crossing):
        targetagent=agents[target.owner]
        defendingarmy=0
        #if mob>target.pop*militia:
        #    defendingarmy=targetagent.army
        defence=target.pop*militia+defendingarmy*armybonus
        defence*=(defencebonus[target.ttype]+riverbonus*crossing)
        attack=mob+army*armybonus
        if defence<=0:
            victorychance=1
        elif attack<=0:
            victorychance=0
        else:
        
            victorychance=(math.tanh(combatmod*math.log(attack/defence))+1)/2
        if targetagent.town:
            targetagent.town.pop-=defendingarmy*(1-random()*loss)
        if self.town:
            self.town.pop-=army*(1-random()*loss)
        if victorychance>=random():
            newciv=self.gainsquare(target)
            if newciv and self.nomad:
                exodus=0
                for square in self.squares:
                    exodus+=square.pop*0.1
                    square.pop*=0.9
                target.pop+=exodus
            target.pop=target.pop*(1-random()*militia*loss)+mob*(1-random()*loss)
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
loss=0.5
militia=0.05
maxtax=0.8

fig,ax=plt.subplots()
fig.set_tight_layout(True)

world = map()
nomadcount=1
agents={}
for i in range(ntiles[0]):
    for j in range(ntiles[1]):
        if world.smap.tiles[(i,j)].ttype not in ["sea","alpine"]:
            agents[i+j*ntiles[0]]=civ(i+j*ntiles[0],i,j)
time=1
popdist=[]
towndist=[]
longevitydata=np.array([[0 for i in range(ntiles[1])] for j in range(ntiles[0])])
conflictdata=np.array([[0 for i in range(ntiles[1])] for j in range(ntiles[0])])
towndata=np.array([[0 for i in range(ntiles[1])] for j in range(ntiles[0])])
popdata=np.array([[0 for i in range(ntiles[1])] for j in range(ntiles[0])])
sizedata=[]
end=2000
while time<end:
    time+=1
    for i in range(ntiles[0]):
        for j in range(ntiles[1]):
            world.smap.tiles[(i,j)].pop*=popgrowth
            if currenttile.owner!=-1:
                longevitydata[(i,j)]+=len(agents[currenttile.owner].squares)
                towndata[(i,j)]+=currenttile.town
                popdata[(i,j)]+=min(currenttile.pop,food[currenttile.ttype])/food[currenttile.ttype]
    remove,add=[],[]
    for key,a in agents.items():
        changes,fights=a.tick()
        if changes=="del" or len(a.squares)<1:
            remove.append(key)
        elif changes:
            add+=changes
        for fight in fights:
            conflictdata[fight.pos]+=1
    #deaddata+=[len(remove)]
    #newdata+=[len(add)]     
    for key in remove:
        
        del agents[key]
    for new in add:
        agents[ntiles[0]*ntiles[1]+nomadcount]=civ(ntiles[0]*ntiles[1]+nomadcount,new.pos[0],new.pos[1])
        nomadcount+=1
    #sizedata+=[max([max([tile.pop for tile in a.squares if tile.town]+[1]) for a in agents.values()])]
    sizedata+=[np.percentile(np.array([len(a.squares) for a in agents.values() if len(a.squares)>1]+[1]),[1,25,50,75,100])]
    popdist+=[np.percentile(np.array([sum([tile.pop for tile in a.squares]) for a in agents.values() if len(a.squares)>0]),[0,25,50,75,100])]
    towndist+=[np.percentile(np.array([sum([tile.pop for tile in a.squares if tile.town]) for a in agents.values() if len(a.squares)>0]),[0,25,50,75,100])]
    ######
#plt.plot(range(len(deaddata)),deaddata,label="mean size")
#plt.plot(range(len(newdata)),newdata,label="mean size")
np.save("longevity",longevitydata)
np.save("pop",popdata)
np.save("conflict",conflictdata)
sizedata=np.array(sizedata)
np.save("sizedist",sizedata)
popdist=np.array(popdist)
np.save("popdist",popdist)
towndist=np.array(towndist)
np.save("towndist",towndist)
print("fin")



