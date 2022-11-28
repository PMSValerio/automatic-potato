from enum import Enum

WIDTH = 60
HEIGHT = 40

SCALE = 16

# refresh rate
FPS = 30

# collision layers
class EntityLayers(Enum):
    NULL = -1
    PLAYER = 0
    OBSTACLE = 1
