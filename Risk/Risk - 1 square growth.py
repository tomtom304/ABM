from random import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
class agent:
    pass

n=4
size=50
fig=plt.figure()
ax = plt.axes(xlim=(0, size), ylim=(0, size))
grid = [[-1 for i in range(size)] for j in range(size)]

def neighbour4(square):
    targets=[]
    for i in (-1,0,1):
        for j in (-1,0,1):
            x=square%size+i
            y=square//size+j
            if abs(i+j)==1 and x not in (-1,-2,size) and y not in (-1,-2,size):
                targets.append([grid[x][y],x,y])
    return targets
def neighbour9(square):
    targets=[]
    for i in (-1,0,1):
        for j in (-1,0,1):
            x=square%size+i
            y=square//size+j
            if abs(i)+abs(j)!=0 and x not in (-1,size) and y not in (-1,size):
                targets.append([grid[x][y],x,y])
    return targets

def neighbour4f(square,a):
    targets=[]
    for i in (-1,0,1):
        for j in (-1,0,1):
            x=square%size+i
            y=square//size+j
            if abs(i+j)==1 and x not in (-1,size) and y not in (-1,size) and grid[x][y]!=a.no:
                targets.append([grid[x][y],x,y])
    return targets

def combat1(a,target,x,y):
    return target.size<a.size
def combat2(a,target,x,y):
    return a.size>random()*(a.size+target.size)
def combat3(a,target,x,y):
    return False

agents=[]
for i in range(n):    
    a=agent()
    a.no=i
    a.aggro=random()
    a.x=randint(0,size-1)
    a.y=randint(0,size-1)
    a.squares=[a.x+a.y*size]
    
    neighbours=neighbour4(a.x+a.y*size)
    a.edgesquares=[i[1]+i[2]*size for i in neighbours]
    a.size=1
    grid[a.x][a.y]=a.no
    agents.append(a)
scatter=ax.scatter
change=1

while change!=0:
    ax.clear()
    for a in agents:
        if len(a.edgesquares)!=0:
            target=choice(a.edgesquares)
            a.edgesquares.remove(target)
            x,y=target%size,target//size
            targetno=grid[x][y]
            if targetno==-1:
                grid[x][y]=a.no
                a.size+=1
                a.squares.append(target)
                neighbours=neighbour4f(target,a)
                a.edgesquares+=[i[1]+i[2]*size for i in neighbours]
                    
            elif combat1(a,agents[targetno],x,y):
                grid[x][y]=a.no
                agents[targetno].edgesquares.append(target)
                a.squares.append(target)
                agents[targetno].squares.remove(target)
                a.size+=1
                agents[targetno].size-=1
                targetneighbour=neighbour4f(target,a)
                a.edgesquares+=[i[1]+i[2]*size for i in targetneighbour]
                
                    
        

        ax.plot([i%size for i in a.squares],[j//size for j in a.squares],"sC%d" %a.no)
        ax.plot([i%size for i in a.edgesquares],[j//size for j in a.edgesquares],"xC%d" %int(a.no+5))
    plt.show(block=False)
    plt.pause(0.005)
