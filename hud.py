import pygame

from common import *
from services import service_locator
from player_data import player_data

# offset in pixels relative to screen top-left corner (x and y)
HUD_OFFSET = 16

class HUD:
    def __init__(self):
        self.player_health = 0
        self.player_score = 0
        self.potions_left = 0

        # TODO:
        # self.current_wave = 0
        # self.enemies_left = 0

        self.healthbar_back = service_locator.graphics_loader.image_at("assets/gfx/healthbar.png", (0, 0, 128, 32))
        self.healthbar_fore = service_locator.graphics_loader.image_at("assets/gfx/healthbar.png", (0, 32, 128, 32))
        self.health_wid = 0 # width of the healthbar in pixels

        service_locator.event_handler.subscribe(self, "new_health")
        service_locator.event_handler.subscribe(self, "new_score")
        service_locator.event_handler.subscribe(self, "new_potions_left")
    
    # TODO:
    def draw(self, surface):
        surface.blit(self.healthbar_back, (HUD_OFFSET, HUD_OFFSET, 128, 32))
        scaled = pygame.transform.scale(self.healthbar_fore, (self.health_wid, 32))
        surface.blit(scaled, (HUD_OFFSET, HUD_OFFSET, self.health_wid, 32))

    def on_notify(self, event, arg):
        if event == "new_health":
            self.player_health = arg
            self.health_wid = max(0, (128 * self.player_health) / player_data.player_type.max_health)
            print(self.health_wid)
        elif event == "new_score":
            self.player_score = arg
            print("Score: " + str(self.player_score))
        elif event == "new_potions_left":
            self.potions_left = arg