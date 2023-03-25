import random as rnd
import synthetic_maps

PRODUCE = {
    'plains'      : 2000,
    'mountain' : 200,
    'desert'      : 250
}

PRODUCTION_VARIANCE = 0.1

class Harvest:
    def __init__(self,fullmap,production=PRODUCE,variance=PRODUCTION_VARIANCE):
        self.produce    = production
        self.variance   = variance
        self.multiplier  = -1
        self.init_resources(fullmap)

    def init_resources(self,fullmap):
        self.resources = {}
        for x in range(fullmap.ntiles[0]):
            for y in range(fullmap.ntiles[1]):
                tile = fullmap.tiles[x][y]
                if tile.ttype in self.produce:
                    self.resources[tile] = 0
        
    def harvest(self):
        self.set_overall_production_multiplier()
        for tile in self.resources:
            self.resources[tile] = round(self.produce[tile.ttype] * self.multiplier * tile.population.efficiency())
            tile.set_food = self.resources[tile]
        print ('* harvested with multiplier =',self.multiplier)
            
    def set_overall_production_multiplier(self):
        self.multiplier  = -1
        while self.multiplier<0.:
            self.multiplier = rnd.gauss(1., self.variance)

