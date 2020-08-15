import pygame


class Enemy:
    def __init__(self, pos, type):
        self.display = pygame.display.get_surface()
        self.x = pos[0]
        self.y = pos[1]
        self.type = type
        self.speed = 3 * (.5 * self.type)
        self.img = pygame.image.load(f'assets/sprites/alien{self.type}.png')
        self.rect = self.img.get_rect(x=self.x, y=self.y)

    def left(self):
        self.speed = -abs(self.speed)

    def right(self):
        self.speed = abs(self.speed)

    def advance(self):
        self.y += self.img.get_height() * self.type

    def update(self):
        self.x += self.speed
        self.rect = self.display.blit(self.img, (self.x, self.y))
