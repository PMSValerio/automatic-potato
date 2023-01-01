import random
from pygame import Vector2

from common import *
from services import service_locator
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

        self.health = 300

        self.shoot_timer = 0

        self.left_shield = BossShields(Vector2(self.pos.x - 80, self.pos.y))
        self.right_shield = BossShields(Vector2(self.pos.x + 80, self.pos.y))

        self.graphics = Animation("assets/gfx/boss.png")
    
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
            self.shoot()
        else:
            self.shoot_timer -= delta
    
    def collide(self, other):
        if other.col_layer == EntityLayers.PLAYER_ATTACK:
            self.damage(other.stats.power)
    
    def shoot(self):
        deltax = 64
        ran = random.random()
        if ran < 0.33:
            deltax = -64
        elif ran < 0.67:
            deltax = 0
        Spud(Vector2(self.pos.x + deltax, self.pos.y - BLOCK * 0.5), Vector2(0, -1))
    
    def damage(self, value):
        self.health = max(0, self.health - value)
        if self.health == 0:
            service_locator.event_handler.publish(Events.BOSS_DEFEATED)
    
    def on_target_reached(self):
        service_locator.event_handler.publish(Events.BOSS_REACH_TARGET)


class BossShields(Entity):
    def __init__(self, pos):
        Entity.__init__(self, pos, EntityLayers.OBSTACLE)

        self.rect.height = 160
        self.rect.width = 64
    
    def update(self, delta):
        pass
