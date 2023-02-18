from matplotlib import animation
from matplotlib import pyplot as plt
from random import *
boid_count=30
size=5000
limits=[size,size]

pos=[[random()*(size-1000)+500 for i in range(2)] for j in range(boid_count)]
vel=[[random()*20-10 for i in range(2)] for j in range(boid_count)]


figure = plt.figure()
axes = plt.axes(xlim=(0, limits[0]), ylim=(0, limits[1]))
scatter = axes.scatter(pos[0], pos[1],marker='o', edgecolor='k', lw=0.5)


def update(pos,vel):
    visualdist=300
    midstrength=0.0008
    alertdist=100
    alertstrength=0.05
    formstrength=0.03
    minspeed=2
    maxspeed=40
    sep=[]
    for i in range(boid_count):
        seprow=[]
        for j in range(boid_count):
            seprow.append(((pos[i][0]-pos[j][0])**2+(pos[i][1]-pos[j][1])**2)**0.5)
        sep.append(seprow)
    
    for i in range(boid_count):
        if any(x!=0 and x<visualdist for x in sep[i]):
            mid=[0,0]
            groupvel=[0,0]
            count=0
            for j in range(boid_count):
                if sep[i][j]<visualdist and sep[i][j]!=0:
                    count+=1
                    mid=[mid[n]+pos[j][n] for n in range(2)]
                    groupvel=[groupvel[n]+vel[j][n] for n in range(2)]
            mid=[mid[n]/count for n in range(2)]
            groupvel=[groupvel[n]/count for n in range(2)]
            direction=[pos[i][n]-mid[n] for n in range(2)]
            for n in range(2):
                vel[i][n]-=direction[n]*midstrength
                vel[i][n]+=groupvel[n]*formstrength

        if any(x!=0 and x<alertdist for x in sep[i]):
            mid=[0,0]
            count=0
            for j in range(boid_count):
                if sep[i][j]<alertdist and sep[i][j]!=0:
                    count+=1
                    mid=[mid[n]+pos[j][n] for n in range(2)]
            mid=[mid[n]/count for n in range(2)]
            direction=[pos[i][n]-mid[n] for n in range(2)]
            for n in range(2):
                vel[i][n]+=direction[n]*alertstrength
        for n in range(2):
            if pos[i][n]+vel[i][n]>size-500:
                vel[i][n]-=2
            if pos[i][n]+vel[i][n]<500:
                vel[i][n]+=2
            speed=(vel[i][0]**2+vel[i][1]**2)**0.5
            #if speed<minspeed:
                #vel[i]=[vel[i][n]/speed*minspeed for n in range(2)]
            if speed>maxspeed:
                vel[i]=[vel[i][n]/speed*maxspeed for n in range(2)]
    
            pos[i][n]=(pos[i][n]+vel[i][n])
    return pos,vel

def animate(frame):
    update(pos,vel)
    scatter.set_offsets(pos)


anim = animation.FuncAnimation(figure, animate,frames=60, interval=1)



writergif = animation.PillowWriter(fps=30) 
anim.save('boids.gif', writer=writergif)
plt.close()
