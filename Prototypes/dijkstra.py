import numpy as np
pos=(1,1)
travel=30
size=[20,8]
distances=np.array([[i+j for i in range(size[1])] for j in range(size[0])])
print(len(distances),len(distances[0]))
shortest={}
neighbours=[]
for i in range(max(pos[0]-travel,0),min(pos[0]+travel,size[0])):
    for j in range(max(pos[1]-travel,0),min(pos[1]+travel,size[1])):
        shortest[(i,j)]=[size[0]*size[1],False]
shortest[pos][0]=0
running=True
while running:
    shortestdist=min([v[0] for v in shortest.values() if not v[1]])
    current=[k for k,v in shortest.items() if v[0]==shortestdist and not v[1]][0]
    if shortest[current][0]>=travel:
        running=False
    else:
        for i in (-1,0,1):
            for j in (-1,0,1):
                if abs(i+j)==1 and -1<current[0]+i and current[0]+i<size[0] and current[1]+j>-1 and current[1]+j<size[1]:
                    x,y=current[0]+i,current[1]+j
                    new=shortest[current][0]+distances[x,y]
                    if new<shortest[(x,y)][0]:
                        shortest[x,y][0]=new
        shortest[current][1]=True
        if len([1 for v in shortest.values() if not v[1]])==0:
            running=False


print({k:v[0] for k,v in shortest.items() if v[0]<=travel})            
output=""
for i in range(max(pos[0]-travel,0),min(pos[0]+travel,size[0])):
    for j in range(max(pos[1]-travel,0),min(pos[1]+travel,size[1])):
        output+=str(shortest[(i,j)][0])+"   "
    output+="\n"
print(output)



