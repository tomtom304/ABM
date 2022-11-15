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
                if abs(i+j)==1 and -1<x and x<size and y>-1 and y<size:
                    targets.append([grid[x][y],x,y])
        return targets
    
    
    def growth(self):
        surrounded=True
        while surrounded:
            
            square=int(choice(self.edgesquares))
            self.edgesquares.remove(square)
            targets=[a for a in self.neighbour(square) if a[0]!=self.no]
            if len(targets)!=0 or len(self.edgesquares)==0:
                surrounded=False
        
        for target in targets:
            targetno,x,y=target[0],target[1],target[2]
            targetagent=agents[targetno]
            newsquare=x+y*size
            if targetno==-1:
                grid[x][y]=self.no
                self.size+=1
                
                self.squares.append(newsquare)
                self.edgesquares.append(newsquare)
            elif self.combat(self,targetagent,newsquare):
                grid[x][y]=self.no
                try:
                    targetagent.edgesquares.remove(newsquare)
                except:
                    pass
                self.squares.append(newsquare)
                self.edgesquares.append(newsquare)
                targetagent.squares.remove(newsquare)
                self.size+=1
                targetagent.size-=1
                targetneighbour=targetagent.neighbour(newsquare)
                for newtarget in targetneighbour:
                    if newtarget[0]==targetagent.no:
                        targetagent.edgesquares.append(newtarget[1]+newtarget[2]*size)
    def combat1(self,a,targetagent,targetsquare):
        return target.size<a.size
    def combat2(self,a,targetagent,targetsquare):
        return a.size>random()*(a.size+target.size)
    def combat3(self,a,targetagent,targetsquare):
        return False
    def combat4(self,a,targetagent,targetsquare):
        return random()>0.5
    def combat5(self,a,targetagent,targetsquare):
        combatants=self.neighbour(targetsquare)
        return len([a for a in combatants if a[0]==self.no])>=len([a for a in combatants if a[0]==targetagent.no])
    
    def combat(self,a,targetagent,targetsquare):
        return self.combat5(a,targetagent,targetsquare)    
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
                if abs(i)+abs(j)>0 and -1<x and x<size and y>-1 and y<size:
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
            neighbours=[a for a in self.neighbour(target) if a[0]!=self.no]
            self.edgesquares+=[i[1]+i[2]*size for i in neighbours]
                
        elif self.combat(a,targetagent,target):
            grid[x][y]=a.no
            targetagent.edgesquares.append(target)
            self.squares.append(target)
            targetagent.squares.remove(target)
            self.size+=1
            targetagent.size-=1
            targetneighbour=[a for a in targetagent.neighbour(target) if a[0]!=targetagent.no]
            self.edgesquares+=[i[1]+i[2]*size for i in targetneighbour]


n=5
size=50
fig,ax=plt.subplots(2)
ax[0].set_ylim(0,size, auto=False)
ax[0].set_xlim(0,size, auto=False)
fig.set_size_inches(3.5, 6.75)
fig.set_tight_layout(True)
fig.set_dpi(125)
grid = [[-1 for i in range(size)] for j in range(size)]
agents=[]
for i in range(n):    
    a=agent8(i)
    agents.append(a)
change=1



bar=ax[1].bar(range(n),[a.size for a in agents],color=["C%d" %a.no for a in agents])
while change!=0:
    ax[0].clear()
    ax[0].set_ylim(-1,size, auto=False)
    ax[0].set_xlim(-1,size, auto=False)
    ax[1].set_ylim(0,size**2, auto=True)
    for a in agents:
        surrounded=True
        if len(a.edgesquares)!=0:
            a.growth()
                    
                    
        

        ax[0].scatter([i%size for i in a.squares],[j//size for j in a.squares],marker="s",s=16)
        bar[a.no].set_height(a.size)
        #ax.plot([i%size for i in a.edgesquares],[j//size for j in a.edgesquares],"sC%d" %int(a.no+5))
    
    plt.show(block=False)
    plt.pause(0.001)
