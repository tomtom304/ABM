import numpy as np
import pygame
import matplotlib.pyplot as plt

save=True

filenames=("longevity","pop","conflict")


pygame.init()

pygame.display.set_caption("Real Map")
screen = pygame.display.set_mode( (400*4, 200*4) )
for name in filenames:
    data=np.array([[0.0 for i in range(200)] for j in range(400)])
    for i in range(10):
        print(i)
        data += np.load(str(i+1)+"/"+name+".npy")/10
    screen.fill((0,100,255))
    xmax=np.partition(data.flatten(), -2)[-2]
    for index, x in np.ndenumerate(data):
        if x!=0:
            pygame.draw.rect(screen, (min(255,abs(255*(x/xmax))),0,0), pygame.Rect(4*index[0], 4*index[1], 4, 4))
    pygame.display.flip()
    if save:
        filename=name+".png" 
        pygame.image.save(screen,filename)


fig=plt.figure()
fig.set_tight_layout(True)
filenames=("sizedist","popdist","towndist")
for name in filenames:
    plt.figure()
    data = np.load(name+".npy")
    data=np.array([[0.0 for i in range(5)] for j in range(2000)])
    for i in range(10):
        print(i)
        data += np.load(str(i+1)+"/"+name+".npy")/10
    for i in range(5):
        plt.plot(range(len(data)),data[:,i],label=name)
    plt.savefig(name+".png")
    
