import pygame as pg
from settings import *


class Bunker(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.sprites, self.game.bunkers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = self.game.spritesheet.get_image(0, 64, 88, 64, GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pg.mask.from_surface(self.image)

        # le focused goyo mode >:)
