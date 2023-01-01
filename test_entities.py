import pygame

from common import *
from player_data import player_data
from entity import Entity
from pickups import *

class Test2(Entity):
    def __init__(self, pos):
        Entity.__init__(self, pos, EntityLayers.ENEMY)

        self.colour = (100, 0, 0)

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
    
    def update(self, delta):
        pass
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)
    
    def collide(self, other):
        self.die()
        player_data.update_score(30)
        SpeedPickup(self.pos.copy())
