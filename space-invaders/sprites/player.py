import pygame
from pygame.math import Vector2
from __main__ import WIDTH, HEIGHT, GREEN, screen
from tools import IMG, SND
from sprites.bullet import PlayerBullet as Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_base = IMG.get('ship', GREEN)
        self.image = self.image_base
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 80
        self.mask = pygame.mask.from_surface(self.image)
        self.speedx = 0
        self.lives = 3
        self.bullets = pygame.sprite.Group()
        self.SHOOT_DELAY = 500
        self.last_shot_time = pygame.time.get_ticks() - self.SHOOT_DELAY
        self.respawning = False
        self.death_time = pygame.time.get_ticks()
        self.respawn_timer = 1500  # time

    def shoot(self):
        SND.sounds['shoot'].play()
        self.bullets.add(Bullet(self.rect.centerx, self.rect.top))

    def die(self, time_died):
        SND.sounds['die'].play()
        self.lives -= 1
        self.respawning = True
        self.death_time = pygame.time.get_ticks()

    def draw_lives(self):
        offset = Vector2(250, 30)
        spacing = 55
        heart_image = self.image_base
        for l in range(self.lives - 1):
            screen.blit(heart_image, heart_image.get_rect(center = (l * spacing + offset.x, HEIGHT - offset.y)))

    def update(self):
        if self.respawning:
            self.image = pygame.Surface((self.rect.size), pygame.SRCALPHA)
            self.image = self.image.convert_alpha()
            current_time = pygame.time.get_ticks()
            if current_time - self.death_time > self.respawn_timer:
                self.image = self.image_base
                self.rect.centerx = WIDTH / 2
                self.respawning = False
        else:
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
