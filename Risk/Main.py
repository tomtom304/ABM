from random import *
import matplotlib.pyplot as plt
import numpy as np
class combattypes:           
    def combat1(self,a,targetagent,targetsquare): #functional but random
        return targetagent.size<a.size
    def combat2(self,a,targetagent,targetsquare): #functional but very random
        return a.size>random()*(a.size+targetagent.size)
    def combat3(self,a,targetagent,targetsquare): #pretty
        return False
    def combat4(self,a,targetagent,targetsquare): #very random
        return random()>0.5
    def combat5(self,a,targetagent,targetsquare): #pretty
        combatants=a.neighbour(targetsquare)
        return len([s for s in combatants if s[0]==a.no])>len([s for s in combatants if s[0]==targetagent.no])
    def combat6(self,a,targetagent,targetsquare): #pretty, maybe functional
        combatants=a.neighbour(targetsquare)
        adv=int(a.size>targetagent.size)
        return len([s for s in combatants if s[0]==a.no])+adv>len([s for s in combatants if s[0]==targetagent.no])
    #def combat7(self,a,targetagent,targetsquare):
        


class agent():
    def __init__(self,no):
        self.c=combattypes()
        self.no=no
        self.aggro=random()
        self.x=randint(0,xsize-1)
        self.y=randint(0,ysize-1)
        while grid[self.x][self.y]["owner"]!=-1 or grid[self.x][self.y]["terrain"]==1:
            self.x=randint(0,xsize-1)
            self.y=randint(0,ysize-1)
        self.squares=[self.x+self.y*xsize]
        self.size=1
        grid[self.x][self.y]["owner"]=self.no
        grid[self.x][self.y]["pop"]=1
        self.c=combattypes()
        self.edgesquares=[self.x+self.y*xsize]
    def combat(self,targetagent,targetsquare,terrain):
        return self.c.combat2(self,targetagent,targetsquare)
    def gainsquare(self,x,y,square):
        grid[x][y]["owner"]=self.no
        grid[x][y]["pop"]=1
        self.size+=1
        self.squares.append(square)
        self.edgesquares.append(square)
    def losesquare(self,a,x,y,square):
        self.edgesquares.remove(square)
        self.squares.remove(square)
        self.size-=1
        for i in a.neighbour(square):
            if i[0] not in (a.no,-1):
                if i[1]+i[2]*xsize not in agents[i[0]].edgesquares:
                    agents[i[0]].edgesquares.append(i[1]+i[2]*xsize)
    def neighbour(self,square):
        targets=[]
        for i in (-1,0,1):
            for j in (-1,0,1):
                x=square%xsize+i
                y=square//xsize+j
                if abs(i+j)==1 and -1<x and x<xsize and y>-1 and y<ysize and grid[x][y]["terrain"]!=1:
                    targets.append([grid[x][y]["owner"],x,y,grid[x][y]["terrain"]])
        return targets
    def growth(self):
        new=0
        surrounded=True
        while surrounded:
            square=int(choice(self.edgesquares))
            targets=[newsquare for newsquare in self.neighbour(square) if newsquare[0]!=self.no]
            if len(targets)!=0:
                surrounded=False
            else:
                self.edgesquares.remove(square)
                if len(self.edgesquares)==0:
                    surrounded=False
        for target in targets:
            targetno,x,y,terrain=target[0],target[1],target[2],target[3]
            targetagent=agents[targetno]
            newsquare=x+y*xsize
            if terrain!=1:
                if targetno==-1:
                    self.gainsquare(x,y,newsquare)
                    new+=1
                elif self.combat(targetagent,newsquare,terrain):
                    self.gainsquare(x,y,newsquare)
                    targetagent.losesquare(self,x,y,newsquare)
                    new+=1
        return new==0
    
n=10
xsize=80
ysize=50
fig,ax=plt.subplots(2)
ax[0].set_ylim(0,ysize, auto=False)
ax[0].set_xlim(0,xsize, auto=False)
fig.set_size_inches(5.25, 6.75)
fig.set_tight_layout(True)
fig.set_dpi(125)
grid = np.array([[{"owner":-1,"terrain":0,"pop":0} for i in range(ysize)] for j in range(xsize)])
border=[]
for i in range(ysize-1):
    border.append([25,i])
    border.append([55,i+1])
for i in range(27):
    border.append([i+27,25])
for i in border:
    grid[i[0]][i[1]]["terrain"]=1
blocked=len(border)
ax[0].scatter([i[0] for i in border],[i[1] for i in border],color="black",marker="s",s=16)
agents=[]
for i in range(n):    
    a=agent(i)
    agents.append(a)
    ax[0].scatter([i%xsize for i in a.squares],[j//xsize for j in a.squares],marker="s",s=16)
change=n
end=0
bar=ax[1].bar(range(n),[a.size for a in agents],color=["C%d" %a.no for a in agents])
ax[1].set_ylim(0,xsize*ysize, auto=True)
while end<5:
    change=n
    ax[0].clear()
    ax[0].set_ylim(-1,ysize, auto=False)
    ax[0].set_xlim(-1,xsize, auto=False)
    
    for a in agents:
        if len(a.edgesquares)!=0:
            if a.growth():
                change-=1
        else:
            change-=1
        ax[0].scatter([i[0] for i in border],[i[1] for i in border],color="black",marker="s",s=16)            
        ax[0].scatter([i%xsize for i in a.squares],[j//xsize for j in a.squares],marker="s",s=16)
        bar[a.no].set_height(a.size)
        #ax[0].scatter([i%xsize for i in a.edgesquares],[j//xsize for j in a.edgesquares],marker="s",s=16, color="C%d" %int(a.no+5))
    if change==0:
        end+=1
    else:
        end=0
    plt.show(block=False)
    plt.pause(0.001)
print("fin")
