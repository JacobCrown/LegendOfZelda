from enum import Enum


class DirectionType(Enum):
    HORIZONTAL = 1
    VERTICAL = 0


class SpriteType(Enum):
    INVISIBLE = 1
    GRASS = 2
    OBJECT = 3


class LayoutType(Enum):
    BOUNDARY = '395'
    NOTHING = '-1'


class PlayerDirection(Enum):
    """Indicates status of the player e.g. Facing down/up/right/left"""
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

class PlayerStatus(Enum):
    IDLE = 1
    MOVE = 2
    ATTACK = 3
