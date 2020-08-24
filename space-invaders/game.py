import os
from os import path
import pygame as pg
from settings import *
from tools import SpriteSheet, SoundController, text, style_numbers
from sprites.player import Player
from sprites.mob import MobGroup, Mob
from sprites.bunker import Bunker
from sprites.explosion import Explosion


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 512)
        pg.init()
        # self.backscreen = pg.display.set_mode((0, 0), flags=pg.FULLSCREEN)
        # self.backscreen.fill(BACKSCREEN_COLOR)
        # self.screen = pg.Surface((WIDTH, HEIGHT))
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.GAMESCREEN_POS = ((pg.display.Info().current_w - WIDTH) / 2, (pg.display.Info().current_h - HEIGHT) / 2)
        self.running = True


    def load_data(self):
        self.spritesheet = SpriteSheet(path.join(IMAGE_DIR, SPRITESHEET_NAME))
        self.sound_controller = SoundController(SOUND_NAMES)


    def new(self):
        self.score = 0
        self.sprites = pg.sprite.Group()  # all sprites
        self.player = pg.sprite.GroupSingle()
        self.mobs = MobGroup()  # spritegroup sub class
        self.bunkers = pg.sprite.Group()
        self.bullets = pg.sprite.Group()  # all bullets
        self.player_bullets = pg.sprite.Group()
        self.mob_bullets = pg.sprite.Group()
        Player(self)
        # spawn mobs
        for col in range(self.mobs.cols):
            for row in range(self.mobs.rows):
                x = MOB_WIDTH * 1.5 * col + MOB_WIDTH
                y = MOB_HEIGHT * 1.5 * row + MOB_START_Y
                if row == 0:
                    mob = Mob(self, x, y, 3)
                if row == 1 or row == 2:
                    mob = Mob(self, x, y, 2)
                if row == 3 or row == 4:
                    mob = Mob(self, x, y, 1)
                self.mobs.colgroups[col].add(mob)
        # spawn bunkers
        for i in range(4):
            spacing = WIDTH / 5
            offset = (WIDTH - (BUNKER_WIDTH * 4 + (spacing - BUNKER_WIDTH) * 3)) / 2
            Bunker(self, i * spacing + offset, BUNKER_Y)
        self.run()


    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):
        for mob in self.mobs:
            if mob.rect.y > HEIGHT:
                self.playing = False
        if self.player.sprite.lives == 0:
            self.playing = False
        if self.player.sprite.respawning:
            self.player.update()
            self.mobs.last_shot = pg.time.get_ticks()
        else:
            self.sprites.update()
            self.mobs.update()
        # check if player gets hit by mobs or mob bullets
        player_hit_mobs = pg.sprite.spritecollide(self.player.sprite, self.mobs, True, pg.sprite.collide_mask)
        player_hit_mob_bullets = pg.sprite.spritecollide(self.player.sprite, self.mob_bullets, True, pg.sprite.collide_mask)
        if player_hit_mobs or player_hit_mob_bullets:
            self.player.sprite.die()
            for bullet in self.bullets:
                bullet.kill()
        # check if player bullets hit mobs
        player_bullets_hit_mobs = pg.sprite.groupcollide(self.player_bullets, self.mobs, True, True, pg.sprite.collide_mask)
        for mobs in player_bullets_hit_mobs.values():
            for mob in mobs:
                Explosion(self, mob.rect.center)
                self.score += mob.type * 10
                self.sound_controller.play_effect('score')
        # check if player bullets hit mob bullets
        player_bullets_hit_mob_bullets = pg.sprite.groupcollide(self.player_bullets, self.mob_bullets, True, True, pg.sprite.collide_mask)
        for mob_bullets in player_bullets_hit_mob_bullets.values():
            for bullet in mob_bullets:
                Explosion(self, bullet.rect.center, True)
        # check if something hit bunkers
        bunkers_hit_bullets = pg.sprite.groupcollide(self.bunkers, self.bullets, False, True, pg.sprite.collide_mask)
        bunkers_hit_mobs = pg.sprite.groupcollide(self.bunkers, self.mobs, True, False, pg.sprite.collide_mask)
        if bunkers_hit_mobs:
            self.sound_controller.play_effect('explosion')
        for mobs in bunkers_hit_mobs.values():
            mobs[0].kill()


    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    self.quit()


    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.sprites.draw(self.screen)
        pg.draw.line(self.screen, WHITE, (0, TOP_SPACING), (WIDTH, TOP_SPACING), 3)
        pg.draw.line(self.screen, GREEN, (0, HEIGHT - BOT_SPACING), (WIDTH, HEIGHT - BOT_SPACING), 3)
        self.player.sprite.draw_lives(self.screen)
        # display score
        text(self.screen, 'SCORE', SCORE_TEXT_SIZE, (WIDTH / 3, SCORE_LABEL_Y))
        text(self.screen, style_numbers(self.score), SCORE_TEXT_SIZE, (WIDTH / 3, SCORE_VALUE_Y))
        text(self.screen, 'HI-SCORE', SCORE_TEXT_SIZE, (WIDTH / 1.5, SCORE_LABEL_Y))
        # text(self.screen, style_numbers(99999), SCORE_TEXT_SIZE, (WIDTH / 1.5, SCORE_VALUE_Y))
        # self.backscreen.blit(self.screen, self.GAMESCREEN_POS)
        pg.display.flip()


    def start_screen(self):
        if not self.running:
            return
        self.screen.fill(BACKGROUND_COLOR)
        text(self.screen, 'SPACE', 160, (WIDTH / 2, HEIGHT / 4 - 40), GREEN)
        text(self.screen, 'INVADERS', 100, (WIDTH / 2, HEIGHT / 4 + 40), GREEN)
        alien1 = self.spritesheet.get_image(48, 128, 48, 32, WHITE)
        alien2 = self.spritesheet.get_image(48, 160, 44, 32, WHITE)
        alien3 = self.spritesheet.get_image(48, 192, 32, 32, WHITE)

        self.screen.blit(alien3, alien3.get_rect(center=(WIDTH/3 + 20, HEIGHT / 2 - 25)))
        text(self.screen, '= 30 POINTS', 40, (WIDTH / 2 + 40, HEIGHT / 2 - 25))

        self.screen.blit(alien2, alien2.get_rect(center=(WIDTH/3 + 20, HEIGHT / 2 + 25)))
        text(self.screen, '= 20 POINTS', 40, (WIDTH / 2 + 40, HEIGHT / 2 + 25))

        self.screen.blit(alien1, alien1.get_rect(center=(WIDTH/3 + 20, HEIGHT / 2 + 75)))
        text(self.screen, '= 10 POINTS', 40, (WIDTH / 2 + 40, HEIGHT / 2 + 75))

        text(self.screen, 'MOVE WITH ARROW KEYS', 30, (WIDTH / 2, HEIGHT * .75 - 30))
        text(self.screen, 'SHOOT WITH SPACE BAR', 30, (WIDTH / 2, HEIGHT * .75))
        text(self.screen, 'PRESS ANY KEY TO PLAY...', 30, (WIDTH / 2, HEIGHT * .75 + 30))

        # self.backscreen.blit(self.screen, self.GAMESCREEN_POS)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    self.sound_controller.play_effect('select')
                if event.type == pg.KEYUP:
                    self.sound_controller.play_effect('select2')
                    waiting = False


    def gameover_screen(self):
        pass


    def quit(self):
        self.playing = False
        self.running = False
