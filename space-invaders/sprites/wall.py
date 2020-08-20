import pygame
from __main__ import WHITE


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((80, 70))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center = pos)
        self.health = 21
        self.shrink = round(self.rect.w / self.health + 1)

    def hit(self):
        self.health -= 1
        center = self.rect.center
        self.image = pygame.transform.scale(self.image, (self.rect.w - self.shrink, self.rect.h - self.shrink))
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        if self.health == 0:
            self.kill()
