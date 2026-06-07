import pygame
import random
import sys

# ── Initialise ────────────────────────────────────────────────────────────────
pygame.init()

SCREEN_W, SCREEN_H = 800, 600
FPS             = 60
NUM_ENEMIES     = 7

# Colours
WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)
SKY     = ( 30,  30,  60)      # dark‑navy background
PLAYER_COL  = ( 72, 199, 142)  # mint‑green
ENEMY_COL   = (255,  82,  82)  # coral‑red
TEXT_COL    = (255, 220,  80)  # warm‑yellow HUD

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Collision Score Demo")
clock  = pygame.time.Clock()
font   = pygame.font.SysFont("monospace", 28, bold=True)


# ── Sprite classes ────────────────────────────────────────────────────────────
class Player(pygame.sprite.Sprite):
    SIZE  = 40
    SPEED = 4

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)
        # Draw a simple spaceship‑like triangle
        pts = [(self.SIZE // 2, 0),
               (0, self.SIZE),
               (self.SIZE, self.SIZE)]
        pygame.draw.polygon(self.image, PLAYER_COL, pts)
        self.rect = self.image.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))

    def update(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: dx -= self.SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += self.SPEED
        if keys[pygame.K_UP]    or keys[pygame.K_w]: dy -= self.SPEED
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: dy += self.SPEED
        self.rect.x = max(0, min(SCREEN_W - self.SIZE, self.rect.x + dx))
        self.rect.y = max(0, min(SCREEN_H - self.SIZE, self.rect.y + dy))


class Enemy(pygame.sprite.Sprite):
    SIZE  = 32
    MIN_SPEED = 1
    MAX_SPEED = 3

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)
        # Draw a diamond enemy
        cx = cy = self.SIZE // 2
        pts = [(cx, 0), (self.SIZE, cy), (cx, self.SIZE), (0, cy)]
        pygame.draw.polygon(self.image, ENEMY_COL, pts)
        self._place_randomly()
        self.vx = random.choice([-1, 1]) * random.uniform(self.MIN_SPEED, self.MAX_SPEED)
        self.vy = random.choice([-1, 1]) * random.uniform(self.MIN_SPEED, self.MAX_SPEED)

    def _place_randomly(self):
        x = random.randint(0, SCREEN_W - self.SIZE)
        y = random.randint(0, SCREEN_H - self.SIZE)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_W:
            self.vx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_H:
            self.vy *= -1


# ── Build sprite groups ───────────────────────────────────────────────────────
player       = Player()
player_group = pygame.sprite.GroupSingle(player)

enemy_group  = pygame.sprite.Group()
for _ in range(NUM_ENEMIES):
    enemy_group.add(Enemy())

all_sprites  = pygame.sprite.Group(player, *enemy_group)

score = 0

# ── Star field (decorative background) ───────────────────────────────────────
stars = [(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H),
          random.randint(1, 3)) for _ in range(120)]


# ── Main loop ─────────────────────────────────────────────────────────────────
running = True
while running:
    clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Update
    all_sprites.update()

    # Collision detection ─ collided enemies bounce away; score increases
    hit_enemies = pygame.sprite.spritecollide(player, enemy_group, False,
                                              pygame.sprite.collide_rect)
    for enemy in hit_enemies:
        score += 1
        # Reverse the enemy's direction so it bounces away
        enemy.vx *= -1
        enemy.vy *= -1

    # ── Draw ──────────────────────────────────────────────────────────────────
    screen.fill(SKY)

    # Stars
    for sx, sy, sr in stars:
        pygame.draw.circle(screen, WHITE, (sx, sy), sr)

    all_sprites.draw(screen)

    # HUD
    score_surf = font.render(f"SCORE : {score}", True, TEXT_COL)
    screen.blit(score_surf, (16, 12))

    hint_surf = pygame.font.SysFont("monospace", 16).render(
        "WASD / Arrow keys to move  |  ESC to quit", True, (160, 160, 200))
    screen.blit(hint_surf, (16, SCREEN_H - 28))

    pygame.display.flip()

pygame.quit()
sys.exit()
