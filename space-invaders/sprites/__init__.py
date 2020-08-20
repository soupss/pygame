import pygame
from os import path
from __main__ import BASE_DIR, BLACK

IMG_DIR = path.join(BASE_DIR, path.join('assets', 'img'))

class Images:
    PLAYER = pygame.image.load(path.join(IMG_DIR, 'ship.png')).convert_alpha()
    PLAYER_BULLET = pygame.image.load(path.join(IMG_DIR, 'player_bullet.png')).convert_alpha()
    ALIENS = {
            '1': pygame.image.load(path.join(IMG_DIR, 'alien1.png')).convert_alpha(),
            '2': pygame.image.load(path.join(IMG_DIR, 'alien2.png')).convert_alpha(),
            '3': pygame.image.load(path.join(IMG_DIR, 'alien3.png')).convert_alpha()
    }

print('loading sprite images...')
IMG = Images()
print('all sprite images loaded')
