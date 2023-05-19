import pygame

from tile import Tile
from settings import *
from player import Player

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        for row_idx, row in enumerate(WORLD_MAP):
            for col_idx, col in enumerate(row):
                x = col_idx * TILESIZE
                y = row_idx * TILESIZE
                if col == "x":
                    Tile((x,y), [self.visible_sprites, self.obstacle_sprites])
                elif col == "p":
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)

                    
    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()