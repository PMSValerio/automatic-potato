from common import *
import enum
import enemy
import fsm 
import services 
import random

TOTAL = "total"
TROLL = "troll"
GHOST = "ghost"
PUMPKIN = "pumpkin"
SKELETON = "skeleton"

class EnemyWaves(enum.Enum):
    IRON = 0 
    SILVER = 1
    GOLD = 2
    PLAT = 3

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

    def setup(self):
        self.wave_info = { 
            EnemyWaves.IRON : {
                TROLL : random.randint(3, 7),
            },

        }

        self._troll_instance = enemy.Troll()
        # self._ghost_instance = Ghost()
        # self._pumpkin_instance = Pumpkin()
        # self._skeleton_instance = Skeleton()

        services.service_locator.event_handler.subscribe(self, Events.KILL_ENTITY)
        self.spawning = True
        self.wave_enemies = 0

    
    def on_notify(self, event, entity = None):
        if event == Events.KILL_ENTITY and entity.col_layer == EntityLayers.ENEMY:
            self.wave_enemies -= 1
        
        if self.wave_enemies == 0: 
            self.iron_league()
            pass

    def iron_league(self, new = False):
        # league = EnemyWaves.IRON
        enemy.Spawner.spawn_monster(self._troll_instance)
        # trolls = [enemy.Spawner.spawn_monster(self._troll_instance) for i in range(self.wave_info[league][TROLL])]
        # self.wave_enemies += len(trolls)
        

    def silver_league(self):
        pass 

    def gold_league(self):
        pass 

    def plat_league(self):
        pass 
