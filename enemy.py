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
        
        self._health = health
        self._move_speed = move_speed
        self._attack_speed = attack_speed
        self._strength = strength

        self._move_dir : Vector2 = init_spawn[1]

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
            init_pos = Vector2(x, HEIGHT + 5)
            move_dir = Vector2(0, -1)
        
        elif side == "MAP_BORDER_UP":
            init_pos = Vector2(x, -5)
            move_dir = Vector2(0, 1)
        
        elif side == "MAP_BORDER_LEFT":
            init_pos = Vector2(-5, y)
            move_dir = Vector2(1, 0)
        
        elif side == "MAP_BORDER_RIGHT":
            init_pos = Vector2(WIDTH + 5, y)
            move_dir = Vector2(-1, 0)

        return (init_pos, move_dir)

    
    def update(self, delta): 
        raise NotImplementedError

    def damage(self, value):
        raise NotImplementedError

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
        
        self._change_dir : int = 15
        self.graphics = animation.Animation("assets/gfx/test.png", True, 5)

    def update(self, delta):
        self.pos += self._move_speed * self._move_dir * delta

        self.fsm.update()
        self.update_bbox()

    def wandering(self, new = False):
        # change direction after 15 updates
        if self._change_dir == 0:
            self._move_dir = Vector2(random.randint(-1, 1), random.randint(-1, 1))
            self._change_dir = 15

        self._change_dir -= 1
        # if player nearby ... change state

    def seek(self, new = False):
        # move towards the center of the map 
        # common.py TARGET_X and TARGET_Y 
        pass 

    def collide(self, other):
        if other.col_layer == EntityLayers.PLAYER_ATTACK:
            self.damage(other.stats.power)

    def damage(self, value):
        self._health = max(0, self._health - value)
        if self._health == 0:
            self.die()

    def clone(self):
        return Troll()