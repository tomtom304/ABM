import random as rnd
import synthetic_maps
import population

# the values are for [ general population, army ]
ATTACK = {
    'farmers' :  [0.,   5.],
    'nomads':   [1., 10.]
}

DEFENSE = {
    'farmers' :  [  1., 10.],
    'nomads':   [0.5,   5.]
}

TERRAIN = {
    'plains' :       1.,
    'mountain':  3.,
    'desert':       3.
}

class FightValues:
    def __init__(self,attack=ATTACK,defense=DEFENSE,terrain=TERRAIN):
        self.attack_factors   = attack
        self.defense_factors = defense
        self.terrain_factors  = terrain
        
    def defense_value(self,tile):
        if tile.ttype not in self.terrain_factors:
            return 0.
        pop = tile.population
        return (
            (self.defense_factors[pop.ptype][0]*pop.total_number() +
             self.defense_factors[pop.ptype][1]*pop.army_number()) *
            self.terrain_factors[tile.ttype] )

    def attack_value(self,tile,army_only=True):
        pop   = tile.population
        value = self.attack_factors[pop.ptype][1]*pop.army_number()
        if not army_only:
            value += self.attack_factors[pop.ptype][0]*pop.total_number()
        return value

class Fight:
    def __init__(self,attack=ATTACK,defense=DEFENSE,terrain=TERRAIN):
        self.fight_values = FightValues(ATTACK,DEFENSE,TERRAIN)
    
    def raid(self,defense,attack):
        pass
