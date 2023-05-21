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