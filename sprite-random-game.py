import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Custom Event - Color Change")

WHITE = (255, 255, 255)
BLACK = (0,   0,   0)

def random_color():
    return (random.randint(30, 255), random.randint(30, 255), random.randint(30, 255))

class ColorSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.width  = width
        self.height = height
        self.color  = random_color()
        self.image  = pygame.Surface((width, height))
        self.image.fill(self.color)
        self.rect   = self.image.get_rect(topleft=(x, y))

    def change_color(self):
        self.color = random_color()
        self.image.fill(self.color)

CHANGE_COLOR_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(CHANGE_COLOR_EVENT, 1000)

sprite1 = ColorSprite(150, 200, 120, 120)
sprite2 = ColorSprite(530, 200, 120, 120)

all_sprites = pygame.sprite.Group(sprite1, sprite2)

font_large = pygame.font.SysFont(None, 42)
font_small = pygame.font.SysFont(None, 28)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == CHANGE_COLOR_EVENT:
            sprite1.change_color()
            sprite2.change_color()

    screen.fill(WHITE)

    title = font_large.render("Custom Color Change Event", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

    hint = font_small.render("Colours change every 1 second via custom event", True, (100, 100, 100))
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 90))

    all_sprites.draw(screen)

    label1 = font_small.render("Sprite 1", True, BLACK)
    label2 = font_small.render("Sprite 2", True, BLACK)
    screen.blit(label1, (sprite1.rect.x + 25, sprite1.rect.bottom + 10))
    screen.blit(label2, (sprite2.rect.x + 25, sprite2.rect.bottom + 10))

    color_text1 = font_small.render(str(sprite1.color), True, sprite1.color)
    color_text2 = font_small.render(str(sprite2.color), True, sprite2.color)
    screen.blit(color_text1, (sprite1.rect.x, sprite1.rect.bottom + 35))
    screen.blit(color_text2, (sprite2.rect.x, sprite2.rect.bottom + 35))

    pygame.display.flip()
    clock.tick(60)
