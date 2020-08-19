import pygame
import random
from __main__ import WIDTH, HEIGHT, RED
from sprites import IMG
from sprites.bullet import EnemyBullet as Bullet


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, type, row=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMG.ALIENS[f'{type}']
        self.rect = self.image.get_rect()
        self.speed = 1
        self.dir = 1
        self.rect.x = x
        self.rect.y = y
        self.bullets = pygame.sprite.Group()
        self.row = row

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom)
        self.bullets.add(bullet)
        return bullet

class MobPack():
    def __init__(self, startx, starty, cols, rows):
        # temporary instance to access class variables
        self.mobs = pygame.sprite.Group()
        self.colgroups = []
        # one group for each column
        for _ in range(cols):
            self.colgroups.append(pygame.sprite.Group())
        self.advance_frames = 0
        self.moveframe = 0
        self.bullets = pygame.sprite.Group()
        self.SHOOT_DELAY = 1000
        self.last_shot_time = pygame.time.get_ticks() - self.SHOOT_DELAY
        temp = Mob(0, 0, 1)
        for col in range(cols):
            for row in range(rows):
                x = startx + col * (temp.rect.width + temp.rect.width / 2)
                y = starty + row * (temp.rect.height + temp.rect.height / 2)
                mob = Mob(x, y, 1, row)
                self.mobs.add(mob)
                self.colgroups[col].add(mob)
        del temp

    def get_speed_multiplier(self):
        pass

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.SHOOT_DELAY:
            valid_shooter = False
            while not valid_shooter:
                selected_enemy = random.choice(self.mobs.sprites())
                for col in self.colgroups:
                    if selected_enemy in col.sprites():
                        if selected_enemy.row + 1 == len(col.sprites()):
                            valid_shooter = True
            self.bullets.add(selected_enemy.shoot())
            self.last_shot_time = current_time

    def update(self):
        self.shoot()
        self.moveframe += 1
        # only move half the time
        if self.moveframe % 2 == 0:
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
                m.rect.x += m.speed * m.dir
            if self.advance_frames > 0:
                for m in self.mobs:
                    m.rect.y += abs(m.speed)
                self.advance_frames -= 1
