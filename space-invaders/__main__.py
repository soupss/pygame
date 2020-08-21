'''
Space Invaders clone
'''
import pygame
from pygame.math import Vector2
from os import path

# constants
# sprites are scaled to 300%
# 12x8 = 36x24
WIDTH = 224 * 3
HEIGHT = 256 * 3
FIELD = Vector2(WIDTH, HEIGHT - 55)
FPS = 60

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
YELLOW = pygame.Color(255, 255, 0)

BASE_DIR = path.join(path.dirname(__file__))

# pygame initialization
pygame.mixer.pre_init(44100, -16, 1, 512)
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
from init import SND
from sprites.player import Player
from sprites.mob import MobPack
from sprites.bunker import Bunker

# prepare sprites and groups
sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bunkers = pygame.sprite.Group()

player = Player()
sprites.add(player)

temp = Bunker((0, 0))
for i in range(4):
    spacing = WIDTH / 5
    offset = (WIDTH - (temp.rect.w * 4 + (spacing - temp.rect.w )* 3)) / 2
    bunker = Bunker((offset + spacing * i, HEIGHT - 180))
    bunker.add(sprites, bunkers)
del temp

mob_pack = MobPack(30, 150, 11, 5)
for mob in mob_pack.mobs:
    sprites.add(mob)


score = 0
invaded = False

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
            if event.key == pygame.K_UP:
                SND.volume_up()
            if event.key == pygame.K_DOWN:
                SND.volume_down()

    # dynamic sprite groups
    for bullet in player.bullets:
        bullet.add(sprites, bullets)
    for bullet in mob_pack.bullets:
        bullet.add(sprites, bullets)

    # logic
    for mob in mob_pack.mobs:
        if mob.rect.bottom > FIELD.y:
            invaded = True
    if len(mob_pack.mobs) == 0:
        print('win')
        running = False
    elif player.lives <= 0 or invaded:
        print('lose')
        running = False

    # player shoots mobs
    player_bullets_hit_mobs = pygame.sprite.groupcollide(mob_pack.mobs, player.bullets, True, True, pygame.sprite.collide_mask)
    for mob in player_bullets_hit_mobs:
        SND.sounds['score'].play()
        score += mob.type * 10

    # bunker collision
    player_bullets_hit_bunkers = pygame.sprite.groupcollide(bunkers, player.bullets, False, True, pygame.sprite.collide_mask)
    mob_bullets_hit_bunkers = pygame.sprite.groupcollide(bunkers, mob_pack.bullets, False, True, pygame.sprite.collide_mask)
    mobs_hit_bunkers = pygame.sprite.groupcollide(bunkers, mob_pack.mobs, True, False, pygame.sprite.collide_mask)
    for mobs in mobs_hit_bunkers.values():
        mobs[0].kill()
        SND.sounds['explosion'].play()

    # things hit player
    mob_bullets_hit_player = pygame.sprite.spritecollide(player, mob_pack.bullets, True, pygame.sprite.collide_mask)
    mobs_hit_player = pygame.sprite.spritecollide(player, mob_pack.mobs, True, pygame.sprite.collide_mask)
    if mob_bullets_hit_player or mobs_hit_player:
        player.die(pygame.time.get_ticks())
        for bullet in bullets:
            bullet.kill()

    # update
    if player.respawning:
        player.update()
    else:
        sprites.update()
        mob_pack.update()

    # render
    screen.fill(BLACK)
    pygame.draw.line(screen, GREEN, (0, int(FIELD.y)), (WIDTH, int(FIELD.y)), 2)
    sprites.draw(screen)
    player.draw_lives()
    score_size = 25
    score_offset = 25
    score_spacing = 30
    draw_text('score', score_size, (int(WIDTH / 3), score_offset))
    draw_text(str(score), score_size, (int(WIDTH / 3), score_offset + score_spacing))
    draw_text('hi-score', score_size, (int(WIDTH / 1.5), score_offset))
    draw_text(str(0), score_size, (int(WIDTH / 1.5), score_offset + score_spacing))
    draw_text('extra lives', 20, (70, HEIGHT - 30))
    pygame.display.flip()

pygame.quit()
