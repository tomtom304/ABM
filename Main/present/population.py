import random as rnd

# numbers in populations: [civilians, proportion of army]

STARTING_POPS = {
    'plains' :       [1000, 0],
    'mountain':   [50, 0],
    'alpine':        [0, 0],
    'desert':       [200, 0.2],
    'sea':           [0, 0]
}

STARTING_POPS_VARIANCE = {
    'plains' :      [.10, 0],
    'mountain':  [.10, 0],
    'alpine':       [0, 0],
    'desert':      [.10, 0],
    'sea':          [0, 0]
}

REPRODUCTION_RATES = {
    'farmers' :  0.1 ,
    'nomads':   0.12
}

STARTING_TYPE = {
    'plains' :      'farmers',
    'mountain':  'farmers',
    'alpine':       'none',
    'desert':      'nomads',
    'sea':          'none'
}

class Population:
    def __init__(self,pid,ptype,current_tile=None):
        self.pid                 = pid
        self.ptype             = ptype
        self.current_tile    = current_tile
        self.traits              = []

    def fix_initial_numbers(self,numbers,variance):
        if numbers[0] == 0:
            total = 0
        else:
            total = numbers[0]
            if variance[0] > 0:
                while True:
                    smear = rnd.gauss(1.,variance[0])
                    if smear>0:
                        break
                total = int(smear*total)
        self.army_fraction = numbers[1];
        if self.army_fraction == 0:
            army = 0
        else:
            if variance[1] > 0:
                while True:
                    smear = rnd.gauss(1.,variance[1])
                    if smear>0:
                        break
                self.army_fraction *= smear                
            army = int(self.army_fraction * total)
        self.numbers = [total, army]

    def set_reproduction_rate(self,rate):
        self.reproduction_rate = rate

    def total_number(self):
        return self.numbers[0]

    def army_number(self):
        return self.numbers[1]

    def set_total_number(self,number):
        self.numbers[0] = number
        self.numbers[1] = self.army_fraction*self.numbers[0]

    def efficiency(self):
        return 1.



        
class Population_Initialiser:
    def __init__(self,fullmap):
        print ('--------------------------------------------------------------------------------------------------------------')
        print ('Init populations on',fullmap.ntiles,'tiles.')
        print ('--------------------------------------------------------------------------------------------------------------')
        self.pid        = 0
        self.fullmap = fullmap
        self.populations  = []
        for i in range(self.fullmap.ntiles[0]):
            for j in range(self.fullmap.ntiles[1]):
                tile = self.fullmap.tiles[i][j]
                pop = self.init_tile(tile)
                if pop!=None:
                    self.pid+=1
                    self.populations.append(pop)
        print ('--------------------------------------------------------------------------------------------------------------')
        print ('Done. Initialised',len(self.populations),'populations.')
        print ('--------------------------------------------------------------------------------------------------------------')

    def init_tile(self,tile):
        pop = Population(self.pid,STARTING_TYPE[tile.ttype],tile)
        if pop.ptype=='none':
            return None
        pop.fix_initial_numbers(STARTING_POPS[tile.ttype],STARTING_POPS_VARIANCE[tile.ttype],)
        pop.set_reproduction_rate(REPRODUCTION_RATES[pop.ptype])
        tile.set_population(pop)
        #print ('   --- Init population for',tile.ttype,' --> ',pop.ptype,':',pop.numbers)
        return pop


