import math
import random
import pygame

SCREEN_W=800
SCREEN_H=500
PLAYER_START_X=370
Y=380
ENEMY_START_Y_MIN=50
ENEMY_START_Y_MAX=150
ENEMY_SPEED_X=4
ENEMY_SPEED_Y=40
BULLET_SPEED_Y=10
COLLISION_DISTANCE=27
pygame.init()
screen=pygame.display.set_mode((SCREEN_W,SCREEN_H))
backgroud=pygame.image.load('space_image.png')
pygame.display.set_caption("Space Invaders")
ICON=pygame.image.load('ufo.png')
pygame.display.set_icon(ICON)
player_image=pygame.image.load('space_ship.png')
player_X=PLAYER_START_X
player_Y=Y
player_X_change=0
enemy_image=[]
enemy_X=[]
enemy_Y=[]
enemy_X_change=[]
enemy_Y_change=[]
num_of_enemies=6
for i in range(num_of_enemies):
  enemy_image.append(pygame.image.load('enemy_spaceship.png'))
  enemy_X.append(random.randint(0,SCREEN_W-64))
  enemy_Y.append(random.randint(ENEMY_START_Y_MIN,ENEMY_START_Y_MAX))
  enemy_X_change.append(ENEMY_SPEED_X)
  enemy_Y_change.append(ENEMY_SPEED_Y)
bullet_image=pygame.image.load('bullet.png')
bullet_X=0
bullet_Y=Y
bullet_X_change=0
bullet_Y_change=BULLET_SPEED_Y
bullet_state="ready"
score_value=0
font=pygame.font.Font('freesansbold.ttf',64)
def show_score(x,y):
  score=font.render("score: "+str(score_value),True,(255,255,255))
  screen.blit(score,(x,y))
def game_over_text():
  over_text=over_font.render("Game over",True,(255,255,255))
  screen.blit(over_text,(200,250))
def player(x,y):
  screen.blit(player_image,(x,y))
def enemy(x,y,i):
  screen.blit(enemy_image[i],(x,y))
