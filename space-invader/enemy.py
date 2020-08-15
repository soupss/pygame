import pygame


class Enemy:
    def __init__(self, pos, type):
        self.display = pygame.display.get_surface()
        self.x = pos[0]
        self.y = pos[1]
        self.speed = 3
        self.img = pygame.image.load(f'assets/sprites/alien{type}.png')
        self.rect = self.img.get_rect(x=self.x, y=self.y)

    def advance(self):
        self.speed *= -1
        self.y += self.img.get_height() * 2

    def update(self):
        self.x += self.speed
        self.rect = self.display.blit(self.img, (self.x, self.y))
