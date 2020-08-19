import pygame
from os import path
'''
Space Invaders clone
'''

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

# prepare sprites and groups
sprites = pygame.sprite.Group()
player = Player()
sprites.add(player)

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
        sprites.add(bullet)
    for bullet in mob_pack.bullets:
        sprites.add(bullet)

    # logic
    if len(mob_pack.mobs) == 0:
        print('win')
        running = False
    hits = pygame.sprite.groupcollide(player.bullets, mob_pack.mobs, True, True)
    bullet_hits = pygame.sprite.spritecollide(player, mob_pack.bullets, False)
    mob_hits = pygame.sprite.spritecollide(player, mob_pack.mobs, False)
    if bullet_hits or mob_hits:
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
