import pygame


class Bullet:
    def __init__(self, pos):
        self.display = pygame.display.get_surface()
        self.x = pos[0]
        self.y = pos[1]
        self.speed = 20
        self.img = pygame.image.load('assets/sprites/bullet.png')
        self.rect = self.img.get_rect(x=self.x, y=self.y)

    def update(self):
        self.y -= self.speed
        self.rect = self.display.blit(self.img, (self.x, self.y))


class Player:
    def __init__(self, pos):
        self.display = pygame.display.get_surface()
        self.x = pos[0]
        self.y = pos[1]
        self.speed = 20
        self.img = pygame.image.load('assets/sprites/ship.png')
        self.rect = self.img.get_rect(x=self.x, y=self.y)
        self.bullets = []

    def left(self):
        self.x -= self.speed

    def right(self):
        self.x += self.speed

    def shoot(self):
        bulletx = self.x + self.img.get_width() / 2 - 2
        self.bullets.append(Bullet((bulletx, self.y + 36)))

    def update(self):
        if self.x <= 0:
            self.x = 0
        if self.x + self.img.get_width() >= self.display.get_width():
            self.x = self.display.get_width() - self.img.get_width()
        for i, b in enumerate(self.bullets):
            b.update()
            if b.y + b.img.get_height() <= 0:
                del self.bullets[i]
        self.rect = self.display.blit(self.img, (self.x, self.y))
