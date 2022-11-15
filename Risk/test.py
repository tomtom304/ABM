
from random import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class agent:
    def __init__(self,no):
        self.no=no
        self.size=randint(0,100)
agents=[]
n=5
for i in range(n):    
    a=agent(i)
    agents.append(a)
fig,ax=plt.subplots(2)




ax[1].bar(range(n),[a.size for a in agents])
print("Done")
