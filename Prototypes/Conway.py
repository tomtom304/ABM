from random import *
from time import *
from copy import deepcopy

N=40
population = 100
gen=0
change=1
grid = [["-" for i in range(N)] for j in range(N)]
def display(grid,gen):
    final=""
    for row in grid:
        for square in row:
            final+=square+" "
        final+="\n"
    final+="\n"+str(gen)
    print(final)
def surround(grid,x,y):
    count=0
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if grid[i%N][j%N]=="X":
                count+=1
    return count
emptysquares = [i for i in range(N**2)]

for i in range(population):
    square = choice(emptysquares)
    emptysquares.remove(square)
    grid[square//N][square%N]="X"
display(grid,0)
while change!=0:
    change=0
    gen+=1
    newgrid=deepcopy(grid)
    for i in range(N):
        for j in range(N):
            if grid[i][j]=="-" and surround(grid,i,j)== 3:
                newgrid[i][j]="X"
                change+=1
            elif grid[i][j]=="X":
                count = surround(grid,i,j)-1
                if count>3 or count<2:
                    newgrid[i][j]="-"
                    change+=1
    grid=deepcopy(newgrid)
    
    display(grid,gen)
    sleep(0.1)
    

            
