from random import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
class baseagent:
    def __init__(self,no):
        self.no=no
        self.aggro=random()
        self.x=randint(0,size-1)
        self.y=randint(0,size-1)
        self.squares=[self.x+self.y*size]
        self.size=1
        grid[self.x][self.y]=self.no
    def neighbour(self,square):
        targets=[]
        for i in (-1,0,1):
            for j in (-1,0,1):
                x=square%size+i
                y=square//size+j
                if abs(i+j)==1 and -1<x and x<size and y>-1 and y<size and grid[x][y]!=self.no:
                    targets.append([grid[x][y],x,y])
        return targets
    def combat1(self,a,target,x,y):
        return target.size<a.size
    def combat2(self,a,target,x,y):
        return a.size>random()*(a.size+target.size)
    def combat3(self,a,target,x,y):
        return False
    def combat4(self,a,target,x,y):
        return random()>0.5

    
    def combat(self,a,target,x,y):
        return self.combat2(a,target,x,y)
    
    def growth(self):
        surrounded=True
        while surrounded:
            
            square=int(choice(self.edgesquares))
            self.edgesquares.remove(square)
            targets=self.neighbour(square)
            if len(targets)!=0 or len(self.edgesquares)==0:
                surrounded=False
        
        for target in targets:
            targetno,x,y=target[0],target[1],target[2]
            targetagent=agents[targetno]
            if targetno==-1:
                grid[x][y]=self.no
                self.size+=1
                newsquare=x+y*size
                self.squares.append(newsquare)
                self.edgesquares.append(newsquare)
            elif self.combat(self,targetagent,x,y):
                grid[x][y]=self.no
                newsquare=x+y*size
                try:
                    targetagent.edgesquares.remove(newsquare)
                except:
                    pass
                self.squares.append(x+y*size)
                self.edgesquares.append(newsquare)
                targetagent.squares.remove(newsquare)
                self.size+=1
                targetagent.size-=1
                targetneighbour=targetagent.neighbour(newsquare)
                for newtarget in targetneighbour:
                    if newtarget[0]==targetagent.no:
                        targetagent.edgesquares.append(newtarget[1]+newtarget[2]*size)
        
class agent8(baseagent):
    def __init__(self,no):
        super().__init__(no)
        self.edgesquares=[self.x+self.y*size]
    def neighbour(self,square):
        targets=[]
        for i in (-1,0,1):
            for j in (-1,0,1):
                x=square%size+i
                y=square//size+j
                if abs(i)+abs(j)>0 and -1<x and x<size and y>-1 and y<size and grid[x][y]!=self.no:
                    targets.append([grid[x][y],x,y])
        return targets

class agent4(baseagent):
    def __init__(self,no):
        super().__init__(no)
        self.edgesquares=[self.x+self.y*size]
class agent1(baseagent):
    def __init__(self,no):
        super().__init__(no)
        neighbours=self.neighbour(self.x+self.y*size)
        self.edgesquares=[i[1]+i[2]*size for i in neighbours]
    def growth(self):
        target=choice(self.edgesquares)
        self.edgesquares.remove(target)
        x,y=target%size,target//size
        targetno=grid[x][y]
        targetagent=agents[targetno]
        if targetno==-1:
            grid[x][y]=self.no
            self.size+=1
            self.squares.append(target)
            neighbours=self.neighbour(target)
            self.edgesquares+=[i[1]+i[2]*size for i in neighbours]
                
        elif self.combat(a,targetagent,x,y):
            grid[x][y]=a.no
            targetagent.edgesquares.append(target)
            self.squares.append(target)
            targetagent.squares.remove(target)
            self.size+=1
            targetagent.size-=1
            targetneighbour=targetagent.neighbour(target)
            self.edgesquares+=[i[1]+i[2]*size for i in targetneighbour]


n=50
size=50
fig,ax=plt.subplots(2)
ax[0].set_ylim(0,size, auto=False)
ax[0].set_xlim(0,size, auto=False)
fig.set_size_inches(3.5, 6.75)
fig.set_tight_layout(True)
fig.set_dpi(120)
grid = [[-1 for i in range(size)] for j in range(size)]
agents=[]
for i in range(n):    
    a=agent1(i)
    agents.append(a)
change=1



bar=ax[1].bar(range(n),[a.size for a in agents],color=["C%d" %a.no for a in agents])
while change!=0:
    ax[0].clear()
    ax[0].set_ylim(0,size, auto=False)
    ax[0].set_xlim(0,size, auto=False)
    ax[1].set_ylim(0,2500, auto=True)
    for a in agents:
        surrounded=True
        if len(a.edgesquares)!=0:
            a.growth()
                    
                    
        

        ax[0].scatter([i%size for i in a.squares],[j//size for j in a.squares],marker="s",s=16)
        bar[a.no].set_height(a.size)
        #ax.plot([i%size for i in a.edgesquares],[j//size for j in a.edgesquares],"sC%d" %int(a.no+5))
    
    plt.show(block=False)
    plt.pause(0.001)
