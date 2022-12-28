import pygame
from pygame import Vector2

from common import *
from entity import Entity
from animation import Animation

class Projectile(Entity):
    def __init__(self, pos, direction, stats):
        Entity.__init__(self, pos, stats.col_layer)

        self.stats = stats

        self.dir = Vector2(direction.x, 0) if direction.x != 0 else Vector2(0, direction.y)

        self.graphics = Animation(self.stats.anim_filepath, True)

    def update(self, delta):
        self.pos += self.dir * (self.stats.speed * delta)

        if self.pos.x < 0 or self.pos.x >= WIDTH or self.pos.y < 0 or self.pos.y >= HEIGHT:
            self.die()
        
        self.update_bbox()

    def collide(self, other):
        self.die()
