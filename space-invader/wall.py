import pygame


class Wall:
    def __init__(self, x, y):
        self.display = pygame.display.get_surface()
        self.health = 8
        self.x = x
        self.y = y
        self.img = pygame.image.load('assets/sprites/wall.png')

    def update(self):
        self.rect = self.display.blit(self.img, (self.x, self.y))
