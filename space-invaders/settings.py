'''This module contains global constants.'''
from os import path
import pygame as pg
from pygame.math import Vector2

# game properties
TITLE = 'Space Invaders'
FPS = 60
SPRITESHEET_NAME = 'spritesheet.png'
FONT_NAME = 'bpdots.unicasesquare-bold.otf'
PRE_WAVE_TIME = 3000

# screen and game field properties
WIDTH = 224 * 4  # 896
HEIGHT = 256 * 4  # 1024
WIDTH_SCALED = 224 * 3  # 672
HEIGHT_SCALED = 256 * 3  # 768
TOP_SPACING = 150
BOT_SPACING = 60
FIELD = pg.Rect(0, TOP_SPACING, WIDTH, HEIGHT - BOT_SPACING - TOP_SPACING)
SCORE_LABEL_Y = TOP_SPACING / 3
SCORE_VALUE_Y = TOP_SPACING / 1.5
SCORE_TEXT_SIZE = 35

# player properties
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 32
PLAYER_Y = HEIGHT - BOT_SPACING - PLAYER_HEIGHT / 2 - 20
PLAYER_SPEED = 5
PLAYER_SHOOT_DELAY = 750
PLAYER_BULLET_SPEED = 16
PLAYER_BULLET_HEIGHT = 16
PLAYER_STARTING_LIVES = 3
PLAYER_RESPAWN_RATE = 3000
PLAYER_EXPLODE_FRAME_RATE = 100

# mob properties
MOB_WIDTH = 44  # base mob is alien 2
MOB_HEIGHT = 32
MOB_ADVANCE_FRAMES = 13
MOB_PACK_COLS = 11
MOB_PACK_ROWS = 5
MOB_BULLET_FRAME_RATE = 60
MOB_BULLET_SPEED = 6
MOB_BULLET_HEIGHT = 28
MOB_START_Y = TOP_SPACING + MOB_HEIGHT / 2 + 20

# mob scaling
# scales with enemy deaths
# mob base speed is increased by 30% each level
# mob speed scale is multiplied by mob deaths and added to base speed
MOB_BASE_SPEED = .2
MOB_SPEED_SCALE = .1
MOB_SPEED_SCALE_EXP = 1.06
# mob framerate increases with mob speed
MOB_BASE_FRAMERATE = 1100
MOB_FRAMERATE_SCALE = .2
MOB_BASE_SHOOT_DELAY = 1500

# bunker properties
BUNKER_WIDTH = 88
BUNKER_HEIGHT = 64
BUNKER_Y = PLAYER_Y - PLAYER_HEIGHT / 2 - BUNKER_HEIGHT - 20

# explosion properties
EXPLOSION_TIME = 300

# music
DUNDUN_RATE = MOB_BASE_FRAMERATE

# resource directories
BASE_DIR = path.join(path.dirname(__file__))
IMAGE_DIR = path.join(BASE_DIR, path.join('assets', 'images'))
FONT_DIR = path.join(BASE_DIR, path.join('assets', 'fonts'))
SOUND_DIR = path.join(BASE_DIR, path.join('assets', 'sounds'))

# colors
BLACK = pg.Color(0, 0, 0)
WHITE = pg.Color(255, 255, 255)
RED = pg.Color(255, 0, 0)
GREEN = pg.Color(0, 255, 0)
BLUE = pg.Color(0, 0, 255)
MAGENTA = pg.Color(255, 0, 255)
DARKGREY = pg.Color(15, 15, 15)
BACKSCREEN_COLOR = DARKGREY
BACKGROUND_COLOR = BLACK

# sound effects
SOUND_NAMES = [
        'shoot', 'score', 'die', 'select', 'select2', 'explosion', 'dun', 'dun2'
]
