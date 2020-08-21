import pygame
from __main__ import WHITE


bunkerimg = pygame.Surface((80, 70)).convert_alpha()
class Bunker(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bunkerimg
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 21
        self.shrink = round(self.rect.w / self.health + 1) - 2

    def dent(self, surf):
        pass
        # self.image.blit(missile_surf, (missile_x - self.rect.x, missile_y - self.rect.y))

    def hit(self):
        self.health -= 1
        if self.health == 0:
            self.kill()
        center = self.rect.center
        self.image = pygame.transform.scale(self.image, (self.rect.w - self.shrink, self.rect.h - self.shrink))
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        if self.health == 0:
            self.kill()
