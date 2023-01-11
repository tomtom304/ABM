import pygame
import numpy as np
import random as rnd
import time
import mapdisplay as display
import rivers  as rivers

# dimensions of map in tiles
NTILES   = (50, 50)
TDIM      = (10, 10)
MARGIN  = 2
# display for executable test?
DISPLAY = True
DISPTIME = 100
# type of map: 'continent' or 'mediterranean'
MAPTYPE = 'continent' #'mediterranean'
# minimal proportion p_min of defining structure of the map: overall proportion is p = (p_min+ran)/3,
# where ran is a random number
MAPMACROS = {'continent': 1.5, 'mediterranean': 0.3}
# number of structures and relative sizes
MAPSTRUCTS  = {'mountain':(5,0.1), 'desert':(2,0.1) }
# relative probability for a river to originate at a tile
PRIVER     = {'alpine':0.1, 'mountain': 0.02, 'plains': 0.002}

class Tile:
    def __init__(self, pos = (0,0), ttype = 'none'):
        self.pos   = pos
        self.ttype = ttype
        self.population = None
        self.food   = 0 

    def set_basics(self, pos = (0,0), ttype = 'none'):
        self.pos   = pos
        self.ttype = ttype
        self.population = None
        self.food = 0
        
    def set_population(self,pop):
        self.population = pop
        
    def set_food(self,food):
        self.food = food
        
class Map:
    def __init__(self, maptype='continent', ntiles=NTILES, structs=MAPSTRUCTS):
        print ('--------------------------------------------------------------------------------------------------------------')
        print ('Init map:',maptype,'on',ntiles,'tiles.')
        print ('--------------------------------------------------------------------------------------------------------------')
        self.maptype   = maptype
        self.ntiles    = ntiles
        self.nsize     = self.ntiles[0]*self.ntiles[1]
        self.structs   = structs
        self.init_tiles_and_rivers()
        self.define_macro_structure_of_map()
        for struct in self.structs:
            self.define_structures(struct)
        self.define_alpine()
        self.add_rivers()
        self.display = None
        print ('--------------------------------------------------------------------------------------------------------------')
        print ('Done.')
        print ('--------------------------------------------------------------------------------------------------------------')
        
    def init_tiles_and_rivers(self):
        self.tiles      = []
        for i in range(self.ntiles[0]):
            ytiles = []
            for j in range(self.ntiles[1]):
                ytiles.append(Tile((i,j)))
            self.tiles.append(ytiles)
        self.rivers    = []

            
    def define_macro_structure_of_map(self):
        nseeds = 1
        nfill      = int( self.nsize * (MAPMACROS[self.maptype]+rnd.random())/3)
        if self.maptype=='continent':
            ttype  = 'plains'
        elif self.maptype=='mediterranean':
            ttype  = 'sea'
        print ('   * start filling the map.  type =',self.maptype,'.',nfill,'tiles out of',self.nsize)
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
                    elif self.maptype=='mediterranean':
                        self.tiles[x][y].ttype = 'plains'
        print ('   * filled inverse',nfill,'tiles.')

    def define_structures(self,struct):
        print ('   * init ',self.structs[struct],struct)
        if not (struct=='mountain' or struct=='desert'):
            return
        forbidden_types = ['sea', struct]
        for seed in range(self.structs[struct][0]):
            nfill = int(self.structs[struct][1]*self.nsize*rnd.random())
            print ('   *** add',nfill,'tiles of',struct,'.')
            self.make_cluster(struct,'plains',nfill,forbidden_types)

    def make_cluster(self,struct,start_type,maxsize,forbidden_types=[]):
        growth_sites  = [ self.select_start_tile(start_type) ]
        #print ('--- start with',growth_sites,len(growth_sites),'-->',maxsize)
        for add_one_tile in range(maxsize):
            if len(growth_sites)==0:
                break
            position = rnd.choice(growth_sites)
            self.tiles[position[0]][position[1]].ttype = struct
            self.add_tile_to_lists(growth_sites,position,forbidden_types)
            #print ('--- added',struct,'at',position," --> ",growth_sites)
            
    def check_pos(self,pos):
        #print ('----- check_pos for',self,pos)
        return pos[0]>=0 and pos[0]<self.ntiles[0] and pos[1]>=0 and pos[1]<self.ntiles[1]

    def print_tiles(self):
        for x in range (self.ntiles[0]):
            for y in range (self.ntiles[1]):
                tile = self.tiles[x][y]
                print (tile.pos, tile.ttype)


    def select_start_tile(self,accepted_types=['none']):
        if accepted_types=='none':
            start = [int(self.ntiles[0]/2),int(self.ntiles[1]/2)] 
        else:
            while True:
                start = [rnd.randint(1,self.ntiles[0]-2), rnd.randint(1,self.ntiles[1]-2)]
                if self.tiles[start[0]][start[1]].ttype in accepted_types:
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
                    for dx in range (-2,3):
                        for dy in range (-2,3):
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
        return river

    def init_display(self,tdim,margin):
        pygame.init()
        pygame.display.set_caption('Synthetic Map Generation')
        screen = pygame.display.set_mode( (self.ntiles[0]*tdim[0], self.ntiles[1]*tdim[1]) )
        self.display = display.MapDisplay(self,screen,tdim,margin)

    def draw_display(self):
        if self.display:
            self.display.draw_map()
            time.sleep(DISPTIME)

if __name__ == '__main__' :
    print ("Testing map generation")
    synth_map = Map(MAPTYPE)
    if DISPLAY:
        synth_map.init_display(TDIM,MARGIN)
        synth_map.draw_display()
    
