from pygame import Rect, Vector2
from pygame.sprite import Sprite

from common import *
import services

class Entity(Sprite):
    def __init__(self, pos : Vector2, layer = EntityLayers.NULL):
        Sprite.__init__(self)

        self.pos = pos # position in space

        self.dir = Vector2(1, 0) # movement direction

        self.rect = Rect(0, 0, BLOCK, BLOCK) # bounding box
        self.update_bbox()

        self.graphics = None

        self.col_layer = layer # layer used by physics engine

        services.service_locator.event_handler.publish("new_entity", self)
    
    def update(self, delta):
        raise NotImplementedError
    
    # draw and update animation
    def draw(self, surface):
        if self.graphics is not None:
            surface.blit(self.graphics.get_frame(), self.rect)


    def die(self):
        services.service_locator.event_handler.publish("kill_entity", self)
    
    # called by physics engine if collision
    def collide(self, other):
        pass
    

    # update self.rect to match position on screen
    def update_bbox(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
    
    # change to a different animation
    def set_animation(self, anim_name):
        self.graphics.play(anim_name)
