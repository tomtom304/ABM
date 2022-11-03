from random import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
class agent:
    pass

n=5
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
    grid[a.x][a.y]=a.no
    agents.append(a)
scatter=ax.scatter
for a in agents:
    ax.plot([i%size for i in a.squares],[j//size for j in a.squares],"sC%d" %a.no)
plt.show(block=False)
plt.pause(0.1)
change=1
def neighbour(square,a,agents):
    targets=[]
    for i in (-1,0,1):
        for j in (-1,0,1):
            x=square%size+i
            y=square//size+j
            if abs(i+j)==1 and x not in (-1,size) and y not in (-1,size):
                targets.append([grid[x][y],x,y])
    return targets



while change!=0:
    ax.clear()
    for a in agents:
        surrounded=True
        while surrounded:
            if len(a.edgesquares)!=0:
                square=int(choice(a.edgesquares))
                a.edgesquares.remove(square)
            else:
                surrounded=False
            targets=neighbour(square,a,agents)
            for target in targets:
                target,x,y=target[0],target[1],target[2]
                if target==-1:
                    grid[x][y]=a.no
                    newsquare=x+y*size
                    a.squares.append(newsquare)
                    a.edgesquares.append(newsquare)
                    surrounded=False
        ax.plot([i%size for i in a.squares],[j//size for j in a.squares],"sC%d" %a.no)
    plt.show(block=False)
    plt.pause(0.1)
