import random as rnd
import numpy as np
import synthetic_maps
import population
import conflict

class Horde:
    def __init__(self):
        self.tiles = []
        self.pop      = 0
        self.army    = 0
        self.food     = 0
        self.neighbours = {}

    def output(self,long=False):
        if long:
            print ('*** horde from',len(self.tiles),'tiles.  Total population =',self.pop,', army =',self.army,',',
                   'attack = ',self.attack,', ',len(self.neighbours),'raiding options:')
            for option in self.neighbours:
                print ('*** -',option.pos,': food = ',self.neighbours[option][0],', defense = ',self.neighbours[option][1],'.')
        else:
            print ('*** horde from',len(self.tiles),'tiles.  Total population =',self.pop,', army =',self.army,',',
               'attack = ',self.attack,', ',len(self.neighbours),'raiding options.')

    def sort_neighbours(self):
        return sorted(self.neighbours.items(), key = lambda x: x[1][0]/x[1][1], reverse=True)
        
class Raid:
    def __init__(self,fullmap,conflict):
        self.fullmap = fullmap
        self.conflict = conflict
        
    def raid(self,raiders):
        self.cluster_raiders(raiders)
        print ('*** raid for',len(self.hordes),'hordes.')
        for horde in self.hordes:
            self.single_raid(horde)
            if horde.food>horde.pop:
                break
            
    def single_raid(self,horde):
        print ('*** raiding horde of',len(horde.tiles),'populations.  Need to gain',(horde.pop-horde.food),'food.')
        for victim in horde.sort_neighbours():
            defense = victim[1][1]
            #d_losses = int(min(victim[0].population.total_number()/20,  attack*np.exp(-(1+attack/defense))))
            #a_losses = int(min(                                       horde.pop/10,  defense*np.exp(-(1+defense/attack))))
            #print ('*** attack ',victim[0].pos,', food = ',victim[1][0],', defense = ',victim[1][1],'defense/attack = ',defense/attack,'.')
            # print ('    losses:',a_losses,'(attack) and',d_losses,'(defense).')
           
    def cluster_raiders(self,raiding_tiles):
        print ('* start clustering raiders into hordes.')
        self.hordes = []
        for tile in raiding_tiles:
            horde = Horde()
            self.cluster_around_tile(tile,horde,raiding_tiles)
            self.hordes.append(horde)
            #horde.output()
            horde.sort_neighbours()
            
    def cluster_around_tile(self,tile,horde,raiding_tiles):
        x = tile.pos[0]
        y = tile.pos[1]
        for dx in range(-1,2):
            for dy in range(-1,2):
                if self.fullmap.check_pos([x+dx,y+dy]):
                    next_tile = self.fullmap.tiles[x+dx][y+dy]
                    if next_tile in raiding_tiles:
                        horde.tiles.append(next_tile)
                        horde.pop     += next_tile.population.total_number()
                        horde.army   += next_tile.population.army_number()
                        horde.food    += next_tile.food
                        raiding_tiles.remove(next_tile)
                        self.cluster_around_tile(next_tile,horde,raiding_tiles)
                    elif next_tile.ttype=='plains' or next_tile.ttype=='mountain':
                        horde.neighbours[next_tile] = [next_tile.food,self.conflict.defense_value(next_tile)]
        
