from pygame import Vector2
from common import *
import entity
import animation
import fsm
import enum
import math
import random
import player_data
import numpy

class EnemyTypes(enum.Enum):
    TROLL = 0
    PUMPKIN = 1
    SKELETON = 2
    GHOST = 3

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
    import json
    # def __init__(self, type : EnemyTypes):
    def __init__(self, health, move_speed, attack_speed, strength, value):
        entity.Entity.__init__(self, self._random_spawn_pos(), EntityLayers.ENEMY)
        
        self.stats = self.load_stats(type)

        self.health = health
        self.move_speed = move_speed
        self.attack_speed = attack_speed
        self.strength = strength
        self.value = value

        self.move_dir : Vector2 = Vector2(0, 0)
        self.target_pos = (TARGET_X, TARGET_Y)

        self.fsm = fsm.FSM()
        self.fsm.add_state(EnemyStates.WANDERING, self.wandering, True)
        self.fsm.add_state(EnemyStates.SEEK, self.seek)
        self.fsm.add_state(EnemyStates.FLEE, self.flee)
        self.fsm.add_state(EnemyStates.ATTACK, self.attack)
    

    def _random_spawn_pos(self):
        # generate a random x and y 
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)

        side = random.choice(["MAP_BORDER_DOWN",
                              "MAP_BORDER_UP", 
                              "MAP_BORDER_RIGHT", 
                              "MAP_BORDER_LEFT"])
        
        # choose a random side of the map
        # and depending on the side, create a random initial position just slighty outside 
        # so the player doesn't see the mobs spawning 

        if side == "MAP_BORDER_DOWN":
            self.init_pos = Vector2(x, HEIGHT + 2)
        
        elif side == "MAP_BORDER_UP":
            self.init_pos = Vector2(x, -2)
        
        elif side == "MAP_BORDER_LEFT":
            self.init_pos = Vector2(-2, y)
        
        elif side == "MAP_BORDER_RIGHT":
            self.init_pos = Vector2(WIDTH + 2, y)

        return self.init_pos

    def load_stats(self, type : EnemyTypes):
        # will use the EnemyData class to access its dictionary, containing
        # all the information about a certain type of enemy 
        # and then loads the data to create said enemey (use EnemyType enum)

        # self.health = health
        # self.move_speed = move_speed
        # self.attack_speed = attack_speed
        # self.strength = strength
        # self.value = value
        pass 

    def get_random_direction(self):
        return Vector2(random.randint(-1, 1), random.randint(-1, 1))

    # calculate a random roaming position relatively close to the current position
    def get_wandering_position(self):
        new_pos = self.pos + self.get_random_direction() * random.randint(20, 60)

        # guarantee that new position is within map boundaries 
        while new_pos == self.pos or \
              new_pos.x >= max(new_pos.x, WIDTH) or new_pos.x <= min(new_pos.x, 0) or \
                new_pos.y >= max(new_pos.y, HEIGHT) or new_pos.y <= min(new_pos.y, 0):

            # while it's not, generate a new one
            new_pos = self.pos + self.get_random_direction() * random.randint(20, 60)

        return new_pos
    
    def update(self, delta): 
        self.fsm.update()
        self.update_bbox()

    def collide(self, other):
        # there are different types of players, which means that the damage is not always equal
        # damage accordingly to the power of each player 

        # TODO: decrease damage based on enemy defense capacity 
        if other.col_layer == EntityLayers.PLAYER_ATTACK:
            self.damage(other.stats.power)

    def damage(self, value):
        self.health = max(0, self.health - value)

        if self.health == 0:
            self.die()

        # each mob will then increase the player's score based on how difficult they are to kill

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
        super().__init__(health = 30, move_speed = 30, attack_speed = 50, strength = 50, value = 10)
        
        self.graphics = animation.Animation("assets/gfx/test.png", True, 5)
        self.wander_pos = super().get_wandering_position() 

    def update(self, delta):
        super().update(delta)

        self.pos += self.move_speed * self.move_dir * delta


    def wandering(self, new = False):
        self.player_pos = player_data.player_data.get_player_pos()

        # get direction to wandering position
        direction = (self.wander_pos - self.pos)
        self.move_dir = direction / numpy.linalg.norm(direction)
        
        # reached wandering position, recalculate
        if self.pos.distance_to(self.wander_pos) < 1: 
            self.wander_pos = super().get_wandering_position() 

        if self.pos.distance_to(self.target_pos) < 300: 
            print("from wandering to seek")
            self.fsm.change_state(EnemyStates.SEEK)

        if self.pos.distance_to(self.player_pos) < 100:
            print("from wandering to attack")
            self.fsm.change_state(EnemyStates.ATTACK)

    def seek(self, new = False):
        self.player_pos = player_data.player_data.get_player_pos()
        # change move speed to go faster 

        # get direction to the center of the map 
        direction = (self.target_pos - self.pos) 
        self.move_dir = direction / numpy.linalg.norm(direction)

        # if the player is close, change to attack 
        if self.pos.distance_to(self.player_pos) < 30:
            print("from seek to attack")
            self.fsm.change_state(EnemyStates.ATTACK)

    def attack(self, new = False):
        self.player_pos = player_data.player_data.get_player_pos()
        # change to attack speed 

        # get direction to the player's position
        direction = (self.player_pos - self.pos) 
        self.move_dir = direction / numpy.linalg.norm(direction)

        if self.pos.distance_to(self.player_pos) >= 10:
            print("from seek to attack")
            self.fsm.change_state(EnemyStates.SEEK)
        

    def collide(self, other):
        super().collide(other)
        player_data.player_data.update_score(20)

    def damage(self, value):
        super().damage(value)

    def clone(self):
        return Troll()