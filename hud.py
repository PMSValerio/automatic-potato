from common import *
from services import service_locator

class HUD:
    def __init__(self):
        self.player_health = 0
        self.player_score = 0
        self.potions_left = 0

        # TODO:
        # self.current_wave = 0
        # self.enemies_left = 0

        service_locator.event_handler.subscribe(self, "new_health")
        service_locator.event_handler.subscribe(self, "new_score")
        service_locator.event_handler.subscribe(self, "new_potions_left")
    
    # TODO:
    def draw(self, surface):
        pass

    def on_notify(self, event, arg):
        if event == "new_health":
            self.player_health = arg
        elif event == "new_score":
            self.player_score = arg
            print("Score: " + str(self.player_score))
        elif event == "new_potions_left":
            self.potions_left = arg