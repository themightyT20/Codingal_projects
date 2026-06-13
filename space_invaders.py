"""
Space Invaders - Improved Version (with Sound)
================================================
Sounds added:
  - shoot      : rising laser blip on SPACE
  - explosion  : noise burst when enemy is hit
  - life_lost  : descending 3-tone sting when enemy reaches bottom
  - game_over  : ominous descending chord
All sounds are synthesised via numpy so no external audio files are needed.
Drop in shoot.wav / explosion.wav / life_lost.wav / game_over.wav to override.
"""

import math
import random
import sys
import numpy as np
import pygame

# Constants
SCREEN_W          = 800
SCREEN_H          = 500
FPS               = 60
PLAYER_Y          = 380
PLAYER_SPEED      = 5
ENEMY_START_Y_MIN = 50
ENEMY_START_Y_MAX = 150
ENEMY_DANGER_Y    = 340
BASE_ENEMY_SPEED  = 4
ENEMY_DROP        = 40
NUM_ENEMIES       = 6
BULLET_SPEED      = 10
MAX_BULLETS       = 3
COLLISION_DIST    = 27
LIVES_START       = 3
KILLS_PER_LEVEL   = 6
SAMPLE_RATE       = 44100
WHITE  = (255, 255, 255)
RED    = (255,  60,  60)
YELLOW = (255, 220,  50)
BLACK  = (  0,   0,   0)


def _make_sound(samples):
    audio  = np.clip(samples, -1.0, 1.0)
    audio  = (audio * 32767).astype(np.int16)
    stereo = np.column_stack([audio, audio])
    return pygame.sndarray.make_sound(stereo)

def synth_shoot():
    dur = 0.12
    t   = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    freq_sweep = np.linspace(880, 2200, len(t))
    wave = 0.4 * np.sin(2 * np.pi * freq_sweep * t) * np.exp(-t * 18)
    return _make_sound(wave)

def synth_explosion():
    dur = 0.45
    t   = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    noise = np.random.uniform(-1, 1, len(t))
    freq_sweep = np.linspace(400, 60, len(t))
    tone = np.sin(2 * np.pi * freq_sweep * t)
    wave = (0.5 * noise + 0.5 * tone) * np.exp(-t * 7)
    return _make_sound(wave)

def synth_life_lost():
    dur  = 0.6
    t    = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    seg  = len(t) // 3
    wave = np.zeros(len(t))
    for i, f in enumerate([523, 349, 220]):
        sl = slice(i * seg, (i + 1) * seg)
        tt = t[sl] - t[sl][0]
        wave[sl] = 0.5 * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 6)
    return _make_sound(wave)

def synth_game_over():
    dur = 1.2
    t   = np.linspace(0, dur, int(SAMPLE_RATE * dur), endpoint=False)
    fs  = np.linspace(300, 60, len(t))
    wave = (0.4 * np.sin(2 * np.pi * fs * t)
          + 0.3 * np.sin(2 * np.pi * fs * 1.5 * t)
          + 0.2 * np.sin(2 * np.pi * fs * 2.0 * t)) * np.exp(-t * 1.5)
    return _make_sound(wave)

def load_sound(path, fallback_fn):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        return fallback_fn()

def draw_centred(surface, font, text, colour, cy):
    surf = font.render(text, True, colour)
    surface.blit(surf, (SCREEN_W // 2 - surf.get_width() // 2, cy))

def load_image(path, fallback_size=(64, 64), fallback_colour=(200, 200, 200)):
    try:
        return pygame.image.load(path)
    except pygame.error:
        surf = pygame.Surface(fallback_size, pygame.SRCALPHA)
        surf.fill(fallback_colour)
        return surf


class Player:
    def __init__(self, image):
        self.image = image
        self.x     = (SCREEN_W - image.get_width()) // 2
        self.y     = PLAYER_Y
        self.vx    = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  self.vx = -PLAYER_SPEED
            if event.key == pygame.K_RIGHT: self.vx =  PLAYER_SPEED
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.vx = 0

    def update(self):
        self.x = max(0, min(self.x + self.vx, SCREEN_W - self.image.get_width()))

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class Enemy:
    def __init__(self, image, speed_multiplier=1.0):
        self.image = image
        self.speed = BASE_ENEMY_SPEED * speed_multiplier
        self.vx    = self.speed
        self._place()

    def _place(self):
        max_x  = max(0, SCREEN_W - self.image.get_width())
        self.x = random.randint(0, max_x)
        self.y = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)

    def reset(self, speed_multiplier=1.0):
        self.speed = BASE_ENEMY_SPEED * speed_multiplier
        self.vx    = self.speed
        self._place()

    def update(self):
        self.x += self.vx
        w = self.image.get_width()
        if self.x <= 0 or self.x >= max(1, SCREEN_W - w):
            self.vx *= -1
            self.y  += ENEMY_DROP

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    @property
    def past_danger_line(self):
        return self.y > ENEMY_DANGER_Y


class Bullet:
    def __init__(self, image, x, y):
        self.image  = image
        self.x      = x
        self.y      = y
        self.active = True

    def update(self):
        self.y -= BULLET_SPEED
        if self.y < 0:
            self.active = False

    def draw(self, surface):
        surface.blit(self.image, (self.x + 16, self.y + 10))

    def hits(self, enemy):
        return math.hypot(enemy.x - self.x, enemy.y - self.y) < COLLISION_DIST


def main():
    pygame.mixer.pre_init(SAMPLE_RATE, -16, 2, 512)
    pygame.init()
    pygame.mixer.init(SAMPLE_RATE, -16, 2, 512)

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Space Invaders")
    clock  = pygame.time.Clock()

    # Background
    try:
        background = pygame.image.load("space_image.png")
    except pygame.error:
        background = pygame.Surface((SCREEN_W, SCREEN_H))
        background.fill((10, 10, 30))
        for _ in range(120):
            pygame.draw.circle(background, WHITE,
                (random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)),
                random.randint(1, 2))

    try:
        pygame.display.set_icon(pygame.image.load("ufo.png"))
    except pygame.error:
        pass

    # Images
    player_img = pygame.transform.scale(
        load_image("space_ship.png",      fallback_colour=(72, 199, 142)), (64, 64))
    enemy_img  = pygame.transform.scale(
        load_image("enemy_spaceship.png", fallback_colour=(255, 82, 82)),  (48, 48))
    bullet_img = pygame.transform.scale(
        load_image("bullet.png", (8, 24), fallback_colour=(255, 220, 50)), (8, 24))

    # Sounds
    snd_shoot     = load_sound("shoot.wav",     synth_shoot)
    snd_explosion = load_sound("explosion.wav", synth_explosion)
    snd_life_lost = load_sound("life_lost.wav", synth_life_lost)
    snd_game_over = load_sound("game_over.wav", synth_game_over)
    snd_shoot.set_volume(0.4)
    snd_explosion.set_volume(0.7)
    snd_life_lost.set_volume(0.8)
    snd_game_over.set_volume(0.9)

    # Fonts
    hud_font = pygame.font.Font("freesansbold.ttf", 28)
    big_font = pygame.font.Font("freesansbold.ttf", 56)
    mid_font = pygame.font.Font("freesansbold.ttf", 32)

    def new_game():
        spd = 1.0
        p   = Player(player_img)
        es  = [Enemy(enemy_img, spd) for _ in range(NUM_ENEMIES)]
        return p, es, [], 0, LIVES_START, spd, False

    player, enemies, bullets, score, lives, speed_mult, game_over = new_game()
    flash_timer      = 0
    game_over_played = False

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False; break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False; break
                if game_over:
                    if event.key == pygame.K_r:
                        player, enemies, bullets, score, lives, speed_mult, game_over = new_game()
                        game_over_played = False
                    continue
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullets.append(Bullet(bullet_img, player.x, player.y))
                    snd_shoot.play()                      # shoot sound
            if not game_over:
                player.handle_event(event)

        if not running:
            break

        if not game_over:
            player.update()
            for b in bullets: b.update()
            bullets = [b for b in bullets if b.active]

            invaded = False
            for enemy in enemies:
                enemy.update()
                if enemy.past_danger_line:
                    invaded = True
                for bullet in bullets:
                    if bullet.active and bullet.hits(enemy):
                        bullet.active = False
                        score        += 1
                        flash_timer   = 6
                        level         = score // KILLS_PER_LEVEL + 1
                        speed_mult    = 1.0 + (level - 1) * 0.2
                        enemy.reset(speed_mult)
                        snd_explosion.play()              # explosion sound

            if invaded:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    snd_life_lost.play()                  # life-lost sound
                    for enemy in enemies:
                        enemy.reset(speed_mult)

            if game_over and not game_over_played:
                snd_game_over.play()                      # game-over sound
                game_over_played = True

            if flash_timer > 0:
                flash_timer -= 1

        # Draw
        screen.blit(background, (0, 0))
        if flash_timer > 0:
            fs = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            fs.fill((255, 255, 100, 60))
            screen.blit(fs, (0, 0))

        for e in enemies: e.draw(screen)
        for b in bullets: b.draw(screen)
        player.draw(screen)

        screen.blit(hud_font.render(f"Score: {score}", True, WHITE), (10, 10))
        ls = hud_font.render(f"Lives: {lives}", True, YELLOW)
        screen.blit(ls, (SCREEN_W - ls.get_width() - 10, 10))
        lv = hud_font.render(f"Level: {score // KILLS_PER_LEVEL + 1}", True, (150, 220, 255))
        screen.blit(lv, (SCREEN_W // 2 - lv.get_width() // 2, 10))

        if game_over:
            ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            ov.fill((0, 0, 0, 160))
            screen.blit(ov, (0, 0))
            draw_centred(screen, big_font, "GAME OVER",            RED,    170)
            draw_centred(screen, mid_font, f"Final Score: {score}", WHITE,  260)
            draw_centred(screen, mid_font, "Press  R  to Restart", YELLOW, 320)
            draw_centred(screen, hud_font, "ESC to Quit",           WHITE,  380)

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
