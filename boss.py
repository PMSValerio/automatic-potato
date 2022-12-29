from common import *
from services import service_locator
from entity import Entity
from animation import Animation

SPEED = 4

class Boss(Entity):
    def __init__(self, pos):
        Entity.__init__(self, pos, EntityLayers.ENEMY)

        self.dir.xy = (0, -1)
        self.rect.height = 160
        self.rect.width = 160

        self.health = 100

        self.graphics = Animation("assets/gfx/boss.png")
    
    def update(self, delta):
        self.pos.y -= SPEED * delta

        self.update_bbox()
    
    def collide(self, other):
        if other.col_layer == EntityLayers.PLAYER_ATTACK:
            self.damage(other.stats.power)

    def damage(self, value):
        self.health = max(0, self.health - value)
        if self.health == 0:
            service_locator.event_handler.publish("boss_defeated")
            print("boss defeated")
    
    def on_target_reached(self):
        pass

