from common import *
from entity import Entity
from enum import Enum
from fsm import FSM

class EnemyStates(Enum):
    WANDERING = 0
    SEEK = 1
    FLEE = 2
    ATTACK = 3

class Breed():
    def __init__(self, health, move_speed, attack_speed, strength):
        self._health = health
        self._move_speed = move_speed
        self._attack_speed = attack_speed
        self._strength = strength

    def get_health(self): return self._health    
    def get_move_speed(self): return self._move_speed    
    def get_attack_speed(self): return self._attack_speed  
    def get_strength(self): return self._strength 

    def wandering(self):
        pass

    def attack(self):
        pass 

    def seek(self):
        pass

    def flee(self):
        pass


class Enemy(Entity):
    
    def __init__(self, pos, breed : Breed):
        Entity.__init__(self, pos, EntityLayers.ENEMY)
        
        # breed properties
        self._breed = breed 

        self._health = breed.get_health()
        self._move_speed = breed.get_move_speed()
        self._attack_speed = breed.get_attack_speed()
        self._strength = breed.get_strength()

        self.fsm = FSM()
        self.fsm.add_state(EnemyStates.WANDERING, self.wandering, True)
        self.fsm.add_state(EnemyStates.SEEK, self.seek)
        self.fsm.add_state(EnemyStates.FLEE, self.flee)
        self.fsm.add_state(EnemyStates.ATTACK, self.attack)

    
    def wandering(self): self._breed.wandering()
    def attack(self): self._breed.attack()
    def seek(self): self._breed.seek()
    def flee(self): self._breed.flee()

