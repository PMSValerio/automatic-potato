import pygame
from pygame import Vector2

from common import *
from entity import Entity
from animation import Animation

class PlayerProjectile(Entity):
    def __init__(self, pos, direction):
        Entity.__init__(self, pos, EntityLayers.PLAYER_ATTACK)

        self.speed = 240
        self.dir = Vector2(direction.x, 0) if direction.x != 0 else Vector2(0, direction.y)

        self.graphics = Animation("assets/gfx/spell.png", True)

    def update(self, delta):
        self.pos += self.dir * (self.speed * delta)
        
        self.update_bbox()

    def collide(self, other):
        self.die()
