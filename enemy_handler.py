from pygame import Vector2
from common import *
from entity import Entity
from enum import Enum
from enemy import Troll, Spawner

import random

from fsm import FSM

class EnemyManager: 
    __instance = None
    
    def get():
        if not EnemyManager.__instance:
            EnemyManager()
        return EnemyManager.__instance 

    
    def __init__(self):
        if EnemyManager.__instance:
            raise Exception("Enemy Manager class already initialised")
        else:
            EnemyManager.__instance = self

            self._troll_instance = Troll()
            # self._ghost_instance = Ghost()
            # self._pumpkin_instance = Pumpkin()
            # self._skeleton_instance = Skeleton()
