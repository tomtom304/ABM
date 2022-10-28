from random import *
import matplotlib.pyplot as plt
from matplotlib import animation

class agent:
    pass

agents=[]
start=[10,8,6]
shuffle(start)
bank=15
turn=30
winner=-1
for i in range(3):
    a=agent()
    a.count=start[i]
    a.aggro=random()
    a.ally=random()
    a.destroy=random()/10
    agents.append(a)
    #print(i,":",a.count,a.aggro,a.ally,a.destroy)
figure=plt.figure()
axes=plt.axes(ylim=(0,20))
bar=axes.bar(["0","1","2","Bank"],[int(agents[i].count) for i in range(3)]+[bank],align='center')
def reset():
    global agents,winner
    print("reset")
    for i,a in enumerate(agents):
        if i!=winner:
            a.aggro=random()
            a.ally=random()
            a.destroy=random()/10
    return
def update():
    global agents,bank,turn,winner
    for i,a in enumerate(agents):
        if a.count==0:
            pass
        elif random()<a.destroy:
            a.count-=1
        else:
            if random()<a.aggro or bank==0:
                target=randint(1,2)
                if agents[(i-target)%3].count==0:
                    target=3-target
                    if agents[(i-target)%3].count==0:
                        break
                if random()<agents[(i+target)%3].ally:
                    a.count+=1
                    agents[(i-target)%3].count-=1
                    if a.count==20:
                        turn=0
                        print(i,"wins")
                        print(i,":",a.count,a.aggro,a.ally,a.destroy)
                        winner=i
                        break
            else:
                bank-=1
                a.count+=1
                if a.count==20:
                    print(i,"wins")
                    print(i,":",a.count,a.aggro,a.ally,a.destroy)
                    winner=i
                    turn=0
                    break
    return 

def animate(frame):
    global agents,bank,turn,winner
    if turn>0:
        update()
        for i in range(3):
            bar[i].set_height(agents[i].count)
        bar[3].set_height(bank)
    elif turn<1:
        print("New Round")
        agents=reset()
        turn=30
    turn-=1

anim = animation.FuncAnimation(figure, animate,frames=120, interval=1)

plt.show()
