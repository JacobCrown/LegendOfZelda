import pygame
from settings import *

import common.constants as c

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        image_path = c.PROJECT_DIRPATH / 'graphics/test/player.png'
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
