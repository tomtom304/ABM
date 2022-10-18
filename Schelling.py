from random import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
class agent:
    pass
fig, ax = plt.subplots()
n=1000
r=0.05
th=0.5
agents=[]
change=100
for i in range(n):    
    a=agent()
    a.type=randint(0,1)
    a.x=random()
    a.y=random()
    agents.append(a)
red=[a for a in agents if a.type==0]
blue=[a for a in agents if a.type==1]
plt.plot([a.x for a in red],[a.y for a in red],"ro")
plt.plot([a.x for a in blue],[a.y for a in blue],"bo")
plt.show(block=False)
plt.pause(0.1)
change=1000
while change!=0:
    change=1000
    for a in agents:
        neighbours=[nb for nb in agents if (a.x-nb.x)**2+(a.y-nb.y)**2<r**2 and nb!=a]
        if len(neighbours)>0:
            q=len([nb for nb in neighbours if nb.type==a.type])/len(neighbours)
            if q<th:
                a.x,a.y=random(),random()
                ax.clear()
                
                red=[a for a in agents if a.type==0]
                blue=[a for a in agents if a.type==1]
                plt.plot([a.x for a in red],[a.y for a in red],"ro")
                plt.plot([a.x for a in blue],[a.y for a in blue],"bo")

                plt.show(block=False)
                plt.pause(0.01)
            else:
                change-=1
    
