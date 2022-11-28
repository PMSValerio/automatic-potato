from pygame import Rect, Vector2
from pygame.sprite import Sprite

from common import *
import services

class Entity(Sprite):
    def __init__(self, pos : Vector2, layer = EntityLayers.NULL):
        Sprite.__init__(self)

        self.pos = pos # position in space

        self.dir = Vector2(1, 0) # movement direction

        self.rect = Rect(0, 0, SCALE, SCALE) # bounding box

        self.sprite = None # spritesheet object

        self.col_layer = layer # layer used by physics engine

        services.service_locator.event_handler.publish("new_entity", self)
    
    def update(self, delta):
        raise NotImplementedError

    def draw(self, surface):
        raise NotImplementedError

    def die(self):
        services.service_locator.event_handler.publish("kill_entity", self)
    
    # called by physics engine if collision
    def collide(self, other):
        pass
