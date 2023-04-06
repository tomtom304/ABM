import pygame
import numpy as np
import random as rnd
import time
import rivers  as rivers
PLAINS      = (154, 205,  50)
DESERT     = (255, 215, 100)
MOUNTAIN = (139,  69,  19)
ALPINE        = (225,245,255)
SEA            = ( 70, 130, 180)
NOTHING   = (  0,   0,   0)

# dimensions of map in tiles
#NTILES   = (30, 20)
#TDIM      = (10, 10)
#MARGIN  = 2
# display for executable test?
DISPLAY = True
DISPTIME = 100
# type of map: 'continent' or "med"
MAPTYPE = 'continent' #"med"
# minimal proportion p_min of defining structure of the map: overall proportion is p = (p_min+ran)/3,
# where ran is a random number
MAPMACROS = {'continent': 1.5, "med": 0.3}
# number of structures and relative sizes
MAPSTRUCTS  = {'mountain':(5,0.1), 'desert':(2,0.1) }
# relative probability for a river to originate at a tile
PRIVER     = {'alpine':0.1, 'mountain': 0.02, 'plains': 0.002}
CIVNO=8
food={"plains":1000,"desert":200,"mountain":100,"alpine":0,"sea":0,"none":0}
move={"plains":2,"desert":2,"mountain":5,"sea":8,"alpine":100}


class Tile:
    def __init__(self, pos = (0,0), ttype = 'none'):
        self.pos   = pos
        self.ttype = ttype
        self.pop = 0
        self.owner=-1
        self.neighbours=[]
        self.town=False
        self.coastal=False
    def set_basics(self, pos = (0,0), ttype = 'none'):
        self.pos   = pos
        self.ttype = ttype
        self.pop = 0
        
    def set_population(self,pop):
        self.pop = pop

    def set_owner(self,owner):
        self.owner=owner

    def findneighbours(self,travel,size,world):
        shortest={}
        neighbours=[]
        for i in range(max(self.pos[0]-travel-1,0),min(self.pos[0]+travel+1,size[0])):
            for j in range(max(self.pos[1]-travel-1,0),min(self.pos[1]+travel+1,size[1])):
                shortest[(i,j)]=[size[0]*size[1],False]
        shortest[self.pos][0]=0
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
                            if world.tiles[x,y].coastal:
                                new=shortest[current][0]+1
                            else:
                                new=shortest[current][0]+move[world.tiles[x,y].ttype]
                            if new<shortest[(x,y)][0]:
                                shortest[x,y][0]=new
                shortest[current][1]=True
                if len([1 for v in shortest.values() if not v[1]])==0:
                    running=False  
        return {k:v[0] for k,v in shortest.items() if v[0]<=travel}
                    
class Map:
    def __init__(self, ntiles, maptype='continent', structs=MAPSTRUCTS):
        print ('--------------------------------------------------------------------------------------------------------------')
        print ('Init map:',maptype,'on',ntiles,'tiles.')
        print ('--------------------------------------------------------------------------------------------------------------')
        self.maptype   = maptype
        self.ntiles    = ntiles
        self.nsize     = self.ntiles[0]*self.ntiles[1]
        self.structs   = structs
        self.rivers    = []
        self.tiles=self.generate()
        self.define_macro_structure_of_map()
        for struct in self.structs:
            self.define_structures(struct)
        self.define_alpine()
        self.add_rivers()
        self.display = None
        self.time=0
        print ('--------------------------------------------------------------------------------------------------------------')
        print ('Done.')
        print ('--------------------------------------------------------------------------------------------------------------')


    def generate(self):
        tiles=np.empty( (self.ntiles[0],self.ntiles[1]), dtype=object)
        for x in range(self.ntiles[0]):
            for y in range(self.ntiles[1]):
                tiles[x,y]=Tile((x,y))
        return tiles      
    def define_macro_structure_of_map(self):
        nseeds = 1
        nfill      = int( self.nsize * (MAPMACROS[self.maptype]+rnd.random())/3)
        if self.maptype=='continent':
            ttype  = 'plains'
        elif self.maptype=="med":
            ttype  = 'sea'
        #print ('   * start filling the map.  type =',self.maptype,'.',nfill,'tiles out of',self.nsize)
        self.make_cluster(ttype,'none',nfill,[ttype])
        self.fill_inverse_of_macro()

    def fill_inverse_of_macro(self):
        nfill = 0
        for x in range (self.ntiles[0]):
            for y in range (self.ntiles[1]):
                if self.tiles[x][y].ttype=='none':
                    nfill += 1
                    if self.maptype=='continent':
                        self.tiles[x][y].ttype = 'sea'
                        for i in range(4):
                            current=self.tiles[(x-(i//2),y-(i%2))]
                            current.coastal=True
                            if current.ttype=="desert":
                                current.ttype="plains"
                            
                    elif self.maptype=="med":
                        self.tiles[x][y].ttype = 'plains'
                        self.tiles[x][y].coastal=True
        #print ('   * filled inverse',nfill,'tiles.')

    def define_structures(self,struct):
        #print ('   * init ',self.structs[struct],struct)
        if not (struct=='mountain' or struct=='desert'):
            return
        forbidden_types = ['sea', struct]
        for seed in range(self.structs[struct][0]):
            nfill = int(self.structs[struct][1]*self.nsize*rnd.random())
            #print ('   *** add',nfill,'tiles of',struct,'.')
            self.make_cluster(struct,'plains',nfill,forbidden_types)

    def make_cluster(self,struct,start_type,maxsize,forbidden_types=[]):
        growth_sites  = [ self.select_start_tile(start_type) ]
        #print ('--- start with',growth_sites,len(growth_sites),'-->',maxsize)
        for add_one_tile in range(maxsize):
            if len(growth_sites)==0:
                break
            position = rnd.choice(growth_sites)
            self.tiles[tuple(position)].ttype = struct
            self.add_tile_to_lists(growth_sites,position,forbidden_types)
            #print ('--- added',struct,'at',position," --> ",growth_sites)
            
    def check_pos(self,pos):
        #print ('----- check_pos for',self,pos)
        return pos[0]>=0 and pos[0]<self.ntiles[0] and pos[1]>=0 and pos[1]<self.ntiles[1]

    def print_tiles(self):
        pass
        #for x in range (self.ntiles[0]):
            #for y in range (self.ntiles[1]):
                #tile = self.tiles[x][y]
                #print (tile.pos, tile.ttype)


    def select_start_tile(self,accepted_types=['none']):
        if accepted_types=='none':
            start = [int(self.ntiles[0]/2),int(self.ntiles[1]/2)] 
        else:
            while True:
                start = [rnd.randint(1,self.ntiles[0]-2), rnd.randint(1,self.ntiles[1]-2)]
                if self.tiles[tuple(start)].ttype in accepted_types:
                    break
        return start

    def add_tile_to_lists(self,growth_sites,pos,forbidden_types):
        posx = pos[0]
        posy = pos[1]
        growth_sites.remove(pos)
        for delta in range(-1,2,2):
            newpos = [posx+delta, posy]
            if (self.check_pos(newpos) and newpos not in growth_sites and
                self.tiles[newpos[0]][newpos[1]].ttype not in forbidden_types): 
                growth_sites.append(newpos)
            newpos = [posx, posy+delta]
            if (self.check_pos(newpos) and newpos not in growth_sites and
                self.tiles[newpos[0]][newpos[1]].ttype not in forbidden_types):
                growth_sites.append(newpos)

    def define_alpine(self):
        for x in range (self.ntiles[0]):
            for y in range (self.ntiles[1]):
                if self.tiles[x][y].ttype == 'mountain':
                    is_alpine = True
                    for dx in range (-5,6):
                        for dy in range (-5,6):
                            if (self.check_pos([x+dx,y+dy]) and
                                not(self.tiles[x+dx][y+dy].ttype == 'mountain' or self.tiles[x+dx][y+dy].ttype == 'alpine')):
                                is_alpine = False
                    if is_alpine:
                        self.tiles[x][y].ttype = 'alpine'
                            
    def add_rivers(self):
        rid = 0
        for x in range (self.ntiles[0]):
            for y in range (self.ntiles[1]):
                if (self.check_for_river(self.tiles[x][y])):
                    self.rivers.append(self.make_river(rid,[x,y]))
                    rid += 1

    def check_for_river(self,tile):
        return (tile.ttype in PRIVER and PRIVER[tile.ttype]>rnd.random())

    def make_river(self,rid,pos):
        river = rivers.River(rid,pos,self)
        river.meander(self)
        for pos in river.links:
            for i in range(4):
                current=self.tiles[(pos[0]-(i//2),pos[1]-(i%2))]
                current.coastal=True
                if current.ttype=="desert":
                    current.ttype="plains"
        return river

    
    def init_display(self,tdim,margin):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Synthetic Map Generation')
        screen = pygame.display.set_mode( (self.ntiles[0]*tdim[0], self.ntiles[1]*tdim[1]) )
        self.display = MapDisplay(self,screen,tdim,margin)

    def draw_display(self):
        self.time+=1
        if self.display:
            self.display.draw_map(self.time)
class MapDisplay:
    def __init__(self, fullmap,screen,tdim,margin):
        self.tiles   = fullmap.tiles
        self.rivers = fullmap.rivers
        self.ntiles  = fullmap.ntiles
        self.screen = screen
        self.display = self.screen!=None
        self.tdim     = tdim
        self.margin  = margin
        self.xsize   = self.tdim[0]-2*self.margin
        self.ysize   = self.tdim[1]-2*self.margin
    def draw_map(self,time):
        self.screen.fill((0,0,0))
        timetext=pygame.font.SysFont("Times New Roman",50).render(str(time),False,(250,0,0))
        self.draw_tiles()
        self.draw_rivers()
        #self.screen.blit(timetext,(0,0))
        if self.display:
            pygame.display.flip()

        
    
    def draw_tiles(self):##########


        near=self.tiles[25][25].findneighbours(25,ntiles,world)
        
        for x in range(len(self.tiles)):
            for y in range(len(self.tiles[x])):
                distance=near.get((x,y), False)
                tile   = self.tiles[x][y]
                xpos = x*self.tdim[0] + self.margin
                ypos = y*self.tdim[1] + self.margin
                pygame.draw.rect(self.screen, self.display_colour(tile),pygame.Rect(xpos, ypos, self.xsize, self.ysize))
                if distance:
                    pygame.draw.rect(self.screen, (distance*10,0,256-distance*10),pygame.Rect(xpos, ypos, self.xsize/2, self.ysize/2))
                if x==25 and y==25:
                    pygame.draw.rect(self.screen, (0,0,0),pygame.Rect(xpos, ypos, self.xsize, self.ysize))
                    
    def draw_rivers(self):        
        for river in self.rivers:
            for i in range(len(river.links)-1):
                x0 = river.links[i][0]
                y0 = river.links[i][1]
                x1 = river.links[i+1][0]
                y1 = river.links[i+1][1]
                if x1<x0:
                    x0,x1=x1,x0
                if y1<y0:
                    y0,y1=y1,y0

                xsize = (x1-x0)*self.tdim[0]+4*self.margin
                ysize = (y1-y0)*self.tdim[1]+4*self.margin
                if x1==x0:
                    xsize = 4*self.margin
                if y1==y0:
                    ysize = 4*self.margin
                if self.display:
                    pygame.draw.rect(self.screen,SEA,pygame.Rect(x0*self.tdim[0]-2*self.margin, y0*self.tdim[1]-2*self.margin, xsize, ysize))
                    if  x1==self.ntiles[0]-1:
                        pygame.draw.rect(self.screen,SEA,pygame.Rect( x1*self.tdim[0]-2*self.margin, y0*self.tdim[1]-2*self.margin, xsize, ysize))
                    if  y1==self.ntiles[1]-1:
                        pygame.draw.rect(self.screen,SEA,pygame.Rect( x0*self.tdim[0]-2*self.margin, y1*self.tdim[1]-2*self.margin, xsize, ysize))
                #print ("drawing [",x0,y0,"] -> [",x1,y1,"]")

    def display_colour(self,tile):
        if (tile.ttype=='plains'):
            return PLAINS
        elif (tile.ttype=='desert'):
            return DESERT
        elif (tile.ttype=='mountain'):
            return MOUNTAIN
        elif (tile.ttype=='alpine'):
            return ALPINE
        elif (tile.ttype=='sea'):
            return SEA
        return NOTHING

if __name__ == '__main__' :
    #print ("Testing map generation")
    ntiles=(50,50)
    tilesize      = (25, 25)
    margin  = 2
    maptype = "continent"
    world = Map(ntiles,maptype)
    world.init_display(tilesize,margin)
    world.draw_display()

