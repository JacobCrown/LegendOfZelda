import pygame

from settings import *
import common.constants as c
from common.enums import DirectionType

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        image_path = c.PROJECT_DIRPATH / 'graphics/test/player.png'
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        # Check for arrow key presses
        if keys[pygame.K_DOWN]:
            self.direction.y = 1
        elif keys[pygame.K_UP]:
            self.direction.y = -1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision(DirectionType.HORIZONTAL)
        self.hitbox.y += self.direction.y * speed
        self.collision(DirectionType.VERTICAL)
        self.rect.center = self.hitbox.center

    def _check_for_collision_horizontal(self):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.x > 0:
                    self.hitbox.right = sprite.hitbox.left
                elif self.direction.x < 0:
                    self.hitbox.left = sprite.hitbox.right

    def _check_for_collision_vertical(self):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.y > 0:
                    self.hitbox.bottom = sprite.hitbox.top
                elif self.direction.y < 0:
                    self.hitbox.top = sprite.hitbox.bottom
        
    def collision(self, direction: DirectionType):
        if direction == DirectionType.HORIZONTAL:
            self._check_for_collision_horizontal()
        elif direction == DirectionType.VERTICAL:
            self._check_for_collision_vertical()

    def update(self):
        self.input()
        self.move(self.speed)