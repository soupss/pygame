import pygame
'''
Space Invaders clone
'''

# constants
WIDTH = 800
HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# uses constants so imported after
from sprites.player import Player

# pygame initialization
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()


# prepare sprites and groups
sprites = pygame.sprite.Group()

player = Player()
sprites.add(player)

# game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update
    sprites.update()

    # render
    screen.fill(BLACK)
    sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
