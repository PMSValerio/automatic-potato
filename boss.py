import random
from pygame import Vector2

from common import *
import services
from entity import Entity
from animation import Animation
from projectile import Spud

SPEED = 6
TARGET_DIST_THRESHOLD = 64

class Boss(Entity):
    def __init__(self, pos):
        Entity.__init__(self, pos, EntityLayers.ENEMY)

        self.dir.xy = (0, -1)
        self.rect.height = 160
        self.rect.width = 160
        self.health = 1000
        self.shoot_timer = 0

        # position two shields on the sides of the boss to prevent easy win
        self.left_shield = BossShields(Vector2(self.pos.x - 80, self.pos.y))
        self.right_shield = BossShields(Vector2(self.pos.x + 80, self.pos.y))

        self.graphics = Animation("assets/gfx/entities/auto_spud.png", True, 4)

        services.service_locator.sound_mixer.play_music(Music.BOSS)
    
    def update(self, delta):
        self.pos.y -= SPEED * delta
        self.right_shield.pos.y = self.pos.y
        self.left_shield.pos.y = self.pos.y

        # check if already reached centre
        if abs(self.pos.y - TARGET_Y) < TARGET_DIST_THRESHOLD:
            self.on_target_reached()
        
        # semi-randomly fire projectiles 
        if self.shoot_timer <= 0:
            self.shoot_timer = projectile_types["Spud"].cooldown
            # this will init the projectile on a position relative to the giant spud
            self.shoot()
        else:
            self.shoot_timer -= delta
    

    def collide(self, other):
        # inflict damage on self if collided with a player attack
        if other.col_layer == EntityLayers.PLAYER_ATTACK:
            # the amount of damage is relative to the power of the projectile used 
            self.damage(other.stats.power)
    

    def shoot(self):
        delta_x = 64
        r = random.random()

        if r < 0.33:
            delta_x = -64
        elif r < 0.67:
            delta_x = 0

        # slighty init the projectiles more to the left or right
        Spud(Vector2(self.pos.x + delta_x, self.pos.y - BLOCK * 0.5), Vector2(0, -1))
    

    # win condition
    def damage(self, value):
        self.health = max(0, self.health - value)
        if self.health == 0:
            services.service_locator.event_handler.publish(Events.BOSS_DEFEATED)
    

    # lose condition 
    def on_target_reached(self):
        services.service_locator.event_handler.publish(Events.BOSS_REACH_TARGET)


class BossShields(Entity):
    def __init__(self, pos):
        Entity.__init__(self, pos, EntityLayers.OBSTACLE)

        self.rect.height = 160
        self.rect.width = 48
    
    def update(self, delta):
        pass
