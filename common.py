from enum import Enum

WIDTH = 960
HEIGHT = 640

BLOCK = 32 # "cell" unit size

# refresh rate
FPS = 30

# game scenes
class GameStates(Enum):
    TITLE_SCREEN = 0
    CHARACTER_SELECT = 1
    LEVEL = 2
    END_RESULTS = 3

# movement directions
class Directions(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)

# player stats to define multiple player types
class PlayerStats:
    def __init__(self, max_health, base_speed):
        self.max_health = max_health # max hp
        self.speed = base_speed # pix/sec

witch_stats = PlayerStats(10, 160)
cat_stats = PlayerStats(8, 200)

# collision layers
class EntityLayers(Enum):
    NULL = -1
    PLAYER = 0
    PLAYER_ATTACK = 1
    ENEMY = 2
    ENEMY_ATTACK = 3
    OBSTACLE = 4
