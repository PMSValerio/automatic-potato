import common.py
from services import service_locator

# class holds all persistent player information, relevant in multiple game states (player stats, score, )
class PlayerData:
    def __init__(self):
        self.player_type = None
        self.score = 0
    
    # update player score and notify all subscribed entities (ex: UI)
    def update_score(self, delta):
        self.score += delta
        service_locator.event_handler.publish("new_score", self.score)
