from random import *
from time import *

pref=0.9
N=10
population = 30
print("preference (at least):",pref)
gen=0
change=1
grid = [["-" for i in range(N)] for j in range(N)]
def display(grid,gen,change):
    final=""
    for row in grid:
        for square in row:
            final+=square+" "
        final+="\n"
    final+="gen:"+str(gen)+"  changes:"+str(change)+"\n"
    print(final)
def surround(grid,x,y,group):
    count,full=-1,-1
    if grid[x][y]=="-":
        count,full=0,0
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if grid[i%N][j%N]==group:
                count+=1
            if grid[i%N][j%N]!="-":
                full+=1
    if full!=0:
        return count/full
    else:
        return 1
def move(grid,emptysquares,groupsquares,group,change):
    available=emptysquares.copy()
    for square in emptysquares:
        if surround(grid,square//N,square%N,group)<=pref:
            available.remove(square)
    for square in groupsquares:
        if surround(grid,square//N,square%N,group)<=pref:
            if available!=[]:
                newsquare=choice(available)
                available.remove(newsquare)
                emptysquares.remove(newsquare)
                emptysquares.append(square)
                grid[square//N][square%N]="-"
                grid[newsquare//N][newsquare%N]=group
                change+=1
            else:
                print(group+" full")
                break
    return grid,emptysquares,change
emptysquares = [i for i in range(N**2)]


for group in ["O","X"]:
    for i in range(population):
        square = choice(emptysquares)
        emptysquares.remove(square)
        grid[square//N][square%N] = group

display(grid,0,"")
while change!=0:
    change=0
    gen+=1
    emptysquares,noughts,crosses=[],[],[]
    for i in range(N):
        for j in range(N):
            if grid[i][j]=="-":
                emptysquares.append(i*N+j)
            elif grid[i][j]=="O":
                noughts.append(i*N+j)
            else:
                crosses.append(i*N+j)
    grid,emptysquares,change=move(grid,emptysquares,noughts,"O",change)
    grid,emptysquares,change=move(grid,emptysquares,crosses,"X",change)
    display(grid,gen,change)
    sleep(0.4)

            
