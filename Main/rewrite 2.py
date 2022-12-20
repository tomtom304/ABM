from random import *
import matplotlib.pyplot as plt
import numpy as np      

class tile():
    def __init__(self,x,y):
        self.terrain=plain
        self.x,self.y=x,y
        self.river=""
        self.neighbours=[]
        for i in (-1,0,1):
            for j in (-1,0,1):
                if abs(i+j)==1 and -1<x+i and x+i<width and y+j>-1 and y+j<height:
                    self.neighbours.append([x+i,y+j])
        self.neighbours=np.array(self.neighbours)
        self.owner=-1
        self.pop=0
class world():
    def __init__(self,width,height):
        self.tiles=self.generate(width,height)
    def generate(self, width, height):
        tiles=np.empty( (width,height), dtype=object)
        for x in range(width):
            for y in range(height):
                tiles[x,y]=tile(x,y)
        return tiles

        
class civ():
    def __init__(self,no):
        self.no=no
        self.x=randint(0,width-1)
        self.y=randint(0,height-1)
        while world.tiles[self.x,self.y].owner!=-1:
            self.x=randint(0,width-1)
            self.y=randint(0,height-1)
        world.tiles[self.x,self.y].owner=self.no
        world.tiles[self.x,self.y].pop=100
        self.edgesquares=[[self.x,self.y]]
        self.squares=[[self.x,self.y]]
    def tick(self):
        for square in self.squares:
            tile=world.tiles[tuple(square)]
            tile.pop*=popgrowth
            if tile.pop>tile.terrain["food"]:
                if square in self.edgesquares:
                    self.expand(tile)
                else:
                    new=world.tiles[tuple(choice(tile.neighbours))]
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
        targets=[world.tiles[tuple(newsquare)] for newsquare in target.neighbours if not any((newsquare == x).all() for x in self.squares)]
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
popgrowth=1.05
plain={"food":100,"defence":1,"move":1}
desert={"food":10,"defence":2,"move":1}
mountain={"food":20,"defence":3,"move":2}
   
n=10
width=80
height=50
fig,ax=plt.subplots(2)
ax[0].set_ylim(0,height, auto=False)
ax[0].set_xlim(0,width, auto=False)
fig.set_size_inches(5.25, 6.75)
fig.set_tight_layout(True)
fig.set_dpi(125)
world = world(width,height)
agents=[]
for i in range(n):    
    a=civ(i)
    agents.append(a)
    ax[0].scatter([i[0] for i in a.squares],[i[1] for i in a.squares],marker="s",s=16)
ax[1].set_ylim(0,width*height, auto=True)
while True:
    print("tick")
    ax[0].clear()
    ax[0].set_ylim(-1,height, auto=False)
    ax[0].set_xlim(-1,width, auto=False)
    for a in agents:
        a.tick()
        ax[0].scatter([i[0] for i in a.squares],[i[1] for i in a.squares],marker="s",s=16)
        #ax[0].scatter([i[0] for i in a.edgesquares],[i[1] for i in a.edgesquares],marker="s",s=16, color="C%d" %int(a.no+1))
    plt.show(block=False)
    plt.pause(0.001)
print("fin")

