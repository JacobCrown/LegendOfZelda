import pygame

from player import Player
from common.enums import PlayerDirection


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player: Player, groups) -> None:
        super().__init__(groups)
        direction = player.player_direction

        #graphics
        self.image = pygame.Surface((40,40))

        #placement
        self.rect = self._get_rect_placement(direction, player)

    def _get_rect_placement(self, direction: PlayerDirection, player: Player):
        rect: pygame.Rect
        if direction == PlayerDirection.UP:
            rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10,0))
        elif direction == PlayerDirection.DOWN:
            rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10,0))
        elif direction == PlayerDirection.RIGHT:
            rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0,16))
        elif direction == PlayerDirection.LEFT:
            rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0,16))
        else:
            rect = self.image.get_rect(center=player.rect.center)
        return rect
        
    
