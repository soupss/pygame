'''
Space Invaders clone
'''
import pygame
from os import path

# constants
WIDTH = 224 * 3
HEIGHT = 256 * 3
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BASE_DIR = path.join(path.dirname(__file__))

# pygame initialization
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()

font_name = pygame.font.match_font('consolas')
def draw_text(text, size, pos, color=WHITE):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = pos
    screen.blit(text_surface, text_rect)

# uses vars above this
from sprites.player import Player
from sprites.mob import MobPack
from sprites.wall import Wall

# prepare sprites and groups
sprites = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
walls = pygame.sprite.Group()

player = Player()
sprites.add(player)

temp = Wall((0, 0))
for i in range(1, 4 + 1):
    spacing = WIDTH / 5 + 20
    offset = (WIDTH - (temp.rect.w * 4 + spacing * 3)) / 2
    wall = Wall((offset + i*spacing, HEIGHT - 180))
    wall.add(sprites, walls)
del temp

mob_pack = MobPack(30, 150, 11, 5)
for mob in mob_pack.mobs:
    sprites.add(mob)


score = 0
lives = 3

# game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    # dynamic sprite groups
    for bullet in player.bullets:
        bullet.add(sprites, all_bullets)
    for bullet in mob_pack.bullets:
        bullet.add(sprites, all_bullets)

    # logic
    if len(mob_pack.mobs) == 0:
        print('win')
        running = False
    elif lives <= 0:
        print('lose')
        running = False

    # player shoots mobs
    player_bullets_hit_mobs = pygame.sprite.groupcollide(player.bullets, mob_pack.mobs, True, True)

    for hit in player_bullets_hit_mobs:
        score += 10

    # wall collision
    player_bullets_hit_walls = pygame.sprite.groupcollide(walls, player.bullets, False, True)
    mob_bullets_hit_walls = pygame.sprite.groupcollide(walls, mob_pack.bullets, False, True)
    for wall in mob_bullets_hit_walls:
        wall.hit()
    for wall in player_bullets_hit_walls:
        wall.hit()

    # things hit player
    mob_bullets_hit_player = pygame.sprite.spritecollide(player, mob_pack.bullets, True)
    mobs_hit_player = pygame.sprite.spritecollide(player, mob_pack.mobs, True)
    if mob_bullets_hit_player or mobs_hit_player:
        lives -= 1

    # update
    sprites.update()
    mob_pack.update()

    # render
    screen.fill(BLUE)
    sprites.draw(screen)
    score_size = 25
    score_offset = 25
    score_spacing = 30
    draw_text('score', score_size, (WIDTH / 3, score_offset))
    draw_text(str(score), score_size, (WIDTH / 3, score_offset + score_spacing))
    draw_text('hi-score', score_size, (WIDTH / 1.5, score_offset))
    draw_text(str(0), score_size, (WIDTH / 1.5, score_offset + score_spacing))

    draw_text(str(lives), 30, (WIDTH / 8, HEIGHT - 30))
    pygame.display.flip()

pygame.quit()
