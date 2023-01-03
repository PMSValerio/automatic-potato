import pygame
from pygame import Vector2

from common import *
from entity import Entity
from animation import Animation
from vfx import VisualEffect

class Projectile(Entity):
    def __init__(self, pos, direction, stats):
        Entity.__init__(self, pos, stats.col_layer)

        self.stats = stats

        self.dir = direction

        self.graphics = Animation(self.stats.anim_filepath, True, 2)

    def update(self, delta):
        self.pos += self.dir * (self.stats.speed * delta)

        if self.pos.x < 0 or self.pos.x >= WIDTH or self.pos.y < 0 or self.pos.y >= HEIGHT:
            self.die()

    def collide(self, other):
        self.die()
        if self.stats.hit_effect is not None:
            if other.col_layer == EntityLayers.OBSTACLE:
                VisualEffect(self.pos.copy(), "assets/gfx/vfx/null_hit.png")
            else:
                VisualEffect(self.pos.copy(), self.stats.hit_effect)
    

class Spell(Projectile):
    def __init__(self, pos, direction):
        Projectile.__init__(self, pos, direction, projectile_types["Spell"])

        self.rot = self.dir.copy()

class PBomb(Projectile):
    def __init__(self, pos, direction):
        Projectile.__init__(self, pos, direction, projectile_types["Pumpkin Bomb"])

        self.graphics.loop = False

    def update(self, delta):
        super().update(delta)
        if self.graphics.end:
            self.explode()
    
    def explode(self):
        self.die()
        PBombExplode(self.pos.copy())

    def collide(self, other):
        self.explode()

class PBombExplode(Projectile):
    def __init__(self, pos):
        Projectile.__init__(self, pos, Vector2(1, 0), projectile_types["Bomb Explosion"])

        self.graphics.loop = False
    
    def update(self, delta):
        if self.graphics.end:
            self.die()
    
    def collide(self, other):
        pass

class Fish(Projectile):
    def __init__(self, pos, direction):
        Projectile.__init__(self, pos, direction, projectile_types["Fish"])

class Shark(Projectile):
    def __init__(self, pos, direction):
        Projectile.__init__(self, pos, direction, projectile_types["Shark"])

        self.rect.size = (48, 48)

        self.rot = self.dir.copy()
        # self.flip = direction.x < 0
    
    def collide(self, other):
        if self.stats.hit_effect is not None:
            if other.col_layer == EntityLayers.OBSTACLE:
                VisualEffect(self.pos.copy(), "assets/gfx/vfx/null_hit.png")
                self.die()
            else:
                VisualEffect(self.pos.copy(), self.stats.hit_effect)

class Spud(Projectile):
    def __init__(self, pos, direction):
        Projectile.__init__(self, pos, direction, projectile_types["Spud"])

    def collide(self, other):
        if other.col_layer == EntityLayers.PLAYER:
            Projectile.collide(self, other)
