'''
This module contains resource loading functions
Also contains general tools which don't belong anywhere else
'''
# art made with https://www.piskelapp.com/
# sound made with https://www.bfxr.net/
from os import path
from random import randrange
import pygame as pg
from settings import *
from sprites.mob import Mob


def text(screen, text, size, pos, color=WHITE):
    font = pg.font.Font(path.join(FONT_DIR, FONT_NAME), size)
    text_surface = font.render(text, False, color)
    text_rect = text_surface.get_rect(center=pos)
    screen.blit(text_surface, text_rect)
    return text_surface


def style_numbers(int):
    string = str(int)
    if len(string) != 5:
        if len(string) == 1:
            string = '0000' + string
        if len(string) == 2:
            string = '000' + string
        if len(string) == 3:
            string = '00' + string
        if len(string) == 4:
            string = '0' + string
    return string


class Menu:
    '''Creates a menu from given labels and functions.

    example dict:
        menu_dict = {
            'play': None,
            'options': self.options,
            'quit': self.quit
        }
    '''
    def __init__(self, game, dict, text_size, start_y):
        self.game = game
        self.waiting = True
        self.dict = dict
        self.options = list(self.dict.keys())
        self.selected = 0
        self.text_size = text_size
        self.start_y = start_y
        Mob.load_images(self, GREEN)
        self.icons = self.images[randrange(len(self.images))]
        self.icon = self.icons[0]

    def select_next(self):
        self.selected += 1
        if self.selected == len(self.dict):
            self.selected = 0

    def select_prev(self):
        self.selected -= 1
        if self.selected < 0:
            self.selected = len(self.dict) - 1

    def events(self):
        self.game.clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q or event.key == pg.K_ESCAPE:
                    self.waiting = False
                    self.game.quit()
                if event.key == pg.K_j or event.key == pg.K_DOWN:
                    self.select_next()
                    self.game.sound_controller.play_effect('select')
                if event.key == pg.K_k or event.key == pg.K_UP:
                    self.select_prev()
                    self.game.sound_controller.play_effect('select')
                if event.key == pg.K_RETURN:
                    self.icon = self.icons[1]
                    self.game.sound_controller.play_effect('select2')
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN:
                    # call dict value function if it isnt set to None
                    if self.dict[self.options[self.selected]]:
                        # exit menu when option selected
                        self.waiting = False
                        self.dict[self.options[self.selected]]()

    def update(self):
        self.events()

    def draw(self, screen):
        spacing = 100
        for i, (label, action) in enumerate(self.dict.items()):
            if i == self.selected:
                text_surf = text(screen, label, self.text_size, (WIDTH / 2, i * spacing + self.start_y), GREEN)
                screen.blit(self.icon, (WIDTH / 2 - text_surf.get_width() / 2 - 70, i * spacing + self.start_y - self.icon.get_height() / 3 + 5))
            else:
                text(screen, label, self.text_size, (WIDTH / 2, i * spacing + self.start_y), WHITE)


class SpriteSheet:
    '''Utility class for loading and parsing spritesheets.'''
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height, color):
        '''Change color and return a single image.'''
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        color_image = pg.Surface(image.get_size()).convert_alpha()
        color_image.fill(color)
        image.blit(color_image, (0,0), special_flags = pg.BLEND_RGBA_MIN)
        image.set_colorkey(BLACK)
        return image


class SoundController:
    '''Utility class for loading and controlling sounds.'''
    def __init__(self, sound_name_list):
        self.effects = {}
        self.last_dun = pg.time.get_ticks()
        self.dun_count = 0
        self.dundun_rate = DUNDUN_RATE
        for sound_name in sound_name_list:
            self.effects[sound_name] = pg.mixer.Sound(path.join(SOUND_DIR, sound_name+'.ogg'))
            self.effects[sound_name].set_volume(.5)

    def play_effect(self, effect):
        self.effects[effect].play()

    def music(self):
        now = pg.time.get_ticks()
        if now - self.last_dun > self.dundun_rate:
            if self.dun_count == 0:
                self.effects['dun2'].play()
            else:
                self.effects['dun'].play()
            self.dun_count += 1
            if self.dun_count > 3:
                self.dun_count = 0
            self.last_dun = now
