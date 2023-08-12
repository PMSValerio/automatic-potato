import json

from common import *
import services
from enemy import EnemyTypes

class AchievementTracker:
    def __init__(self):
        self.achievements_data = {}
        with open(get_asset("json/achievements.json")) as fin:
            self.achievements_data = json.load(fin)

        self.killed_enemies = {k: 0 for k in EnemyTypes}
        self.camp_timer = 0
        self.camped = False

        self.progress = {}
        filepath = os.path.join(OG_PATH, "data/achievement_tracker.json")
        if not os.path.exists(filepath):
            filepath = get_asset("json/default_cchievements.json")

        with open(filepath) as fin:
            self.progress = json.load(fin)

    def setup(self):
        services.service_locator.event_handler.subscribe(self, Events.ENEMY_KILLED)
        services.service_locator.event_handler.subscribe(self, Events.PLAYER_CAMP)
        services.service_locator.event_handler.subscribe(self, Events.BOSS_DEFEATED)
    
    def save(self):
        with open(os.path.join(OG_PATH, "data/achievement_tracker.json"), "w") as fout:
            json.dump(self.progress, fout)
    
    def update_camp_timer(self, delta):
        self.camp_timer += delta
        if self.camp_timer >= 5 and not self.camped:
            self.complete_achievement(Achievements.CAMPER)
            self.camped = True
    
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
        if not self.progress[str(ach.value)]:
            self.progress[str(ach.value)] = True
            services.service_locator.event_handler.publish(Events.ACHIEVEMENT, ach)
    
    # event callback
    def on_notify(self, event, arg):
        if event == Events.ENEMY_KILLED:
            self.killed_enemies[arg] += 1
            if self.killed_enemies[arg] == 10:
                self.complete_pwn_achievement(arg)
        elif event == Events.PLAYER_CAMP:
            self.update_camp_timer(arg)
        elif event == Events.BOSS_DEFEATED:
            self.complete_achievement(Achievements.PWN_BOSS)
