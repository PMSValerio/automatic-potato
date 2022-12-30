from common import *
import enum
import enemy
import fsm 

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

        self.fsm = fsm.FSM()
        self.fsm.add_state(EnemyWaves.IRON, self.iron, True)
        self.fsm.add_state(EnemyWaves.SILVER, self.silver)
        self.fsm.add_state(EnemyWaves.GOLD, self.gold)
        self.fsm.add_state(EnemyWaves.PLAT, self.plat)

        self._troll_instance = enemy.Troll()
        # self._ghost_instance = Ghost()
        # self._pumpkin_instance = Pumpkin()
        # self._skeleton_instance = Skeleton()

    def update(self, delta):
        self.fsm.update()

    def iron(self, delta):
        print("spawning")
        for i in range(0, 10):
            enemy.Spawner.spawn_monster(self._troll_instance)

    def silver(self, delta):
        pass 

    def gold(self, delta):
        pass 

    def plat(self, delta):
        pass 
