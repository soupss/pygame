import pygame
from __main__ import WIDTH, HEIGHT, RED


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((36, 36))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed = 1
        self.rect.x = x
        self.rect.y = y

class MobPack():
    def __init__(self, startx, starty, cols, rows):
        # temporary instance to access class variables
        self.mobs = []
        self.advance_frames = 0
        self.moveframe = 0
        temp = Mob(0, 0)
        for c in range(cols):
            for r in range(rows):
                x = startx + c * (temp.rect.width + temp.rect.width / 2)
                y = starty + r * (temp.rect.height + temp.rect.height / 2)
                self.mobs.append(Mob(x, y))
        del temp

    def update(self):
        self.moveframe += 1
        # only move half the time
        if self.moveframe % 2 == 0:
            if self.advance_frames > 0:
                for m in self.mobs:
                    m.rect.y += abs(m.speed)
                self.advance_frames -= 1
            else:
                for m in self.mobs:
                    m.rect.x += m.speed
                for m in self.mobs:
                    if m.rect.right >= WIDTH or m.rect.left <= 0:
                        for M in self.mobs:
                            M.speed *= -1
                        self.advance_frames = 10
