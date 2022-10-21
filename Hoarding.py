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
for i in range(3):
    a=agent()
    a.count=start[i]
    a.aggro=random()
    a.ally=random()
    a.destroy=random()/10
    agents.append(a)
    print(i,":",a.count,a.aggro,a.ally,a.destroy)
figure=plt.figure()
axes=plt.axes(ylim=(0,20))
bar=axes.bar(["0","1","2","Bank"],[int(agents[i].count) for i in range(3)]+[bank],align='center')
#[str(i) for i in range(3)].append("Bank"),
def update():
    global agents,bank,turn
    action=""
    for i,a in enumerate(agents):
        no=str(i)
        if a.count==0:
            pass
        elif random()<a.destroy:
            a.count-=1
            action+=no+" Destroy              "
        else:
            if random()<a.aggro or bank==0:
                target=randint(1,2)
                if agents[(i-target)%3].count==0:
                    target=3-target
                    if agents[(i-target)%3].count==0:
                        print("no targets")
                        break
                if random()<agents[(i+target)%3].ally:
                    a.count+=1
                    agents[(i-target)%3].count-=1
                    action+=no+" Steal from "+str((i-target)%3)+"         "
                    if a.count==20:
                        print(i,"wins")
                        turn=0
                        break
                else:
                    action+=no+" Failed Steal from "+str((i-target)%3)+"  "
            else:
                bank-=1
                a.count+=1
                action=action+no+" Steal from Bank      "
                if a.count==20:
                    print(i,"wins")
                    turn=0
                    break
    print([int(agents[i].count) for i in range(3)]+[bank])
    print("\n"+action+"\n")
    return agents,bank

def animate(frame):
    global agents,bank,turn
    if turn>0:
        update()
        for i in range(3):
            bar[i].set_height(agents[i].count)
        bar[3].set_height(bank)
    elif turn==0:
        print("The Bank found out")
    turn-=1

anim = animation.FuncAnimation(figure, animate,frames=1, interval=500)

plt.show()
