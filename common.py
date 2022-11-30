from enum import Enum

WIDTH = 960
HEIGHT = 640

BLOCK = 32 # "cell" unit size

# refresh rate
FPS = 30

# collision layers
class EntityLayers(Enum):
    NULL = -1
    PLAYER = 0
    OBSTACLE = 1
