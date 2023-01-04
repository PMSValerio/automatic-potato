from common import *
from pygame import Vector2
import enum
import enemy
import enemy_skeleton
import enemy_ghost
import enemy_pumpkin
import enemy_troll
import services 
import random
import boss

TOTAL = "total"
PICK = "pick"
WEIGHTS = "weights"

class EnemyWaves(enum.Enum):
    IRON = 0 
    SILVER = 1
    GOLD = 2
    PLAT = 3
    EMERALD = 4

# this singleton will handle all the logic of the enemy waves 
# time the spawns and pick the enemies based on probability 

class EnemyHandler: 
    __instance = None
    
    def get():
        if not EnemyHandler.__instance:
            EnemyHandler()
        return EnemyHandler.__instance 

    
    def __init__(self):
        if EnemyHandler.__instance:
            raise Exception("Enemy Manager class already initialised")
        else:
            EnemyHandler.__instance = self

            self.spawn_cooldown = 1
            self.spawn_timer = self.spawn_cooldown


    def update(self, delta):
        if self.spawn_timer > 0:
            self.spawn_timer -= delta
        
        # when the spawn cools down and if there are still mobs to spawn in this wave 
        if self.spawn_timer <= 0 and self.wave_info[self.league][TOTAL] > 0:
            # spawn a random mob based on the wave's pick and weights for each enemy type:

            # random.choices sorts and returns the pick array, based on the weights,
            # pick the enemy in the first index position of said array and spawn it
            enemy.Spawner.spawn_monster(
                random.choices(self.wave_info[self.league][PICK], weights=self.wave_info[self.league][WEIGHTS])[0]
            )

            # update wave variables
            self.wave_enemies += 1
            self.spawn_timer = self.spawn_cooldown
            self.wave_info[self.league][TOTAL] -= 1
            
            # if its the last wave and half the mobs have been spawned, start trying to spawn the boss
            # also based on a 50-50 probability 
            # IF not self.spawn_boss guarantees that it won't spawn the boss more than one time    
            if [self.league] == EnemyWaves.EMERALD and self.wave_info[self.league][TOTAL] < 5 and not self.spawn_boss:
                self.spawn_boss = random.choice([True, False])


    def setup(self):
        # get prototype instances ready
        self._skeleton_instance = enemy_skeleton.Skeleton()
        self._ghost_instance = enemy_ghost.Ghost()
        self._pumpkin_instance = enemy_pumpkin.Pumpkin()
        self._troll_instance = enemy_troll.Troll()

        self.wave_info = { 
            EnemyWaves.IRON : {
                # total number of mobs for this wave
                TOTAL : 10,
                # types of mobs to pick from in this wave
                PICK : [self._skeleton_instance, self._ghost_instance],
                # weights of chance for said mobs (match index) to be picked
                WEIGHTS : [60, 40],
            },
            EnemyWaves.SILVER : {
                TOTAL : 7,
                PICK : [self._skeleton_instance, self._ghost_instance, self._pumpkin_instance],
                WEIGHTS : [60, 20, 20],
            },
            EnemyWaves.GOLD : {
                TOTAL : 10,
                PICK : [self._skeleton_instance, self._ghost_instance, self._pumpkin_instance, self._troll_instance],
                WEIGHTS : [40, 30, 20, 10],
            },
            EnemyWaves.PLAT : {
                TOTAL : 15,
                PICK : [self._skeleton_instance, self._ghost_instance, self._pumpkin_instance, self._troll_instance],
                WEIGHTS : [30, 20, 30, 20],
            },
            EnemyWaves.EMERALD : {
                TOTAL : 10,
                PICK : [self._skeleton_instance, self._ghost_instance, self._pumpkin_instance, self._troll_instance],
                WEIGHTS : [25, 25, 25, 25],
            },
        }
        

        services.service_locator.event_handler.subscribe(self, Events.KILL_ENTITY)

        # keep track of current league, enemies, and if the boss has been spawned
        self.leagues = [EnemyWaves.IRON, EnemyWaves.SILVER, EnemyWaves.GOLD, EnemyWaves.PLAT, EnemyWaves.EMERALD]
        self.wave_enemies = 0
        self.curr = 0
        self.league = self.leagues[self.curr]
        self.spawn_boss = False


    def on_notify(self, event, entity = None):
        # if an entity dies and is either an enemy or enemy melee, subtract the number of enemies alive by 1 
        if event == Events.KILL_ENTITY and \
            (entity.col_layer == EntityLayers.ENEMY or entity.col_layer == EntityLayers.ENEMY_MELEE):
            self.wave_enemies -= 1

            # if no more enemies and yet another wave to come, call it 
            if self.wave_enemies == 0: 
                self.curr = min(self.curr + 1, 4)
                self.league = self.leagues[self.curr]

                # its time to call the big guns 
                if self.spawn_boss: 
                    boss.Boss(Vector2(WIDTH * 0.5, HEIGHT))

                # if the round ended and the boss wasn't spawned (it happens by chance)
                if self.league == EnemyWaves.EMERALD and self.spawn_boss == False:
                    boss.Boss(Vector2(WIDTH * 0.5, HEIGHT))