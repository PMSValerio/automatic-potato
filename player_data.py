import pygame

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
        
        self.player_type : PlayerStats = player_types["Witch"]

        self.key_map = {
            "move_left": pygame.K_a,
            "move_right": pygame.K_d,
            "move_up": pygame.K_w,
            "move_down": pygame.K_s,
            "shoot": pygame.K_p,
        }

        self.score = 250
        self.potions_left = 0

        self.win = False
        # TODO: if there's time
        # statistics that contribute to final score
        # self.shots_fired = 0 # number of shots fired is discounted from score
        # self.health_healed = 0 # amount of health player had to heal is discounted from score
    
    def select_player_type(self, ptype : PlayerStats):
        self.player_type = ptype

    def update_position(self, position):
        self.pos = position

    def get_player_pos(self):
        return self.pos

    # update player score and notify all subscribed entities (ex: UI)
    def update_score(self, delta):
        self.score += delta
        services.service_locator.event_handler.publish(Events.NEW_SCORE, self.score)
    
    def update_potions(self, delta):
        self.potions_left += delta
        services.service_locator.event_handler.publish(Events.NEW_POTIONS_LEFT, self.potions_left)

player_data : PlayerData = None
