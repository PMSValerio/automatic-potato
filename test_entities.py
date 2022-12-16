import pygame

from common import *
from entity import Entity
from graphics import Animation

class Test1(Entity):
    def __init__(self, pos):
        Entity.__init__(self, pos, EntityLayers.PLAYER)

        self.colour = (255, 0, 0)
        self.graphics = Animation("assets/gfx/test.png", 32, 32, True, 5) # animation object
        self.graphics.add_animation("idle", 0, 4)
    
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