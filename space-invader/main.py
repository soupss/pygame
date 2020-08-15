import pygame
from player import Player
from enemy import Enemy
pygame.init()

SCREENWIDTH = 900
SCREENHEIGHT = 900
BASEY = SCREENHEIGHT - 20 - 64
FPS = 60

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Space Invaders')
pygame.key.set_repeat(round(1000/FPS))


player = Player((SCREENWIDTH/2 - 32, BASEY))

enemy_cols = 8
enemy_rows = 4
enemies = []
for i in range(1, enemy_cols + 1):
    enemies.append(Enemy(((64+20)*i, 20), 1))

running = True
moving_left = False
moving_right = False
shooting = False
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
        player.shoot()

    # enemy movement
    for e in enemies:
        if e.x + e.img.get_width() >= screen.get_width() or e.x <= 0:
            for E in enemies:
                E.advance()

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
        running = False
        print('win')

    # update and draw
    screen.fill((0, 0, 0))
    for e in enemies:
        e.update()
    player.update()
    pygame.display.update()
    clock.tick(FPS)
