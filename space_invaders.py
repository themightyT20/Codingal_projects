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
background=pygame.image.load('space_image.png')
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
font=pygame.font.Font('freesansbold.ttf',32)
text_X=10
text_Y=10
over_font=pygame.font.Font('freesansbold.ttf',64)
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
def fire_bullet(x,y):
  global bullet_state
  bullet_state="fire"
  screen.blit(bullet_image,(x+16,y+10))
def iscollision(enemy_X,enemy_Y,bullet_X,bullet_Y):
  distance=math.sqrt((enemy_X-bullet_X)**2+(enemy_Y-bullet_Y)**2)
  return distance<COLLISION_DISTANCE
running=True
while running:
  screen.fill((0,0,0))
  screen.blit(background,(0,0))
  for event in pygame.event.get():
    if event.type==pygame.QUIT:
      running=False
    if event.type==pygame.KEYDOWN:
      if event.key==pygame.K_LEFT:
        player_X_change=-5
      if event.key==pygame.K_RIGHT:
        player_X_change=5
      if event.key==pygame.K_SPACE and bullet_state=="ready":
        bullet_X=player_X
        fire_bullet(bullet_X,bullet_Y)
    if event.type==pygame.KEYUP and event.key in [pygame.K_LEFT,pygame.K_RIGHT]:
      player_X_change=0
  player_X+=player_X_change
  player_X=max(0,min(player_X,SCREEN_W-64))
  for i in range(num_of_enemies):
    if enemy_Y[i]>340:
      for j in range(num_of_enemies):
        enemy_Y[j]=2000
      game_over_text()
      break
  enemy_X[i]+=enemy_X_change[i]
  if enemy_X[i]<=0 or enemy_X[i]>=SCREEN_W-64:
    enemy_X_change[i]*=-5
    enemy_Y[i]+=enemy_Y_change[i]
  if iscollision(enemy_X[i],enemy_Y[i],bullet_X,bullet_Y):
    bullet_Y=Y
    bullet_state="ready"
    score_value+=1
    enemy_X[i]=random.randint(0,SCREEN_W-64)
    enemy_Y[i]=random.randint(ENEMY_Y_START_MIN,ENEMY_Y_START_MAX)
  enemy(enemy_X[i],enemy_Y[i],i)
  if bullet_Y<=0:
   bullet_Y=Y
   bullet_state="ready"
  elif bullet_state=="fire":
   fire_bullet(bullet_X,bullet_Y)
   bullet_Y-=bullet_Y_change
  player(player_X,player_Y)
  show_score(text_X,text_Y)
  pygame.display.update()
