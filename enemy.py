from pygame import Vector2
from common import *
import entity
import animation
import fsm
import enum

import random

class EnemyStates(enum.Enum):
    WANDERING = 0
    SEEK = 1
    FLEE = 2
    ATTACK = 3


class Spawner():
    __instance = None

    def get(): 
        if not Spawner.__instance:
            Spawner()
        return Spawner.__instance

    def __init__(self):
        if Spawner.__instance:
            raise Exception("Spawner singleton class already initialised")
        else:
            Spawner.__instance = self

    def spawn_monster(prototype):
        return prototype.clone()


class Enemy(entity.Entity):
    def __init__(self, health, move_speed, attack_speed, strength):
        init_spawn = self._fetch_spawn_pos()

        entity.Entity.__init__(self, init_spawn[0], EntityLayers.ENEMY)
        
        self.health = health
        self.move_speed = move_speed
        self.attack_speed = attack_speed
        self.strength = strength

        self.move_dir : Vector2 = init_spawn[1]
        self.target_pos = (TARGET_X, TARGET_Y)


        self.fsm = fsm.FSM()
        self.fsm.add_state(EnemyStates.WANDERING, self.wandering, True)
        self.fsm.add_state(EnemyStates.SEEK, self.seek)
        self.fsm.add_state(EnemyStates.FLEE, self.flee)
        self.fsm.add_state(EnemyStates.ATTACK, self.attack)
    

    def _fetch_spawn_pos(self):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)

        side = random.choice(["MAP_BORDER_DOWN", "MAP_BORDER_UP", "MAP_BORDER_RIGHT", "MAP_BORDER_LEFT"])
        
        # depending on the initial position, the move direction is towards the center of the map
        if side == "MAP_BORDER_DOWN":
            self.init_pos = Vector2(x, HEIGHT + 5)
            self.move_dir = Vector2(0, -1)
        
        elif side == "MAP_BORDER_UP":
            self.init_pos = Vector2(x, -5)
            self.move_dir = Vector2(0, 1)
        
        elif side == "MAP_BORDER_LEFT":
            self.init_pos = Vector2(-5, y)
            self.move_dir = Vector2(1, 0)
        
        elif side == "MAP_BORDER_RIGHT":
            self.init_pos = Vector2(WIDTH + 5, y)
            self.move_dir = Vector2(-1, 0)

        return (self.init_pos, self.move_dir)


    def get_random_direction(self):
        return Vector2(random.randint(-1, 1), random.randint(-1, 1)).normalize
        
    def update(self, delta): 
        self.fsm.update()
        self.update_bbox()

    def collide(self, other):
        if other.col_layer == EntityLayers.PLAYER_ATTACK:
            self.damage(other.stats.power)

    def damage(self, value):
        self.health = max(0, self.health - value)

        if self.health == 0:
            self.die()

    def attack(self): 
        raise NotImplementedError

    def seek(self): 
        raise NotImplementedError

    def flee(self): 
        raise NotImplementedError

    def wandering(self): 
        raise NotImplementedError

    def clone(self):
        raise NotImplementedError


class Troll(Enemy):
    def __init__(self):
        # TODO change this to call super with information from json
        super().__init__(health = 30, move_speed = 30, attack_speed = 50, strength = 50)
        
        self.change_dir : int = 15
        self.graphics = animation.Animation("assets/gfx/test.png", True, 5)


    def update(self, delta):
        super().update(delta)
        self.pos += self.move_speed * self.move_dir * delta


    def wandering(self, new = False):
        # change direction after 15 updates
        if self.change_dir == 0:
            self.move_dir = Vector2(random.randint(-1, 1), random.randint(-1, 1))
            self.change_dir = 15

        self.change_dir -= 1
        # if player nearby ... change state


    def seek(self, new = False):
        # move towards the center of the map 
        # common.py TARGET_X and TARGET_Y 
        pass 


    def collide(self, other):
        super().collide(other)

    def damage(self, value):
        super().damage(value)

    def clone(self):
        return Troll()