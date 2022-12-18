from random import *
import matplotlib.pyplot as plt
import numpy as np      

class tile():
    def __init__(self,x,y):
        self.terrain=""
        self.x,self.y=x,y
        self.river=""
        self.neighbours=[]
        for i in (-1,0,1):
            for j in (-1,0,1):
                if abs(i+j)==1 and -1<x+i and x+i<width and y+j>-1 and y+j<height:
                    self.neighbours.append([x,y])
        self.owner=0
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
        while world.tiles[self.x,self.y].owner!=0:
            self.x=randint(0,width-1)
            self.y=randint(0,height-1)
        world.tiles[self.x,self.y].owner=self.no
        world.tiles[self.x,self.y].pop=1
        self.edgesquares=np.array([[self.x,self.y]])
        self.squares=np.array([[self.x,self.y]])
##    def combat(self,targetagent,targetsquare,terrain):
##        return self.c.combat2(self,targetagent,targetsquare)
    def gainsquare(self,x,y):
        world.tiles[self.x,self.y].owner=self.no
        self.squares+=[[x,y]]
        self.edgesquares+=[[x,y]]
    def losesquare(self,a,x,y,square):
        self.edgesquares=self.edgesquares[self.edgesquares!=[x,y]]
        self.squares=self.squares[self.squares!=[x,y]]
        for i in world.tiles[x,y].neighbours:
            if i not in self.edgesquares and i in self.squares:
                    self.edgesquares+=[[x,y]]
    def expand(self):
        print("expanding")
        new=0
        surrounded=True
        while surrounded:
            square=choice(self.edgesquares)
            targets=[newsquare for newsquare in world.tiles[tuple(square)].neighbours if newsquare not in self.squares]
            print(targets)
            if len(targets)!=0:
                surrounded=False
            else:
                self.edgesquares=self.edgesquares[self.edgesquares!=square]
                if len(self.edgesquares)==0:
                    surrounded=False
                    new=1
        for target in targets:
            
            targetagent=agents[targetno]
            if terrain!=1:
                if targetno==-1:
                    self.gainsquare(x,y)
                    new+=1
##                elif self.combat(targetagent,newsquare,terrain):
##                    self.gainsquare(x,y,newsquare)
##                    targetagent.losesquare(self,x,y,newsquare)
##                    new+=1
        return new==0
    
n=4
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
    ax[0].scatter(a.squares[:,0],a.squares[:,1],marker="s",s=16)
change=n
end=0
ax[1].set_ylim(0,width*height, auto=True)
while end<5:
    change=n
    ax[0].clear()
    ax[0].set_ylim(-1,height, auto=False)
    ax[0].set_xlim(-1,width, auto=False)
    
    for a in agents:
        if len(a.edgesquares)!=0:
            if a.expand():
                change-=1
        else:
            change-=1
        ax[0].scatter(a.squares[:,0],a.squares[:,1],marker="s",s=16)
        ax[0].scatter([i%width for i in a.edgesquares],[j//width for j in a.edgesquares],marker="s",s=16, color="C%d" %int(a.no+5))
    if change==0:
        end+=1
    else:
        end=0
    plt.show(block=False)
    plt.pause(0.001)
print("fin")

