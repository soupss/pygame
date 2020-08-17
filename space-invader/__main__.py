import pygame
import random
from player import Player
from enemy import Enemy, Explosion
pygame.init()

# base enemy instance to check enemy vars
_e = Enemy((-1000, -1000), 1)
# base player instance
_p = Player((-1000, -1000))

SCREENSCALE = 4
SCREENWIDTH = 224 * SCREENSCALE  # 896
SCREENHEIGHT = 256 * SCREENSCALE  # 1024
BASEY = SCREENHEIGHT - 20 - _p.img.get_height()
FPS = 60
SHOOT_DELAY = 500  # time between player shots in ms
ENEMY_SHOOT_DELAY = 2000

screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Space Invaders')

player = Player((SCREENWIDTH / 2 - 32, BASEY))

ENEMY_COLS = 8
ENEMY_ROWS = 5
ENEMY_SPACE = 32  # space between enemies
enemies = []


# spawn enemies
for col in range(ENEMY_COLS):
    for row in range(ENEMY_ROWS):
        start_pos = ((_e.img.get_width() + ENEMY_SPACE) * col, (_e.img.get_height() + ENEMY_SPACE) * row)
        enemies.append(Enemy(start_pos, 1))  # new alien type each row

running = True
moving_left = False
moving_right = False
shooting = False
last_shot_time = pygame.time.get_ticks()
enemy_last_shot_time = pygame.time.get_ticks()
enemy_advance = 0
explosions = []
while running:
    screen.fill((0, 0, 0))
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
        if current_time - last_shot_time > SHOOT_DELAY:
            player.shoot()
            last_shot_time = current_time

    # enemy behavior
    for e in enemies:
        if e.x + e.img.get_width() >= screen.get_width():
            for E in enemies:
                E.left()
                enemy_advance = 5
            break
        elif e.x <= 0:
            for E in enemies:
                E.right()
                enemy_advance = 5
            break
        current_time = pygame.time.get_ticks()
        if current_time - enemy_last_shot_time > ENEMY_SHOOT_DELAY:
            random.choice(enemies).shoot()
            enemy_last_shot_time = current_time
    if enemy_advance != 0:
        for e in enemies:
            e.advance()
        enemy_advance -= 1

    # collision
    # enemy - player
    for e in enemies:
        if e.rect.colliderect(player.rect) or e.y + e.img.get_height() > SCREENHEIGHT:
            running = False
    # player bullets
    for i, b in enumerate(player.bullets):
        for I, e in enumerate(enemies):
            if b.rect.colliderect(e.rect):
                del player.bullets[i]
                explosions.append(Explosion(e.x, e.y))
                del enemies[I]
    # enemy bullets
    for e in enemies:
        for i, b in enumerate(e.bullets):
            if b.rect.colliderect(player.rect):
                del e.bullets[i]
                running = False

    # win check
    if len(enemies) == 0:
        running = False
        print('win')

    def get_enemy_speed():
        # max enemies = 8x5 = 40
        # incrementally increase speed
        # this ugly way of doing it gives me the most control
        e = len(enemies)
        if e <= 5:
            return 6.5
        elif e <= 10:
            return 5
        elif e <= 15:
            return 3.8
        elif e <= 20:
            return 3
        elif e <= 25:
            return 2.5
        elif e <= 30:
            return 1.8
        elif e <= 35:
            return 1.3
        else:
            return _e.base_speed

    # update and draw
    for e in enemies:
        e.speed = get_enemy_speed()
        e.update()
    if explosions:
        for e in explosions:
            e.update()
    print('enemy:', enemies[0].speed)
    player.update()
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
