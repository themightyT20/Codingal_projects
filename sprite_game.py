import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Sprites")

WHITE = (255, 255, 255)
BLUE  = (50, 120, 220)
RED   = (220, 60,  60)
BLACK = (0, 0, 0)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(Sprite):
    def __init__(self, color, x, y, width, height, speed=5):
        super().__init__(color, x, y, width, height)
        self.speed = speed

    def update(self, keys):
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        self.rect.x = max(0, min(WIDTH  - self.rect.width,  self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

font = pygame.font.SysFont(None, 28)

player  = Player(BLUE, 100, 250, 80, 80)
static  = Sprite(RED,  550, 250, 80, 80)

all_sprites = pygame.sprite.Group(player, static)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    player.update(keys)

    screen.fill(WHITE)
    all_sprites.draw(screen)

    label_player = font.render("Player (Arrow Keys)", True, BLACK)
    label_static = font.render("Static Sprite",       True, BLACK)
    screen.blit(label_player, (player.rect.x - 20, player.rect.y - 25))
    screen.blit(label_static, (static.rect.x -  5, static.rect.y - 25))

    pygame.display.flip()
    clock.tick(60)
