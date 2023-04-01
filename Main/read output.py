import numpy as np
import pygame

save=True




pygame.init()
pygame.display.set_caption('Synthetic Map Generation')
screen = pygame.display.set_mode( (400*4, 200*4) )
screen.fill((0,0,0))
data = np.load("output1.npy")
screen.fill((0,0,0))
xmax=np.amax(data)
for index, x in np.ndenumerate(data):
    pygame.draw.rect(screen, (255*(x/xmax),0,255-255*(x/xmax)),
                                     pygame.Rect(4*index[0], 4*index[1], 4, 4))
pygame.display.flip()
if save:
    filename="output1.png" 
    pygame.image.save(screen,filename)
