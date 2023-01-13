import pygame

PLAINS      = (154, 205,  50)
DESERT     = (255, 235, 205)
MOUNTAIN = (139,  69,  19)
ALPINE        = (225,245,255)
SEA            = ( 70, 130, 180)
NOTHING   = (  0,   0,   0)

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

    def draw_map(self):
        self.draw_tiles()
        self.draw_rivers()
        if self.display:
            pygame.display.flip()

    def draw_tiles(self):
        for x in range(len(self.tiles)):
            for y in range(len(self.tiles[x])):
                tile   = self.tiles[x][y]
                xpos = x*self.tdim[0] + self.margin
                ypos = y*self.tdim[1] + self.margin
                if self.display:
                    pygame.draw.rect(self.screen, self.display_colour(tile),
                                     pygame.Rect(xpos, ypos, self.xsize, self.ysize))
                
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


    
