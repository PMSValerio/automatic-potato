from common import *
from player_data import player_data
from entity import Entity
from animation import Animation

class Pickup(Entity):
    def __init__(self, pos, anim_filepath):
        Entity.__init__(self, pos, EntityLayers.PICKUP)

        self.lifespan = 5 # 5 second time to live
        self.age = 0

        self.graphics = Animation(anim_filepath, True)

    def update(self, delta):
        self.age += delta
        if self.age >= self.lifespan:
            self.die()

    def collide(self, other):
        if other.col_layer == EntityLayers.PLAYER:
            self.handle_player(other)
            self.die()
    
    # this method must be extended by the different pickups
    def handle_player(self, player):
        raise NotImplementedError


class SpeedPickup(Pickup):
    def __init__(self, pos):
        Pickup.__init__(self, pos, "assets/gfx/speed_pickup.png")

    def handle_player(self, player):
        print("speed+")
        player.speed_modifier = 1.2

class InvulnPickup(Pickup):
    def __init__(self, pos):
        Pickup.__init__(self, pos, "assets/gfx/speed_pickup.png")

    def handle_player(self, player):
        print("invincible")
        player.invincible_timer = 3

class WeaponPickup(Pickup):
    def __init__(self, pos):
        Pickup.__init__(self, pos, "assets/gfx/speed_pickup.png")
    
    def handle_player(self, player):
        print("weapon upgrade")
        # TODO: change this to a pool of weapon upgrades per player type
        if player_data.player_type.name == "Witch":
            player.projectile_type = projectile_types["Pumpkin Bomb"]
        elif player_data.player_type.name == "Cat":
            player.projectile_type = projectile_types["Shark"]
