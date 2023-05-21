import random

import pygame

from tile import Tile
from settings import *
from player import Player
import common.constants as c
from common.helpers import import_csv_layout, import_folder
from common.enums import SpriteType, LayoutType

class Level:
    player: Player

    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout(c.PROJECT_DIRPATH / 'map/map_FloorBlocks.csv'),
            'grass': import_csv_layout(c.PROJECT_DIRPATH / 'map/map_Grass.csv'),
            'object': import_csv_layout(c.PROJECT_DIRPATH / 'map/map_Objects.csv'),
        }
        graphics = {
            'grass': import_folder(c.PROJECT_DIRPATH / 'graphics/Grass')
        }

        for style, layout in layouts.items():
            for row_idx, row in enumerate(layout):
                for col_idx, col in enumerate(row):
                    if col != LayoutType.NOTHING.value:
                        x = col_idx * TILESIZE
                        y = row_idx * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], SpriteType.INVISIBLE)
                        if style == 'grass':
                            rand_surface = random.choice(graphics['grass']).convert_alpha()
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], SpriteType.GRASS, surface=rand_surface)
                        if style == 'object':
                            pass
                    
        self.player = Player((2000, 1500), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # create the floor 
        self.floor_surface = pygame.image.load(c.PROJECT_DIRPATH / 'graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # displaying the sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
