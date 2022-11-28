import pygame

from common import *
from entity import Entity

class Test1(Entity):
    def __init__(self, pos):
        Entity.__init__(self, pos, EntityLayers.PLAYER)

        self.colour = (255, 0, 0)
    
    def update(self, delta):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_w]:
            self.pos.y -= 40 * delta
        if pressed[pygame.K_s]:
            self.pos.y += 40 * delta
        if pressed[pygame.K_a]:
            self.pos.x -= 40 * delta
        if pressed[pygame.K_d]:
            self.pos.x += 40 * delta
        
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)

class Test2(Entity):
    def __init__(self, pos):
        Entity.__init__(self, pos, EntityLayers.OBSTACLE)

        self.die_on_col = pos.x > WIDTH * SCALE / 2
        self.colour = ((0, 0, 0) if self.die_on_col else (100, 0, 0))

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
    
    def update(self, delta):
        pass
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)
        self.colour = ((0, 0, 0) if self.die_on_col else (100, 0, 0))
    
    def collide(self, other):
        self.colour = (0, 255, 0)
        if self.die_on_col:
            self.die()