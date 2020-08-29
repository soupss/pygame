import pygame as pg
from settings import *


class Explosion(pg.sprite.Sprite):
    def __init__(self, game, pos, is_bullet=False):
        self.game = game
        self.groups = self.game.sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.load_images()
        if is_bullet:
            self.image = self.frames[1]
        else:
            self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.exploded = pg.time.get_ticks()

    def load_images(self):
        self.frames = [
            self.game.spritesheet.get_image(96, 128, 48, 32, WHITE),
            self.game.spritesheet.get_image(88, 224, 20, 28, WHITE),
        ]

    def update(self):
        now = pg.time.get_ticks()
        if now - self.exploded > EXPLOSION_TIME:
            self.kill()
