from enum import Enum

WIDTH = 960
HEIGHT = 640

BLOCK = 32 # "cell" unit size

# refresh rate
FPS = 30

# coordinates of enemy target/healing area
TARGET_X = WIDTH / 2
TARGET_Y = HEIGHT / 2

# range of the healing are positioned on map center
HEAL_RANGE = 48

# when in healing zone, player heals 5 hp per sec
HEAL_RATE = 5

# map border; player can only move inside these
MAP_BORDER_LEFT = 128
MAP_BORDER_RIGHT = WIDTH - 128
MAP_BORDER_UP = 128
MAP_BORDER_DOWN = HEIGHT - 128

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

# collision layers
class EntityLayers(Enum):
    NULL = -1
    PLAYER = 0
    PLAYER_ATTACK = 1
    ENEMY = 2
    ENEMY_ATTACK = 3
    PICKUP = 4

# player stats to define multiple player types
class PlayerStats:
    def __init__(self, name, max_health, base_speed):
        self.name = name
        self.max_health = max_health # max hp
        self.speed = base_speed # pix/sec

player_types = {
    "Witch": PlayerStats("Witch", 10, 160),
    "Cat": PlayerStats("Cat", 8, 200)
}

# projectiles' types and stats
class ProjectileStats:
    def __init__(self, name, speed, power, cooldown, col_layer, anim_filepath):
        self.name = name
        self.speed = speed # pix/sec
        self.power = power
        self.cooldown = cooldown # sec
        self.col_layer = col_layer # collision layer (should be either PLAYER_ATTACK or ENEMY_ATTACK)
        self.anim_filepath = anim_filepath

projectile_types = {
    "Spell": ProjectileStats("Spell", 260, 5, 0.3, EntityLayers.PLAYER_ATTACK, "assets/gfx/spell.png"),
    "Pumpkin Bomb": ProjectileStats("Pumpkin Bomb", 200, 20, 0.45, EntityLayers.PLAYER_ATTACK, "assets/gfx/spell.png"),
    "Fish": ProjectileStats("Fish", 300, 2, 0.15, EntityLayers.PLAYER_ATTACK, "assets/gfx/spell.png"),
    "Shark": ProjectileStats("Shark", 180, 15, 0.5, EntityLayers.PLAYER_ATTACK, "assets/gfx/spell.png"),

    "Bone": ProjectileStats("Bone", 180, 2, 3, EntityLayers.ENEMY_ATTACK, "assets/gfx/spell.png"),
    "Spud": ProjectileStats("Spud", 140, 3, 0.8, EntityLayers.ENEMY_ATTACK, "assets/gfx/boss_bullet.png")
}
