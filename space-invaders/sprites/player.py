import pygame as pg
from settings import *
from sprites.bullet import PlayerBullet as Bullet


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.groups = self.game.sprites, self.game.player
        pg.sprite.Sprite.__init__(self, self.groups)
        self.load_images()
        self.frame = 0
        self.image = self.frame_alive
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(WIDTH / 2, PLAYER_Y))
        self.last_shot = pg.time.get_ticks() - PLAYER_SHOOT_DELAY
        self.lives = PLAYER_STARTING_LIVES
        self.respawning = False
        self.last_updated = pg.time.get_ticks()

    def load_images(self):
        self.frame_alive = self.game.spritesheet.get_image(0, 0, 60, 32, GREEN)
        self.frames_exploded = [
            self.game.spritesheet.get_image(0, 32, 60, 32, GREEN),
            self.game.spritesheet.get_image(60, 32, 60, 32, GREEN)
        ]


    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > PLAYER_SHOOT_DELAY:
            self.last_shot = now
            Bullet(self.game, self.rect.centerx, self.rect.top)
            self.game.sound_controller.play_effect('shoot')

    def die(self):
        self.lives -= 1
        self.time_died = pg.time.get_ticks()
        self.respawning = True
        self.game.sound_controller.play_effect('die')

    def draw_lives(self, screen):
        image_small = pg.transform.scale(self.frame_alive, (45, 25))
        offset = (BOT_SPACING - image_small.get_height()) / 2
        spacing = image_small.get_width() + 15
        for life in range(self.lives):
            screen.blit(image_small, image_small.get_rect(left=life * spacing + offset, bottom=HEIGHT-offset))


    def update(self):
        if self.respawning:
            now = pg.time.get_ticks()
            if now - self.time_died > PLAYER_RESPAWN_RATE:
                self.rect.centerx = WIDTH / 2
                self.image = self.frame_alive
                self.respawning = False
            elif now - self.time_died > PLAYER_RESPAWN_RATE / 3:
                self.image = pg.Surface((self.rect.size), pg.SRCALPHA)
                self.image = self.image.convert_alpha()
            else:
                # update exploded frame
                if now - self.last_updated > PLAYER_EXPLODE_FRAME_RATE:
                    self.frame += 1
                    if self.frame == len(self.frames_exploded):
                        self.frame = 0
                    self.image = self.frames_exploded[self.frame]
                    self.last_updated = now
        else:
            self.speedx = 0
            keys = pg.key.get_pressed()
            if keys[pg.K_h] or keys[pg.K_LEFT]:
                self.speedx = -PLAYER_SPEED
            if keys[pg.K_l] or keys[pg.K_RIGHT]:
                self.speedx = PLAYER_SPEED
            if keys[pg.K_z] or keys[pg.K_SPACE]:
                self.shoot()
            self.rect.x += self.speedx
            if self.rect.right >= WIDTH:
                self.rect.right = WIDTH
            elif self.rect.left <= 0:
                self.rect.left = 0
