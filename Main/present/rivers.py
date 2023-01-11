import random as rnd

# we assume that for rivers all tile coordinates denote the upper left corner

class River:
    def __init__(self, rid,pos, fullmap):
        self.rid          = rid
        self.startpos = self.pick_corner_of_tile(pos,fullmap)
        self.links        = []
        self.direction = self.define_direction_of_river(fullmap)
        self.Px           = abs(self.direction[0]) / (abs(self.direction[0])+abs(self.direction[1]))
        self.Py           = 1.-self.Px
        self.stepx      = 1
        self.stepy      = 1
        if self.direction[0]<0.:
            self.stepx = -1
        if self.direction[1]<0.:
            self.stepy = -1
        print ('   *** start river at',fullmap.tiles[pos[0]][pos[1]].ttype,pos," --> ",self.startpos," --> ",self.direction,
               "with",(len(self.links)-1),"links.")

    def pick_corner_of_tile(self,pos,fullmap):
        # when picking a tile, wemust one of the four corners - this happens at random
        while True:
            newpos = [pos[0], pos[1]]
            for i in range(2):
                if rnd.random()>0.5:
                    newpos[i] = newpos[i]+1
            if fullmap.check_pos(newpos):
                return newpos                
        
    def define_direction_of_river(self,fullmap):
        # basic idea is to define three (or four, for mediterranean maps) default directions :
        # - one to the nearest corner
        # - one parallel to the x or y axis (shortest distance to the border of the map), plus some random wiggle
        #   around a y or z direction
        # for mediterranean maps we also add a direction to the centre of the map, where the sea usually is
        # out of these we pick one with a probablity proportional to the inverse distance to its destination
        directions = {}
        total_length = 0
        if fullmap.maptype=='mediterranean':
            distvec     = [(self.startpos[0]-int(fullmap.ntiles[0]/2)) ,(self.startpos[1]-int(fullmap.ntiles[1]/2))]
            distlength =(distvec[0]**2+distvec[1]**2)**(1./2.)
            nvec         = [distvec[0]/distlength,  distvec[1]/distlength]
            directions[1./distlength] = nvec
            total_length += 1./distlength
            #print ('   --- possible river from',self.startpos,'towards',nvec,'distance = ',distlength)
        to_border = [self.startpos[0], self.startpos[1]]
        for i in range(2):
            if self.startpos[i]<fullmap.ntiles[i]/2:
                to_border[i] = -fullmap.ntiles[i]  + self.startpos[i]
        distvec = [-to_border[0], -to_border[1]]
        distlength =(distvec[0]**2+distvec[1]**2)**(1./2.)
        nvec         = [distvec[0]/distlength,  distvec[1]/distlength]
        total_length += 1./distlength
        directions[1./distlength]   = nvec
        #print ('   --- possible river from',self.startpos,'towards',nvec,'distance = ',distlength)
        distvec = [-to_border[0], -rnd.random()*to_border[1]]   
        distlength =(distvec[0]**2+distvec[1]**2)**(1./2.)
        nvec         = [distvec[0]/distlength,  distvec[1]/distlength]
        total_length += 1./distlength
        directions[1./distlength]   = nvec
        #print ('   --- possible river from',self.startpos,'towards',nvec,'distance = ',distlength)
        distvec = [--rnd.random()*to_border[0], to_border[1]]   
        distlength =(distvec[0]**2+distvec[1]**2)**(1./2.)
        nvec         = [distvec[0]/distlength,  distvec[1]/distlength]
        total_length += 1./distlength
        directions[1./distlength]   = nvec
        #print ('   --- possible river from',self.startpos,'towards',nvec,'distance = ',distlength)
        #print ("   --- total = ",total_length)
        dist = rnd.random() * total_length
        for invdist in directions:
            dist -= invdist
            if dist <= 0.:
                return directions[invdist]

            
    def step(self, position):
        # a step of the meandering river, with probabilities along the x- or y-direction given by their relative probabilities
        newposition = [position[0],position[1]]
        if rnd.random()<self.Px:
            newposition[0] += self.stepx
        else:
            newposition[1] -= self.stepx
        return newposition

    def found_confluence(self,position,fullmap):
        # checking if the river at a position hits another river or the sea.
        x = position[0]
        y = position[1]
        if (fullmap.tiles[x][y].ttype=='sea' or
            (x>0 and fullmap.tiles[x-1][y].ttype=='sea') or
            (y>0 and fullmap.tiles[x][y-1].ttype=='sea') or
            (x>0 and y>0 and fullmap.tiles[x-1][y-1].ttype=='sea')):
            #print ("   --- river",self.rid,"goes to sea at",position)
            return True
        for river in fullmap.rivers:
            if position in river.links:
                #print ("   --- found confluence of",self.rid,"with",river.rid,"at",position)
                return True
        return False
        
    def meander(self, fullmap):
        # the river is built, step-by-step with the srep function.
        # in each step we check if the edge of the map is reached, if not we add the step to the list of linked
        # positions.  if we find any confluence with another river or the sea we stop.
        position = self.startpos
        while fullmap.check_pos(position):
            self.links.append(position)
            if self.found_confluence(position,fullmap):
                break
            position = self.step(position)
