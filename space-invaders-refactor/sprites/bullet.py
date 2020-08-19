import pygame
from __main__ import WIDTH, HEIGHT, WHITE
from sprites import IMG


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x


class PlayerBullet(Bullet):
    def __init__(self, x, y):
        Bullet.__init__(self, x, IMG.PLAYER_BULLET)
        self.speedy = 16
        self.rect.bottom = y + self.speedy

    def update(self):
        self.rect.y -= self.speedy
        if self.rect.bottom < 0:
            self.kill()


class EnemyBullet(Bullet):
    def __init__(self, x, y):
        Bullet.__init__(self, x, IMG.PLAYER_BULLET)
        self.speedy = 6
        self.rect.top = y - self.speedy

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()
