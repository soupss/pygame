import pygame
from player import Player
from enemy import Enemy
pygame.init()

SCREENWIDTH = 900
SCREENHEIGHT = 900
BASEY = SCREENHEIGHT - 20 - 64
FPS = 60
level = 1

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Space Invaders')

player = Player((SCREENWIDTH / 2 - 32, BASEY))

enemy_cols = 8
enemies = []


def spawn_enemies(level):
    for i in range(1, enemy_cols + 1):
        for I in range(1, level + 1):
            enemies.append(Enemy(((64 + 20) * i, (64 + 20) * I), level))


spawn_enemies(level)

running = True
moving_left = False
moving_right = False
shooting = False
last_shot_time = pygame.time.get_ticks()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                moving_left = True
            if event.key == pygame.K_l:
                moving_right = True
            if event.key == pygame.K_z:
                shooting = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_h:
                moving_left = False
            if event.key == pygame.K_l:
                moving_right = False
            if event.key == pygame.K_z:
                shooting = False
    if moving_left:
        player.left()
    if moving_right:
        player.right()
    if shooting:
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > 500:
            player.shoot()
            last_shot_time = current_time

    # enemy movement
    for e in enemies:
        if e.x + e.img.get_width() >= screen.get_width():
            for E in enemies:
                E.left()
                E.advance()
            break
        elif e.x <= 0:
            for E in enemies:
                E.right()
                E.advance()
            break

    # collision
    for e in enemies:
        if e.rect.colliderect(player.rect):
            running = False
    for i, b in enumerate(player.bullets):
        for I, e in enumerate(enemies):
            if b.rect.colliderect(e.rect):
                del enemies[I]
                del player.bullets[i]

    # win check
    if len(enemies) == 0:
        if level == 3:
            running = False
            print('win')
        level += 1
        spawn_enemies(level)

    # update and draw
    screen.fill((0, 0, 0))
    for e in enemies:
        e.update()
    player.update()
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
