from common import *
import services

# class holds all persistent player information, relevant in multiple game states (player stats, score, ...)
class PlayerData:
    __instance = None

    def get():
        if PlayerData.__instance is None:
            PlayerData()
        return PlayerData.__instance

    def __init__(self):
        if PlayerData.__instance is not None:
            raise Exception("Singleton class already initialised")
        else:
            PlayerData.__instance = self
        
        self.player_type : PlayerStats = None
        self.score = 0

        # TODO: if there's time
        # statistics that contribute to final score
        # self.shots_fired = 0 # number of shots fired is discounted from score
        # self.health_healed = 0 # amount of health player had to heal is discounted from score
    
    def select_player_type(self, ptype : PlayerStats):
        self.player_type = ptype

    # update player score and notify all subscribed entities (ex: UI)
    def update_score(self, delta):
        self.score += delta
        services.service_locator.event_handler.publish("new_score", self.score)

# PlayerData is not included in services as it is not an engine specific system
# TODO: make sure this ^ makes sense
player_data : PlayerData = None
