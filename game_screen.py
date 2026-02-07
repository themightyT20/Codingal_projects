import pygame
pygame.init()
screen_width,screen_height=500,500
display_surface=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('My-first_game-screen')
background_image=pygame.transform.scale(pygame.image.load('grey_background.png').convert(),(screen_width,screen_height))
penguin_image=pygame.transform.scale(pygame.image.load('game_screen.png').convert_alpha(),(300,300))
penguin_rect=penguin_image.get_rect(center=(screen_width//2,screen_height//2-30))
def game_loop():
 clock=pygame.time.Clock()
 running=True
 while running:
  for event in pygame.event.get():
   if event.type==pygame.QUIT:
    running=False
  display_surface.blit(background_image,(0,0))
  display_surface.blit(penguin_image,penguin_rect)
  pygame.display.flip()
  clock.tick(30)
 pygame.quit()
if __name__=='__main__':
 game_loop()
