from random import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
class agent:
    pass

n=10
size=50
fig=plt.figure()
ax = plt.axes(xlim=(0, size), ylim=(0, size))
grid = [[-1 for i in range(size)] for j in range(size)]
agents=[]
for i in range(n):    
    a=agent()
    a.no=i
    a.aggro=random()
    a.x=randint(0,size-1)
    a.y=randint(0,size-1)
    a.squares=[a.x+a.y*size]
    a.edgesquares=[a.x+a.y*size]
    a.size=1
    grid[a.x][a.y]=a.no
    agents.append(a)
scatter=ax.scatter
change=1
def neighbour4(square,a):
    targets=[]
    for i in (-1,0,1):
        for j in (-1,0,1):
            x=square%size+i
            y=square//size+j
            if abs(i+j)==1 and x not in (-1,-2,size) and y not in (-1,-2,size):
                targets.append([grid[x][y],x,y])
    return targets
def neighbour9(square,a):
    targets=[]
    for i in (-1,0,1):
        for j in (-1,0,1):
            x=square%size+i
            y=square//size+j
            if abs(i)+abs(j)!=0 and x not in (-1,-2,size) and y not in (-1,-2,size):
                targets.append([grid[x][y],x,y])
    return targets

def neighbour4f(square,a):
    targets=[]
    for i in (-1,0,1):
        for j in (-1,0,1):
            x=square%size+i
            y=square//size+j
            if abs(i+j)==1 and x not in (-1,-2,size) and y not in (-1,-2,size) and grid[x][y]!=a.no:
                targets.append([grid[x][y],x,y])
    return targets

def combat1(a,target,x,y):
    if target.size<a.size:
        return True
    else:
        return False
def combat2(a,target,x,y):
    if a.size>random()*(a.size+target.size):
        return True
    else:
        return False
def combat3(a,target,x,y):
    return False
while change!=0:
    ax.clear()
    for a in agents:
        surrounded=True
        while surrounded:
            if len(a.edgesquares)!=0:
                square=int(choice(a.edgesquares))
                a.edgesquares.remove(square)
                targets=neighbour4f(square,a)
                if len(targets)!=0:
                    surrounded=False
            else:
                surrounded=False
        for target in targets:
            targetno,x,y=target[0],target[1],target[2]
            targetag=agents[targetno]
            if targetno==-1:
                grid[x][y]=a.no
                a.size+=1
                newsquare=x+y*size
                a.squares.append(newsquare)
                a.edgesquares.append(newsquare)
            elif combat2(a,targetag,x,y):
                grid[x][y]=a.no
                newsquare=x+y*size
                a.squares.append(x+y*size)
                a.edgesquares.append(newsquare)
                targetag.squares.remove(newsquare)
                a.size+=1
                targetneighbour=neighbour4(newsquare,a)
                for newtarget in targetneighbour:
                    if newtarget[0]==targetag.no:
                        targetag.edgesquares.append(newtarget[1]+newtarget[2]*size)
                try:
                    targetag.edgesquares.remove(newsquare)
                except:
                    pass
                
            

        ax.plot([i%size for i in a.squares],[j//size for j in a.squares],"sC%d" %a.no)
        #ax.plot([i%size for i in a.edgesquares],[j//size for j in a.edgesquares],"sC%d" %int(a.no+5))
    plt.show(block=False)
    plt.pause(0.01)
