import pygame
import time

import synthetic_maps as smaps 
import population as pop
import time_evolution as stepper

# dimensions of map in tiles
NTILES   = (50, 50)
TDIM      = (30, 30)
MARGIN  = 2
# display for executable test?
DISPLAY = False
# type of map: 'continent' or 'mediterranean'
MAPTYPE = 'mediterranean'
# number of timesteps
STEPS = 2

class DryRun:
    def __init__(self,maptype,ntiles):
        self.smap          = self.init_map()
        self.populations = self.init_pops()
        print ('============================================')
        print ("Initial conditions: map and starting populations fixed.")
        print ('============================================')
    
    def init_map(self):
        return smaps.Map(MAPTYPE)
            
    def init_pops(self):
        pi = pop.Population_Initialiser(self.smap)
        return pi.populations

    def init_display(self,tdim,margin):
        self.smap.init_display(tdim,margin)

    def draw(self):
        self.smap.draw_display()
        
    def total_evolution(self,steps):
        self.evolution = stepper.TimeEvolution(self.smap,self.populations)
        for step in range(steps):
            print ('============================================')
            print ('Timestep:',step,'.')
            print ('============================================')
            self.evolution.step()

if __name__ == '__main__' :
    print ('============================================')
    print ("Testing dryrun")
    print ('============================================')
    dryrun = DryRun(MAPTYPE,NTILES)
    if DISPLAY:
        dryrun.init_display(TDIM,MARGIN)
        dryrun.draw()
    dryrun.total_evolution(STEPS)
