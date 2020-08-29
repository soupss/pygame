import pygame as pg
from game import Game

game = Game()
game.start_screen()
while game.running:
    game.new()
    game.gameover_screen()
pg.quit()
