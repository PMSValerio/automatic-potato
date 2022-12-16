from enum import Enum

WIDTH = 960
HEIGHT = 640

BLOCK = 32 # "cell" unit size

# refresh rate
FPS = 30

# movement directions
class Directions(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)

# collision layers
class EntityLayers(Enum):
    NULL = -1
    PLAYER = 0
    PLAYER_ATTACK = 1
    ENEMY = 2
    ENEMY_ATTACK = 3
    OBSTACLE = 4
