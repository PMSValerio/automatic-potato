from common import *
import pygame
from pygame import Vector2
from entity import Entity
from graphics import Animation

class PlayerProjectile(Entity):
    def __init__(self, pos, direction):
        Entity.__init__(self, pos, EntityLayers.PLAYER_ATTACK)

        self.speed = 240
        self.dir = Vector2(direction.x, 0) if direction.x != 0 else Vector2(0, direction.y)

        self.graphics = Animation("assets/gfx/spell.png", 32, 32, True)
        self.graphics.add_animation("default", 0, 4)

    def update(self, delta):
        self.pos += self.dir * (self.speed * delta)
        
        self.update_bbox()

    def collide(self, other):
        self.die()
