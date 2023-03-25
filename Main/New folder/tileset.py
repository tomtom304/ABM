import pygame


TDIM     = (30, 30)
MARGIN    = 2
PLAINS      = (154, 205,  50)
DESERT     = (255, 235, 205)
MOUNTAIN = (139,  69,  19)
ALPINE        = (225,245,255)
SEA            = ( 70, 130, 180)
NOTHING   = (  0,   0,   0)


class TileSet:
    def __init__(self, fullmap):
        self.tiles   = fullmap.tiles
        self.rivers = fullmap.rivers
        self.ntiles  = fullmap.ntiles
        self.wdim  = (self.ntiles[0]*TDIM[0], self.ntiles[1]*TDIM[1])
        self.xsize   = TDIM[0]-2*MARGIN
        self.ysize   = TDIM[1]-2*MARGIN
        self.display = True
        if self.display:
            pygame.init()
            self.screen = pygame.display.set_mode(self.wdim)
            pygame.display.set_caption('Synthetic Map Generation')

    def draw(self):
        self.draw_tiles()
        self.draw_rivers()
        if self.display:
            pygame.display.flip()

    def draw_tiles(self):
        for x in range(len(self.tiles)):
            for y in range(len(self.tiles[x])):
                tile   = self.tiles[x][y]
                xpos = x*TDIM[0] + MARGIN
                ypos = y*TDIM[1] + MARGIN
                if self.display:
                    pygame.draw.rect(self.screen, tile.display_colour(),
                                     pygame.Rect(xpos, ypos, self.xsize, self.ysize))
                #print ('Tile at x = ',x,' (',tile.pos[0],'), y = ',y,' (',tile.pos[1],'), ',
                #       ' type = ',tile.ttype)
                
    def draw_rivers(self):        
        for river in self.rivers:
            for i in range(len(river.links)-1):
                x0 = river.links[i][0]
                y0 = river.links[i][1]
                x1 = river.links[i+1][0]
                y1 = river.links[i+1][1]
                if x1<x0:
                    helpx = x0
                    x0 = x1
                    x1 = helpx
                if y1<y0:
                    helpy = y0
                    y0 = y1
                    y1 = helpy
                xsize = (x1-x0)*TDIM[0]
                ysize = (y1-y0)*TDIM[1]
                if x1==x0:
                    xsize = 6*MARGIN
                if y1==y0:
                    ysize = 6*MARGIN
                if self.display:
                    pygame.draw.rect(self.screen,SEA,pygame.Rect(x0*TDIM[0], y0*TDIM[1], xsize, ysize))
                    if  x1==self.ntiles[0]-1:
                        pygame.draw.rect(self.screen,SEA,pygame.Rect( x1*TDIM[0], y0*TDIM[1], xsize, ysize))
                    if  y1==self.ntiles[1]-1:
                        pygame.draw.rect(self.screen,SEA,pygame.Rect( x0*TDIM[0], y1*TDIM[1], xsize, ysize))
                #print ("drawing [",x0,y0,"] -> [",x1,y1,"]")


class Tile:
    def __init__(self, pos = (0,0), ttype = 'none'):
        self.pos   = pos
        self.ttype = ttype

    def SetBasics(self, pos = (0,0), ttype = 'none'):
        self.pos   = pos
        self.ttype = ttype
        
    def display_colour(self):
        if (self.ttype=='plains'):
            return PLAINS
        elif (self.ttype=='desert'):
            return DESERT
        elif (self.ttype=='mountain'):
            return MOUNTAIN
        elif (self.ttype=='alpine'):
            return ALPINE
        elif (self.ttype=='sea'):
            return SEA
        return NOTHING

    
