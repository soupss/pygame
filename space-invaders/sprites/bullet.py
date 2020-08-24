import pygame as pg
from settings import *


class Bullet(pg.sprite.Sprite):
    def __init__(self, groups):
        self.groups = groups
        pg.sprite.Sprite.__init__(self, self.groups)


class PlayerBullet(Bullet):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.sprites, self.game.bullets, self.game.player_bullets
        Bullet.__init__(self, self.groups)
        self.image = self.game.spritesheet.get_image(60, 0, 4, 16, GREEN)
        self.rect = self.image.get_rect(center=(x, y + PLAYER_BULLET_HEIGHT))
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        if self.rect.top - 4 < TOP_SPACING:
            self.kill()
        self.rect.y -= PLAYER_BULLET_SPEED


class MobBullet(Bullet):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.sprites, self.game.bullets, self.game.mob_bullets
        Bullet.__init__(self, self.groups)
        self.load_images()
        self.last_updated = pg.time.get_ticks()
        self.frame = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=(x, y + MOB_BULLET_HEIGHT))

    def load_images(self):
        self.frames = [
            self.game.spritesheet.get_image(64, 224, 12, 28, WHITE),
            self.game.spritesheet.get_image(76, 224, 12, 28, WHITE),
            pg.transform.flip(self.game.spritesheet.get_image(64, 224, 12, 28, WHITE), True, False),
            pg.transform.flip(self.game.spritesheet.get_image(76, 224, 12, 28, WHITE), True, False)
        ]

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_updated > MOB_BULLET_FRAME_RATE:
            self.frame += 1
            if self.frame == len(self.frames):
                self.frame = 0
            self.image = self.frames[self.frame]
            self.last_updated = now
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        if self.rect.bottom > HEIGHT - BOT_SPACING:
            self.kill()
        self.rect.y += MOB_BULLET_SPEED
        self.animate()
