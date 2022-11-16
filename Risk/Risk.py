from random import *
import matplotlib.pyplot as plt
class baseagent:
    def __init__(self,no):
        self.no=no
        self.aggro=random()
        self.x=randint(0,size-1)
        self.y=randint(0,size-1)
        self.squares=[self.x+self.y*size]
        self.size=1
        grid[self.x][self.y]=self.no

class neighbourtypes:
    def neighbour4(self,square):
        targets=[]
        for i in (-1,0,1):
            for j in (-1,0,1):
                x=square%size+i
                y=square//size+j
                if abs(i+j)==1 and -1<x and x<size and y>-1 and y<size:
                    targets.append([grid[x][y],x,y])
        return targets
    
    def neighbour8(self,square):
        targets=[]
        for i in (-1,0,1):
            for j in (-1,0,1):
                x=square%size+i
                y=square//size+j
                if abs(i)+abs(j)>0 and -1<x and x<size and y>-1 and y<size:
                    targets.append([grid[x][y],x,y])
        return targets
    def neighbour16(self,square):
        targets=[]
        for i in (-2,-1,0,1,2):
            for j in (-2,-1,0,1,2):
                x=square%size+i
                y=square//size+j
                if abs(i)+abs(j) in (1,2) and -1<x and x<size and y>-1 and y<size:
                    targets.append([grid[x][y],x,y])
        return targets
    
class growthtypes:
    def growthn(self,a):
        surrounded=True
        while surrounded:
            square=int(choice(a.edgesquares))
            a.edgesquares.remove(square)
            targets=[newsquare for newsquare in a.neighbour(square) if newsquare[0]!=a.no]
            if len(targets)!=0 or len(a.edgesquares)==0:
                surrounded=False
        for target in targets:
            targetno,x,y=target[0],target[1],target[2]
            targetagent=agents[targetno]
            newsquare=x+y*size
            if targetno==-1:
                grid[x][y]=a.no
                a.size+=1
                a.squares.append(newsquare)
                a.edgesquares.append(newsquare)
            elif a.combat(targetagent,newsquare):
                grid[x][y]=a.no
                try:
                    targetagent.edgesquares.remove(newsquare)
                except:
                    pass
                a.squares.append(newsquare)
                a.edgesquares.append(newsquare)
                targetagent.squares.remove(newsquare)
                a.size+=1
                targetagent.size-=1
                targetneighbour=targetagent.neighbour(newsquare)
                for newtarget in targetneighbour:
                    if newtarget[0]==targetagent.no:
                        targetagent.edgesquares.append(newtarget[1]+newtarget[2]*size)                        
    def growth1(self,a):
        target=choice(a.edgesquares)
        a.edgesquares.remove(target)
        x,y=target%size,target//size
        targetno=grid[x][y]
        targetagent=agents[targetno]
        if targetno==-1:
            grid[x][y]=a.no
            a.size+=1
            a.squares.append(target)
            neighbours=[newsquare for newsquare in a.neighbour(target) if newsquare[0]!=a.no]
            a.edgesquares+=[i[1]+i[2]*size for i in neighbours]
                
        elif a.combat(targetagent,target):
            grid[x][y]=a.no
            targetagent.edgesquares.append(target)
            a.squares.append(target)
            targetagent.squares.remove(target)
            a.size+=1
            targetagent.size-=1
            targetneighbour=[s for s in targetagent.neighbour(target) if s[0]!=targetagent.no]
            a.edgesquares+=[i[1]+i[2]*size for i in targetneighbour]
            
class combattypes:           
    def combat1(self,a,targetagent,targetsquare): #functional but random
        return target.size<a.size
    def combat2(self,a,targetagent,targetsquare): #functional but very random
        return a.size>random()*(a.size+target.size)
    def combat3(self,a,targetagent,targetsquare): #pretty
        return False
    def combat4(self,a,targetagent,targetsquare): #very random
        return random()>0.5
    def combat5(self,a,targetagent,targetsquare): #pretty
        combatants=neighbourtypes().neighbour4(targetsquare)
        return len([s for s in combatants if s[0]==a.no])>=len([s for s in combatants if s[0]==targetagent.no])
    def combat6(self,a,targetagent,targetsquare): #pretty, maybe functional
        combatants=neighbourtypes().neighbour16(targetsquare)
        adv=int(a.size>targetagent.size)
        return len([s for s in combatants if s[0]==a.no])+adv>len([s for s in combatants if s[0]==targetagent.no])
    def combat7(self,a,targetagent,targetsquare): #pretty
        x,y=targetsquare%size,targetsquare//size
        return (a.x-x)**2+(a.y-y)**2<(targetagent.x-x)**2+(targetagent.y-y)**2
class agent8(baseagent):
    def __init__(self,no):
        super().__init__(no)
        self.edgesquares=[self.x+self.y*size]
        self.n=neighbourtypes()
        self.g=growthtypes()
        self.c=combattypes()
    def neighbour(self,square):
        return self.n.neighbour8(square)
    def growth(self):
        self.g.growthn(self)
    def combat(self,targetagent,targetsquare):
        return self.c.combat7(self,targetagent,targetsquare)
class agent4(baseagent):
    def __init__(self,no):
        super().__init__(no)
        self.edgesquares=[self.x+self.y*size]
        self.n=neighbourtypes()
        self.g=growthtypes()
        self.c=combattypes()
    def neighbour(self,square):
        return self.n.neighbour4(square)
    def growth(self):
        self.g.growthn(self)
    def combat(self,targetagent,targetsquare):
        return self.c.combat6(self,targetagent,targetsquare)
class agent1(baseagent):
    def __init__(self,no):
        super().__init__(no)
        neighbours=neighbourtypes().neighbour4(self.x+self.y*size)
        self.edgesquares=[i[1]+i[2]*size for i in neighbours]
        self.n=neighbourtypes()
        self.g=growthtypes()
        self.c=combattypes()
    def neighbour(self,square):
        return self.n.neighbour4(square)
    def growth(self):
        self.g.growth1(self)
    def combat(self,targetagent,targetsquare):
        return self.c.combat6(self,targetagent,targetsquare)


n=1
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
change=n

bar=ax[1].bar(range(n),[a.size for a in agents],color=["C%d" %a.no for a in agents])
while change!=0:
    change=n
    ax[0].clear()
    ax[0].set_ylim(-1,size, auto=False)
    ax[0].set_xlim(-1,size, auto=False)
    ax[1].set_ylim(0,size**2, auto=True)
    for a in agents:
        surrounded=True
        if len(a.edgesquares)!=0:
            a.growth()
        else:
            change-=1
        if a.size==size**2:
            change=0
                    
        ax[0].scatter([i%size for i in a.squares],[j//size for j in a.squares],marker="s",s=16)
        bar[a.no].set_height(a.size)
        #ax.plot([i%size for i in a.edgesquares],[j//size for j in a.edgesquares],"sC%d" %int(a.no+5))
    
    plt.show(block=False)
    plt.pause(0.001)
print("fin")
