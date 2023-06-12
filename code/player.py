import os

import pygame

from settings import *
import common.constants as c
from common.enums import DirectionType, PlayerDirection, PlayerStatus
from common.helpers import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        image_path = c.PROJECT_DIRPATH / 'graphics/test/player.png'
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # graphics setup
        self.import_player_assets()
        self.player_direction = PlayerDirection.DOWN
        self.player_status = PlayerStatus.IDLE
        self.frame_index = 0
        self.animation_speed = 0.15

        # movement
        self.direction_vector = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path = c.PROJECT_DIRPATH / 'graphics/player/'
        self.animations = {
            'up_move': [], 'down_move': [], 'left_move': [], 'right_move': [], 
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [], 
            'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': [], 
        }

        for animation in self.animations.keys():
            full_path = character_path / animation
            names_list = import_folder(full_path)
            for name in names_list:
                self.animations[animation].append(name)

    def input(self):
        keys = pygame.key.get_pressed()

        # Check for arrow key presses
        if keys[pygame.K_DOWN]:
            self.direction_vector.y = 1
            self.player_direction = PlayerDirection.DOWN
        elif keys[pygame.K_UP]:
            self.direction_vector.y = -1
            self.player_direction = PlayerDirection.UP
        else:
            self.direction_vector.y = 0

        if keys[pygame.K_LEFT]:
            self.direction_vector.x = -1
            self.player_direction = PlayerDirection.LEFT
        elif keys[pygame.K_RIGHT]:
            self.direction_vector.x = 1
            self.player_direction = PlayerDirection.RIGHT
        else:
            self.direction_vector.x = 0

        if not self.attacking:
            # attack 
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print('attack')

            # magic 
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print('magic')

    def get_status(self):
        # idle status
        if self.direction_vector.x == 0 and self.direction_vector.y == 0:
            self.player_status = PlayerStatus.IDLE
        else:
            self.player_status = PlayerStatus.MOVE
        
        if self.attacking:
            self.direction_vector.x = 0
            self.direction_vector.y = 0
            self.player_status = PlayerStatus.ATTACK


        return self._stringify_player_status()

    def _stringify_player_status(self):
        return f"{self.player_direction.name}_{self.player_status.name}".lower()

    def move(self, speed):
        if self.direction_vector.magnitude() != 0:
            self.direction_vector = self.direction_vector.normalize()
        self.hitbox.x += self.direction_vector.x * speed
        self.collision(DirectionType.HORIZONTAL)
        self.hitbox.y += self.direction_vector.y * speed
        self.collision(DirectionType.VERTICAL)
        self.rect.center = self.hitbox.center

    def _check_for_collision_horizontal(self):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction_vector.x > 0:
                    self.hitbox.right = sprite.hitbox.left
                elif self.direction_vector.x < 0:
                    self.hitbox.left = sprite.hitbox.right

    def _check_for_collision_vertical(self):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction_vector.y > 0:
                    self.hitbox.bottom = sprite.hitbox.top
                elif self.direction_vector.y < 0:
                    self.hitbox.top = sprite.hitbox.bottom
        
    def collision(self, direction: DirectionType):
        if direction == DirectionType.HORIZONTAL:
            self._check_for_collision_horizontal()
        elif direction == DirectionType.VERTICAL:
            self._check_for_collision_vertical()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def animate(self):
        self.status = self.get_status()
        animation = self.animations[self.status]

        # loop over frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.input()
        self.animate()
        self.cooldowns()
        self.move(self.speed)