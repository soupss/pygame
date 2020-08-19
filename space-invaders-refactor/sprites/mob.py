import pygame
import random
from __main__ import WIDTH, HEIGHT, RED
from sprites import IMG
from sprites.bullet import EnemyBullet as Bullet


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMG.ALIENS[f'{type}']
        self.rect = self.image.get_rect()
        self.basespeed = 1
        self.speed = self.basespeed
        self.dir = 1
        self.rect.x = x
        self.rect.y = y
        self.bullets = pygame.sprite.Group()

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom)
        self.bullets.add(bullet)
        return bullet

class MobPack():
    def __init__(self, startx, starty, cols, rows):
        self.mobs = pygame.sprite.Group()
        self.cols = cols
        self.rows = rows
        # array containing groups of mobs - used to see if mob is at the bottom
        self.colgroups = []
        for _ in range(cols):
            self.colgroups.append(pygame.sprite.Group())
        self.advance_frames = 0
        self.bullets = pygame.sprite.Group()
        self.SHOOT_DELAY = 1500
        self.last_shot_time = pygame.time.get_ticks() - self.SHOOT_DELAY
        # temporary instance to access class variables
        temp = Mob(0, 0, 1)
        for col in range(cols):
            for row in range(rows):
                x = startx + col * (temp.rect.width + temp.rect.width / 2)
                y = starty + row * (temp.rect.height + temp.rect.height / 2)
                mob = Mob(x, y, 1)
                self.mobs.add(mob)
                self.colgroups[col].add(mob)
        del temp

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.SHOOT_DELAY:
            valid_shooters = []
            for cg in self.colgroups:
                if not cg:
                    del cg
                    continue
                valid_shooters.append(cg.sprites()[-1])  # the last shooter in a col group is always at the bottom
            selected_shooter = valid_shooters[random.randrange(len(valid_shooters))]
            self.bullets.add(selected_shooter.shoot())
            self.last_shot_time = current_time

    def get_speed_multiplier(self, mobs):
        # multiply speed incrementally when mobs die
        # max mobs = 55 = 11x5
        if mobs <= 5:
            return 2.8
        elif mobs <= 10:
            return 2.4
        elif mobs <= 15:
            return 2.10
        elif mobs <= 20:
            return 1.85
        elif mobs <= 25:
            return 1.7
        elif mobs <= 30:
            return 1.55
        elif mobs <= 35:
            return 1.4
        elif mobs <= 40:
            return 1.3
        elif mobs <= 45:
            return 1.2
        elif mobs <= 50:
            return 1.1
        else:
            return 1

    def update(self):
        self.shoot()
        # edge hit
        for m in self.mobs:
            if m.rect.right >= WIDTH:
                for M in self.mobs:
                    M.dir = -1
                self.advance_frames = 10
            if m.rect.left <= 0:
                for M in self.mobs:
                    M.dir = 1
                self.advance_frames = 10
        # movement
        for m in self.mobs:
            m.speed = m.basespeed * self.get_speed_multiplier(len(self.mobs))
            m.rect.x += m.speed * m.dir
        if self.advance_frames > 0:
            for m in self.mobs:
                m.rect.y += m.speed
            self.advance_frames -= 1
