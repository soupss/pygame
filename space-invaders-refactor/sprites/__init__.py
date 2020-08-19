import pygame
from os import path
from __main__ import BASE_DIR, BLACK

IMG_DIR = path.join(BASE_DIR, path.join('assets', 'img'))

class Images:
    PLAYER = pygame.image.load(path.join(IMG_DIR, 'ship.png')).convert()
    PLAYER_BULLET = pygame.image.load(path.join(IMG_DIR, 'player_bullet.png')).convert()
    ALIENS = {
            '1': pygame.image.load(path.join(IMG_DIR, 'alien1.png')).convert(),
            '2': pygame.image.load(path.join(IMG_DIR, 'alien2.png')).convert(),
            '3': pygame.image.load(path.join(IMG_DIR, 'alien3.png')).convert()
    }

    PLAYER.set_colorkey(BLACK)
    for a in ALIENS:
        ALIENS[a].set_colorkey(BLACK)

print('loading sprite images...')
IMG = Images()
print('all sprite images loaded')
