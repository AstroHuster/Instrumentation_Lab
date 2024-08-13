#importing libraries
import pygame
 
# initializing the pygame
pygame.init()
 
# drawing the surface
surface= pygame.display.set_mode((400,300))
 
#initializing the color
color = (255,0,0)
 
# drawing the rectangle
pygame.draw.rect(surface, color,pygame.Rect(100,150,200,150))
pygame.display.flip()

from time import sleep
sleep(10)
