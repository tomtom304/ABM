from random import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
class agent:
    pass

n=5
size=20
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
while change!=0:
    ax.clear()
    for a in agents:
        surrounded=True
        while surrounded:
            if len(a.edgesquares)!=0:
                square=int(choice(a.edgesquares))
            else:
                surrounded=False
            for target in [[grid[square//size+i][square%size+j],i,j] for i in (-1,0,1) for j in (-1,0,1) if abs(i+j)==1 and square//size+i not in (-1,size) and square%size+j not in (-1,size)]:
                if target[0]==-1:
                    grid[square//size+target[1]][square%size+target[2]]=a.no
                    a.squares.append(square+target[2]+target[1]*size)
                    a.edgesquares.append(square+target[2]+target[1]*size)
                    surrounded=False
            try:
                a.edgesquares.remove(square)
            except:
                pass
        ax.plot([i%size for i in a.squares],[j//size for j in a.squares],"sC%d" %a.no)
    plt.show(block=False)
    plt.pause(0.01)
