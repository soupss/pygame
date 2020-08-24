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
        self.backscreen = pg.display.set_mode((0, 0), flags=pg.FULLSCREEN)
        self.backscreen.fill(BACKSCREEN_COLOR)
        self.screen = pg.Surface((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        pg.display.toggle_fullscreen()
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()
        self.GAMESCREEN_POS = ((pg.display.Info().current_w - WIDTH) / 2, (pg.display.Info().current_h - HEIGHT) / 2)
        self.score = 0


    def load_data(self):
        self.spritesheet = SpriteSheet(path.join(IMAGE_DIR, SPRITESHEET_NAME))
        self.sound_controller = SoundController(SOUND_NAMES)


    def new(self):
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
        player_hit_mobs = pg.sprite.spritecollide(self.player.sprite, self.mobs, True)
        player_hit_mob_bullets = pg.sprite.spritecollide(self.player.sprite, self.mob_bullets, True)
        if player_hit_mobs or player_hit_mob_bullets:
            self.player.sprite.die()
            for bullet in self.bullets:
                bullet.kill()
        # check if player bullets hit mobs
        player_bullets_hit_mobs = pg.sprite.groupcollide(self.player_bullets, self.mobs, True, True)
        for mobs in player_bullets_hit_mobs.values():
            for mob in mobs:
                Explosion(self, mob.rect.center)
                self.score += mob.type * 10
                self.sound_controller.effects['score'].play()
        # check if player bullets hit mob bullets
        player_bullets_hit_mob_bullets = pg.sprite.groupcollide(self.player_bullets, self.mob_bullets, True, True)
        for mob_bullets in player_bullets_hit_mob_bullets.values():
            for bullet in mob_bullets:
                Explosion(self, bullet.rect.center, True)
        # check if something hit bunkers
        bunkers_hit_bullets = pg.sprite.groupcollide(self.bunkers, self.bullets, False, True)
        bunkers_hit_mobs = pg.sprite.groupcollide(self.bunkers, self.mobs, True, False)
        if bunkers_hit_mobs:
            self.sound_controller.effects['explosion'].play()
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
        pg.draw.line(self.screen, WHITE, (0, HEIGHT - BOT_SPACING), (WIDTH, HEIGHT - BOT_SPACING), 2)
        pg.draw.line(self.screen, WHITE, (0, TOP_SPACING), (WIDTH, TOP_SPACING), 2)
        self.player.sprite.draw_lives(self.screen)
        # display score
        text(self.screen, 'SCORE', SCORE_TEXT_SIZE, (WIDTH / 3, SCORE_LABEL_Y))
        text(self.screen, style_numbers(self.score), SCORE_TEXT_SIZE, (WIDTH / 3, SCORE_VALUE_Y))
        text(self.screen, 'HI-SCORE', SCORE_TEXT_SIZE, (WIDTH / 1.5, SCORE_LABEL_Y))
        # text(self.screen, style_numbers(99999), SCORE_TEXT_SIZE, (WIDTH / 1.5, SCORE_VALUE_Y))
        self.backscreen.blit(self.screen, self.GAMESCREEN_POS)
        pg.display.flip()


    def start_screen(self):
        pass


    def gameover_screen(self):
        pass


    def quit(self):
        self.playing = False
        self.running = False
