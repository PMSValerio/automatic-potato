from pygame import Vector2
from common import *
from entity import Entity
from animation import Animation
from enum import Enum
from fsm import FSM

import random

class EnemyStates(Enum):
    WANDERING = 0
    SEEK = 1
    FLEE = 2
    ATTACK = 3

class Enemy(Entity):
    def __init__(self, pos, health, move_speed, attack_speed, strength):
        Entity.__init__(self, pos, EntityLayers.ENEMY)
        
        self._health = health
        self._move_speed = move_speed
        self._attack_speed = attack_speed
        self._strength = strength

        self._move_dir : Vector2 = Vector2(0, 0)

        self.fsm = FSM()
        self.fsm.add_state(EnemyStates.WANDERING, self.wandering, True)
        self.fsm.add_state(EnemyStates.SEEK, self.seek)
        # self.fsm.add_state(EnemyStates.FLEE, self.flee)
        # self.fsm.add_state(EnemyStates.ATTACK, self.attack)

    def update(self, delta): 
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


class Troll(Enemy):
    def __init__(self):
        # TODO change this to call super with information from json
        pos = Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))

        super().__init__(pos, 100, 1, 50, 50)
        self._change_dir : int = 5

        self.graphics = Animation("assets/gfx/test.png", True, 5)


    def update(self, delta):
        self.pos += self._move_speed * self._move_dir

        self.fsm.update()
        self.update_bbox()


    def wandering(self, useless = False):
        print("wandering")
        # change direction after 5 updates
        if self._change_dir == 0:
            self._move_dir = Vector2(random.randint(-1, 1), random.randint(-1, 1))
            self._change_dir = 5

        self._change_dir -= 1

        # if player nearby ...

    def clone(self):
        return Troll()