import pygame
from __main__ import GREEN
from tools import IMG

PURPLE = pygame.Color(255, 0, 255)

class Bunker(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMG.get('bunker', GREEN)
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)

    def dent(self, surf, rect):
        proj_surf = surf.copy()
        proj_surf.fill((0,0,0))
        proj_rect = proj_surf.get_rect(center = rect.center)
        self.image.set_colorkey(PURPLE)
        self.image.blit(proj_surf, (proj_rect.x - self.rect.x, proj_rect.y - self.rect.y))
                         # ,special_flags= pygame.BLEND_RGBA_SUB)
