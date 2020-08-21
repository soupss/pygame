# art made with https://www.piskelapp.com/
# sound made with https://www.bfxr.net/
from os import path
import pygame
from __main__ import BASE_DIR

IMG_DIR = path.join(BASE_DIR, path.join('assets', 'img'))
SND_DIR = path.join(BASE_DIR, path.join('assets', 'snd'))

def style_numbers(int):
    s = str(int)
    l = len(s)
    if l != 5:
        if l == 1:
            s = '0000' + s
        if l == 2:
            s = '000' + s
        if l == 3:
            s = '00' + s
        if l == 4:
            s = '0' + s
    return s


class Images:
    def __init__(self, image_name_list):
        self.images = {}
        for image_name in image_name_list:
            self.images[image_name] = pygame.image.load(path.join(IMG_DIR, image_name+'.png'))

    def get(self, name, color):
        image = self.images[name]
        color_image = pygame.Surface(image.get_size()).convert_alpha()
        color_image.fill(color)
        image.blit(color_image, (0,0), special_flags = pygame.BLEND_RGBA_MIN)
        return image


class Sound:
    def __init__(self, sound_name_list):
        self.sounds = {}
        for sound_name in sound_name_list:
            self.sounds[sound_name] = pygame.mixer.Sound(path.join(SND_DIR, sound_name+'.ogg'))
            self.sounds[sound_name].set_volume(.5)

    def volume_up(self):
        for sound in self.sounds.values():
            sound.set_volume(sound.get_volume() + .1)

    def volume_down(self):
        for sound in self.sounds.values():
            sound.set_volume(sound.get_volume() - .1)


image_names = [
    'ship', 'bunker',
    'alien1', 'alien2', 'alien3',
    'player_bullet'
]

print('loading sprite image files...')
IMG = Images(image_names)
print('all sprite image files loaded')

sound_names = [
    'shoot', 'score', 'die',
    'select', 'select2', 'explosion'
]

print('loading sound files...')
SND = Sound(sound_names)
print('all sound files loaded')
