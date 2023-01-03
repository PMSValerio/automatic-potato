from enum import Enum
from pygame import Rect, Vector2, Color, Surface, BLEND_ADD, BLEND_RGBA_MULT
from pygame.sprite import Sprite

from common import *
import services
from fsm import FSM

class Effects(Enum):
    NONE = 0
    FLASH = 1
    FADE = 2
    CRITICAL = 3

class Entity(Sprite):
    def __init__(self, pos : Vector2, layer = EntityLayers.NULL):
        Sprite.__init__(self)

        self.pos = pos # position in space

        self.dir = Vector2(1, 0) # movement direction

        self.rect = Rect(0, 0, BLOCK, BLOCK) # bounding box
        self.update_bbox()

        self.graphics = None
        self._to_blit = None # the actual surface to be blitted after all image effects

        self.col_layer = layer # layer used by physics engine
        self.collision_on = True # if false, physics manager will not consider this entity in collisions

        self.tint_colour = Color(255, 255, 255)
        self.tint_strength = 0 # range: 0 - 1
        self.alpha = 255

        self.image_effect_fsm = FSM()
        self.image_effect_fsm.add_state(Effects.NONE, None, True)
        self.image_effect_fsm.add_state(Effects.FLASH, self.flash_effect)
        self.image_effect_fsm.add_state(Effects.FADE, self.fade_effect)
        self.image_effect_fsm.add_state(Effects.CRITICAL, self.flash_red_effect)
        self.effect_end = False # flag signalling the end of an effect

        services.service_locator.event_handler.publish(Events.NEW_ENTITY, self)
    
    # this function is to be called by the entity manager ONLY, custom code should go in update()
    def _update(self, delta):
        self.update(delta)

        self.effect_end = False

        self.update_bbox()

        if self.graphics is not None:
            self.graphics.update_frame()
        
        self.image_effect_fsm.update()

    def update(self, delta):
        raise NotImplementedError
    
    # draw animation
    def draw(self, surface):
        if self.graphics is not None:
            if self._to_blit is None:
                self._to_blit = self.graphics.get_frame().copy()
            else:
                self._to_blit.fill((0, 0, 0, 0))
                im = self.graphics.get_frame()
                self._to_blit.blit(im, im.get_rect())

            rect = self._to_blit.get_rect(center=self.pos.xy)
            # image tinting
            if self.tint_strength > 0:
                col = (self.tint_colour.r * self.tint_strength, self.tint_colour.g * self.tint_strength, self.tint_colour.b * self.tint_strength)
                self._to_blit.fill(col, special_flags = BLEND_ADD)
            # alpha property
            if self.alpha < 255:
                self._to_blit.set_alpha(self.alpha)
            surface.blit(self._to_blit, rect)


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
    def enable_collision(self, en = True):
        self.collision_on = en
    
    def play_effect(self, effect):
        self.tint_colour.update(255, 255, 255)
        self.tint_strength = 0
        self.alpha = 255
        self.image_effect_fsm.change_state(effect)
    
    # --- || Image effects || ---

    # entity turns to white and fades out, when used in an enemy death animation, the best thing to do is probably include a new DYING state in which
    # collisions and processing do not occur; calls self.die() when self.effect_end becomes True
    def fade_effect(self, transition = False):
        if transition:
            self.tint_colour.update(WHITE)
            self.tint_strength = 0
            self.alpha = 255
        
        if self.tint_strength < 1:
            self.tint_strength = min(1, self.tint_strength + 0.4)
        elif self.alpha > 0:
            self.alpha -= 20
        else:
            self.alpha = 0
            self.image_effect_fsm.change_state(Effects.NONE)
            self.effect_end = True
    
    # entity flashes white for a moment
    def flash_effect(self, transition = False):
        if transition:
            self.tint_colour.update(WHITE)
            self.tint_strength = 1
            self.alpha = 255
        
        self.tint_strength -= 0.2
        if self.tint_strength <= 0:
            self.tint_strength = 0
            self.image_effect_fsm.change_state(Effects.NONE)
            self.effect_end = True


    # entity flashes white for a moment
    def flash_red_effect(self, transition = False):
        if transition:
            self.tint_colour.update(RED)
            self.tint_strength = 1
            self.alpha = 255
        
        self.tint_strength -= 0.2
        if self.tint_strength <= 0:
            self.tint_strength = 0
            self.image_effect_fsm.change_state(Effects.NONE)
            self.effect_end = True
