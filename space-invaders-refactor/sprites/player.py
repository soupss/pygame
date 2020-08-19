import pygame
from __main__ import WIDTH, HEIGHT, GREEN


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_h]:
            self.speedx = -8
        if keys[pygame.K_l]:
            self.speedx = 8
        self.rect.x += self.speedx
