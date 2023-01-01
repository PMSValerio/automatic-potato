from pygame import Vector2
from common import *
import entity
import fsm
import enum
import random
import player_data
import enemy_data
import numpy 

class EnemyTypes(enum.Enum):
    TROLL = 0
    PUMPKIN = 1
    SKELETON = 2
    GHOST = 3

class EnemyStates(enum.Enum):
    WANDERING = 0
    SEEKING = 1
    FLEEING = 2
    ATTACKING = 3
    DYING = 4

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
    def __init__(self, type : EnemyTypes):
        entity.Entity.__init__(self, self._random_spawn_pos(), EntityLayers.ENEMY)
        
        self.load_stats(type)

        self.move_dir : Vector2 = Vector2(0, 0)
        self.target_pos = (TARGET_X, TARGET_Y)

        self.shoot_dir = Vector2(1, 0)
        self.shoot_timer = 0

        # all enemies will follow this state machine 
        self.fsm = fsm.FSM()
        self.fsm.add_state(EnemyStates.WANDERING, self.wandering, True)
        self.fsm.add_state(EnemyStates.SEEKING, self.seeking)
        self.fsm.add_state(EnemyStates.ATTACKING, self.attacking)
        self.fsm.add_state(EnemyStates.FLEEING, self.fleeing)
        self.fsm.add_state(EnemyStates.DYING, self.dying)

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
        # access the EnemyData dictionary that has the information loaded from the enemy.json file
        # check if the enemy type requested exists in the dictionary, raise KeyError if not
        
        data = enemy_data.EnemyData.get().data

        # initialize instance properties with the provided data
        if type.value in data: 
            data = data[type.value]

            # moving speeds for the different states
            self.wandering_speed = data["wandering_speed"]
            self.seek_speed = data["seek_speed"]
            self.attack_speed = data["attack_speed"]

            # distances needed to change states 
            self.seek_distance = data["seek_distance"]
            self.attack_distance = data["attack_distance"]

            # stats
            self.health = data["health"]
            self.armor = data["armor"]
            self.strength = data["strength"]
            self.score_value = data["score_value"]

            # projectile 
            self.projectile_type = projectile_types[data["projectile_type"]]

        else: 
            raise KeyError("Type {} of enemy does not exist.".format(type))


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
    
    
    def update_move_dir(self, target_position):
        direction = (target_position - self.pos)
        self.move_dir = direction / numpy.linalg.norm(direction)
    

    def get_flee_position(self):
        return self._random_spawn_pos()


    def update(self, delta): 
        self.fsm.update()
        self.update_bbox()


    def collide(self, other):
        # there are different types of players, which means that the damage is not always equal
        # damage accordingly to the power of each player 

        # decrease damage based on the enemy's armor
        if other.col_layer == EntityLayers.PLAYER_ATTACK:
            self.damage(other.stats.power - self.armor)


    def damage(self, value):
        # each mob will independently increase the player's score based on their own score value
        self.health = max(0, self.health - value)
        
        if self.health == 0:
            self.fsm.change_state(EnemyStates.DYING)


    def attacking(self): 
        raise NotImplementedError

    def seeking(self): 
        raise NotImplementedError

    def fleeing(self): 
        raise NotImplementedError

    def wandering(self): 
        raise NotImplementedError

    def dying(self):
        raise NotImplementedError

    def clone(self):
        raise NotImplementedError
