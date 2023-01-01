from common import *
from entity import Entity
from animation import Animation

class VisualEffect(Entity):
    def __init__(self, pos, anim_path):
        Entity.__init__(self, pos, EntityLayers.VFX)

        self.graphics = Animation(anim_path, False)

    def update(self, delta):
        if self.graphics.end:
            self.die()