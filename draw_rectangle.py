import pygame
pygame.init()
screen=pygame.display.set_mode((400,300))
done=False
while not done:
 for event in pygame.event.get():
   if event.type==pygame.QUIT:
     done=True
 pygame.draw.rect(screen,(0,125,125),pygame.Rect(50,100,250,150))
 pygame.display.flip()

