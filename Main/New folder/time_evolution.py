import random as rnd
import synthetic_maps
import population
import harvest as hv
import raid as raid
import conflict as cf

CONFLICT_THRES = 0.1

class TimeEvolution:
    def __init__(self,fullmap,populations,cthres=CONFLICT_THRES):
        self.fullmap          = fullmap
        self.populations    = populations
        self.conflict_thres = cthres
        self.harvest          = hv.Harvest(fullmap)
        self.conflict           = cf.FightValues()
        self.all_raids         = raid.Raid(self.fullmap,self.conflict)
        self.raiding_tiles   = []
        print ('Initialised time evolution')

    def step(self):
        self.harvest.harvest()
        self.check_for_sufficient_produce()
        self.all_raids.raid(self.raiding_tiles)
        
    def check_for_sufficient_produce(self):
        for pop in self.populations:
            tile   = pop.current_tile
            food = tile.food = self.harvest.resources[tile]
            if food < pop.total_number():
                self.raiding_tiles.append(tile)
