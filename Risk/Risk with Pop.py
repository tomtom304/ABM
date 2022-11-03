from random import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
class agent:
    pass

n=10
size=50
fig=plt.figure()
ax = plt.axes(xlim=(0, size), ylim=(0, size))
grid = [[[-1,randint(1,10)] for i in range(size)] for j in range(size)]
agents=[]
for i in range(n):    
    a=agent()
    a.no=i
    a.aggro=random()
    a.x=randint(0,size-1)
    a.y=randint(0,size-1)
    a.squares=[a.x+a.y*size]
    a.edgesquares=[a.x+a.y*size]
    a.population=grid[a.x][a.y][1]
    grid[a.x][a.y][0]=a.no
    agents.append(a)


bar=ax.bar([a.no for a in agents],[a.population for a in agents])
change=1
def neighbour(square,a,agents):
    targets=[]
    for i in (-1,0,1):
        for j in (-1,0,1):
            x=square%size+i
            y=square//size+j
            if abs(i+j)==1 and x not in (-1,size) and y not in (-1,size):
                targets.append([grid[x][y][0],x,y])
    return targets
                
while change!=0:
    ax.clear()
    for a in agents:
        surrounded=True
        while surrounded:
            if len(a.edgesquares)!=0:
                square=int(choice(a.edgesquares))
            else:
                surrounded=False
            targets=neighbour(square,a,agents)
            for target in targets:
                target,x,y=target[0],target[1],target[2]
                if target==-1:
                    grid[x][y][0]=a.no
                    a.population+=grid[x][y][1]
                    newsquare=x+y*size
                    a.squares.append(newsquare)
                    a.edgesquares.append(newsquare)
                    surrounded=False
                elif agents[target].population<a.population:
                    target=agents[target]
                    grid[x][y][0]=a.no
                    a.population+=grid[x][y][1]
                    target.population-=grid[x][y][1]
                    newsquare=x+y*size
                    a.squares.append(x+y*size)
                    a.edgesquares.append(newsquare)
                    target.squares.remove(newsquare)
                    
                    surrounded=False
                    targetneighbour=neighbour(newsquare,a,agents)
                    for newtarget in targetneighbour:
                        if newtarget[0]==target.no:
                            target.edgesquares.append(newtarget[1]+newtarget[2]*size)
                    try:
                        target.edgesquares.remove(newsquare)
                    except:
                        pass
            
        #bar[a.no].set_height(a.population)
        ax.plot([i%size for i in a.squares],[j//size for j in a.squares],"sC%d" %a.no)
    plt.show(block=False)
    plt.pause(0.001)
