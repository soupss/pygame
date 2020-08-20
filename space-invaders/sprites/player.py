import pygame
from __main__ import WIDTH, HEIGHT, GREEN
from sprites import IMG
from sprites.bullet import PlayerBullet as Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMG.PLAYER
        # self.image.fill((GREEN))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 80
        self.speedx = 0
        self.bullets = pygame.sprite.Group()
        self.SHOOT_DELAY = 500
        self.last_shot_time = pygame.time.get_ticks() - self.SHOOT_DELAY

    def shoot(self):
        self.bullets.add(Bullet(self.rect.centerx, self.rect.top))

    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_h]:
            self.speedx = -4
        if keys[pygame.K_l]:
            self.speedx = 4
        if keys[pygame.K_z]:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > self.SHOOT_DELAY:
                self.shoot()
                self.last_shot_time = current_time
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0
