import os
from os import path
import pygame as pg
from settings import *
from tools import SpriteSheet, Menu, SoundController, text, style_numbers
from sprites.player import Player
from sprites.mob import MobGroup, Mob
from sprites.bunker import Bunker
from sprites.explosion import Explosion


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 512)
        pg.init()
        MONITOR_SIZE = Vector2(pg.display.Info().current_w, pg.display.Info().current_h)
        self.screen = pg.Surface((WIDTH, HEIGHT))
        # use scaled screen if window is too big
        if HEIGHT > MONITOR_SIZE.y:
            self.scale_screen = True
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (MONITOR_SIZE.x / 2 - WIDTH_SCALED / 2, MONITOR_SIZE.y / 2 - HEIGHT_SCALED / 2 + 10)
            self.screen_scaled = pg.display.set_mode((WIDTH_SCALED, HEIGHT_SCALED))
        else:
            self.scale_screen = False
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (MONITOR_SIZE.x / 2 - WIDTH / 2, MONITOR_SIZE.y / 2 - HEIGHT / 2 + 10)
            self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.mouse.set_visible(False)
        self.load_data()
        self.running = True


    def load_data(self):
        self.spritesheet = SpriteSheet(path.join(IMAGE_DIR, SPRITESHEET_NAME))
        self.sound_controller = SoundController(SOUND_NAMES)


    def new(self):
        self.score = 0
        self.level = 0
        self.pre_wave_begin = None
        self.sprites = pg.sprite.Group()  # all sprites
        self.player = pg.sprite.GroupSingle()
        self.mobs = MobGroup(self)  # spritegroup sub class
        self.bunkers = pg.sprite.Group()
        self.bullets = pg.sprite.Group()  # all bullets
        self.player_bullets = pg.sprite.Group()
        self.mob_bullets = pg.sprite.Group()
        Player(self)
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
            if not self.mobs:
                self.wave(self.level)
            self.update()
            self.draw()


    def wave(self, level):
        self.pre_wave = True
        if self.pre_wave_begin == None:
            self.level += 1
            self.pre_wave_begin = pg.time.get_ticks()
        if self.pre_wave:
            now = pg.time.get_ticks()
            if now - self.pre_wave_begin > PRE_WAVE_TIME:
                self.pre_wave = False
                self.pre_wave_begin = None
        if not self.pre_wave:
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


    def update(self):
        # freeze when player is respawning
        if self.player.sprite.respawning:
            self.player.update()
            self.mobs.last_shot = pg.time.get_ticks()
            self.sound_controller.dun_count = 0
        else:
            # lose check
            for mob in self.mobs:
                if mob.rect.y > HEIGHT - BOT_SPACING:
                    self.playing = False
            if self.player.sprite.lives == 0:
                self.playing = False
            if not self.pre_wave:
                self.sound_controller.music()
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
        self.show_game_data()
        if self.scale_screen:
            pg.transform.scale(self.screen, (WIDTH_SCALED, HEIGHT_SCALED), self.screen_scaled)
        pg.display.flip()


    def show_game_data(self):
        if self.pre_wave:
            text(self.screen, f'LEVEL {self.level}', 45, (WIDTH / 2, HEIGHT / 2))
        pg.draw.line(self.screen, WHITE, (0, TOP_SPACING), (WIDTH, TOP_SPACING), 3)
        pg.draw.line(self.screen, GREEN, (0, HEIGHT - BOT_SPACING), (WIDTH, HEIGHT - BOT_SPACING), 3)
        self.player.sprite.draw_lives(self.screen)
        text(self.screen, 'SCORE', SCORE_TEXT_SIZE, (WIDTH / 3, SCORE_LABEL_Y))
        text(self.screen, str(self.score), SCORE_TEXT_SIZE, (WIDTH / 3, SCORE_VALUE_Y))
        text(self.screen, 'LEVEL', SCORE_TEXT_SIZE, (WIDTH / 1.5, SCORE_LABEL_Y))
        text(self.screen, str(self.level), SCORE_TEXT_SIZE, (WIDTH / 1.5, SCORE_VALUE_Y))


    def start_screen(self):
        def play():
            pass
        def quit():
            self.quit()
        start_menu_dict = {
            'PLAY': play,
            'QUIT': quit
        }
        start_menu = Menu(self, start_menu_dict, 50, HEIGHT / 2)
        while start_menu.waiting and self.running:
            start_menu.update()
            self.screen.fill(BACKGROUND_COLOR)
            text(self.screen, 'SPACE', 160, (WIDTH / 2, HEIGHT / 4))
            text(self.screen, 'INVADERS', 100, (WIDTH / 2, HEIGHT / 4 + 80))
            start_menu.draw(self.screen)


    def gameover_screen(self):
        def play_again():
            pass
        def quit():
            self.quit()
        gameover_menu_dict = {
            'PLAY AGAIN': play_again,
            'QUIT': quit
        }
        gameover_menu = Menu(self, gameover_menu_dict, 50, HEIGHT / 2)
        while gameover_menu.waiting and self.running:
            gameover_menu.update()
            self.screen.fill(BACKGROUND_COLOR)
            text(self.screen, 'GAME OVER', 85, (WIDTH / 2, HEIGHT / 4 - 10))
            text(self.screen, f'SCORE {style_numbers(self.score)}', 50, (WIDTH / 2, HEIGHT / 3))
            gameover_menu.draw(self.screen)


    def quit(self):
        self.playing = False
        self.running = False
