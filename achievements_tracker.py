import json

from common import *
import services
from enemy import EnemyTypes

class AchievementTracker:
    def __init__(self):
        self.achievements_data = {}
        with open("json/achievements.json") as fin:
            self.achievements_data = json.load(fin)

        self.killed_enemies = {k: 0 for k in EnemyTypes}

    def setup(self):
        services.service_locator.event_handler.subscribe(self, Events.ENEMY_KILLED)
        services.service_locator.event_handler.subscribe(self, Events.BOSS_SPAWNED)
        services.service_locator.event_handler.subscribe(self, Events.BOSS_DEFEATED)
    
    # event callback
    def on_notify(self, event, arg):
        if event == Events.ENEMY_KILLED:
            self.killed_enemies[arg] += 1
            if self.killed_enemies[arg] == 10:
                self.complete_pwn_achievement(arg)
        elif event == Events.BOSS_SPAWNED:
            self.complete_achievement(Achievements.MET_BOSS)
        elif event == Events.BOSS_DEFEATED:
            self.complete_achievement(Achievements.PWN_BOSS)
    
    def complete_pwn_achievement(self, enemy_type):
        ach = None
        if enemy_type == EnemyTypes.PUMPKIN:
            ach = Achievements.PWN_PUMPKIN
        elif enemy_type == EnemyTypes.SKELETON:
            ach = Achievements.PWN_SKELLY
        elif enemy_type == EnemyTypes.GHOST:
            ach = Achievements.PWN_GHOST
        elif enemy_type == EnemyTypes.TROLL:
            ach = Achievements.PWN_OGRE
        
        if ach is not None:
            self.complete_achievement(ach)
    
    def complete_achievement(self, ach):
        services.service_locator.event_handler.publish(Events.ACHIEVEMENT, ach)
