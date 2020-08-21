import pygame
from __main__ import FIELD, WHITE, GREEN
from init import IMG


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.mask = pygame.mask.from_surface(self.image)


class PlayerBullet(Bullet):
    def __init__(self, x, y):
        Bullet.__init__(self, x, IMG.get('player_bullet', WHITE))
        self.speedy = 16
        self.rect.bottom = y + self.speedy

    def update(self):
        self.rect.y -= self.speedy
        if self.rect.top < 0:
            self.kill()


class EnemyBullet(Bullet):
    def __init__(self, x, y):
        Bullet.__init__(self, x, IMG.get('player_bullet', WHITE))
        self.speedy = 5
        self.rect.top = y - self.speedy

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > FIELD.y:
            self.kill()
