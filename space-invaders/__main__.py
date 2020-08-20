'''
Space Invaders clone
'''
import pygame
from os import path

# constants
WIDTH = 224 * 3
HEIGHT = 256 * 3
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BASE_DIR = path.join(path.dirname(__file__))

# pygame initialization
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()

# uses constants and display so imported after
from sprites.player import Player
from sprites.mob import MobPack
from sprites.wall import Wall

# prepare sprites and groups
sprites = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
walls = pygame.sprite.Group()

player = Player()
sprites.add(player)

temp = Wall((0, 0))
for i in range(1, 4 + 1):
    spacing = WIDTH / 5 + 20
    offset = (WIDTH - (temp.rect.w * 4 + spacing * 3)) / 2
    wall = Wall((offset + i*spacing, HEIGHT - 180))
    wall.add(sprites, walls)
del temp

mob_pack = MobPack(20, 80, 11, 5)
for mob in mob_pack.mobs:
    sprites.add(mob)

# game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    # dynamic sprite groups
    for bullet in player.bullets:
        bullet.add(sprites, all_bullets)
    for bullet in mob_pack.bullets:
        bullet.add(sprites, all_bullets)

    # logic
    if len(mob_pack.mobs) == 0:
        print('win')
        running = False

    # player shoots mobs
    player_bullets_hit_mobs = pygame.sprite.groupcollide(player.bullets, mob_pack.mobs, True, True)

    # wall collision
    player_bullets_hit_walls = pygame.sprite.groupcollide(walls, player.bullets, False, True)
    mob_bullets_hit_walls = pygame.sprite.groupcollide(walls, mob_pack.bullets, False, True)
    for wall in mob_bullets_hit_walls:
        wall.hit()
    for wall in player_bullets_hit_walls:
        wall.hit()

    # things hit player
    mob_bullets_hit_player = pygame.sprite.spritecollide(player, mob_pack.bullets, False)
    mobs_hit_player = pygame.sprite.spritecollide(player, mob_pack.mobs, False)
    if mob_bullets_hit_player or mobs_hit_player:
        print('player hit')
        running = False

    # update
    sprites.update()
    mob_pack.update()

    # render
    screen.fill(BLUE)
    sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
