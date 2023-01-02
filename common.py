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

# all game events, some should be published along with an argument
class Events(Enum):
    NEW_GAME_STATE = 0 # receives game state id
    NEW_ENTITY = 1 # receives Entity object
    KILL_ENTITY = 2 # receives Entity object
    NEW_HEALTH = 3 # receives new health value
    NEW_SCORE = 4 # receives new score value
    NEW_POTIONS_LEFT = 5 # receives new potions left value
    BOSS_DEFEATED = 6
    BOSS_REACH_TARGET = 7
    DECREASE_POTION = 8 # receives the amount of potions destroyed/stolen

    PAUSE_UNPAUSE = 9 # receives new pause state

# game scenes
class GameStates(Enum):
    TITLE_SCREEN = 0
    CHARACTER_SELECT = 1
    LEVEL = 2
    END_RESULTS = 3
    GAME_OVER = 4
    SCOREBOARD = 5

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
    ENEMY_MELEE = 4
    PICKUP = 5
    OBSTACLE = 6

    VFX = 7 # special layer

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
    def __init__(self, name, speed, power, cooldown, col_layer, anim_filepath, hit_filepath = None):
        self.name = name
        self.speed = speed # pix/sec
        self.power = power
        self.cooldown = cooldown # sec
        self.col_layer = col_layer # collision layer (should be either PLAYER_ATTACK or ENEMY_ATTACK)
        self.anim_filepath = anim_filepath
        self.hit_effect = hit_filepath # animation to be played on collision


projectile_types = {
    "Spell": ProjectileStats("Spell", 260, 5, 0.3, EntityLayers.PLAYER_ATTACK, "assets/gfx/spell.png", "assets/gfx/vfx/spell_hit.png"),
    "Pumpkin Bomb": ProjectileStats("Pumpkin Bomb", 200, 8, 0.45, EntityLayers.PLAYER_ATTACK, "assets/gfx/spell.png"),
    "Fish": ProjectileStats("Fish", 300, 2, 0.15, EntityLayers.PLAYER_ATTACK, "assets/gfx/spell.png"),
    "Shark": ProjectileStats("Shark", 180, 15, 0.5, EntityLayers.PLAYER_ATTACK, "assets/gfx/spell.png"),

    "Bone": ProjectileStats("Bone", 260, 2, 3, EntityLayers.ENEMY_ATTACK, "assets/gfx/spell.png"),
    "Spud": ProjectileStats("Spud", 140, 3, 0.8, EntityLayers.ENEMY_ATTACK, "assets/gfx/boss_bullet.png")
}


class Music(Enum):
    TITLE = "assets/sfx/title_theme.ogg"
    LEVEL = "assets/sfx/waves_theme.ogg"
    BOSS = "assets/sfx/boss_battle.ogg"
    WIN = "assets/sfx/win_game.ogg"
    GAME_OVER = "assets/sfx/game_over.ogg"
