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
        self.collision_on = True # if false, physics manager will not consider this entity in collisions

        services.service_locator.event_handler.publish(Events.NEW_ENTITY, self)
    
    # this function is to be called by the entity manager ONLY, custom code should go in update()
    def _update(self, delta):
        self.update(delta)

        self.update_bbox()

        if self.graphics is not None:
            self.graphics.update_frame()

    def update(self, delta):
        raise NotImplementedError
    
    # draw animation
    def draw(self, surface):
        if self.graphics is not None:
            subimage = self.graphics.get_frame()
            rect = subimage.get_rect(center=self.pos.xy)
            surface.blit(subimage, rect)


    def die(self):
        services.service_locator.event_handler.publish(Events.KILL_ENTITY, self)
    
    # called by physics engine if collision
    def collide(self, other):
        pass
    

    # update self.rect to match position on screen
    def update_bbox(self):
        self.rect.center = self.pos.xy
    
    # change to a different animation
    def set_animation(self, anim_name):
        self.graphics.play(anim_name)
    
    # toggle collision detection on or off
    def enable_collision(en = True):
        self.collision_on = en
