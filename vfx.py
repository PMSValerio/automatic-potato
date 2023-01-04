from common import *
from entity import Entity
from animation import Animation

class VisualEffect(Entity):
    def __init__(self, pos, anim_path):
        Entity.__init__(self, pos, EntityLayers.VFX)

        self.graphics = Animation(anim_path, False)

    # visual effects exist only to die
    def update(self, delta):
        if self.graphics.end:
            self.die()
