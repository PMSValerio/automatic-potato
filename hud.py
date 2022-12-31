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

        self.font = pygame.font.Font("assets/font/Pokemon Classic.ttf", 16)

        self.potions = self.font.render("x0", True, (255, 255, 255))
        self.potions_rect = self.potions.get_rect()

        self.score = self.font.render("SCORE: %s" % self.player_score, True, (255, 255, 255))
        self.score_rect = self.score.get_rect()

        self.paused = False
        self.pause_label = self.font.render("--GAME PAUSED--", True, (255, 255, 255))
        self.pause_rect = self.pause_label.get_rect()
        self.pause_rect.center = (WIDTH * 0.5, HEIGHT * 0.9)

        service_locator.event_handler.subscribe(self, Events.NEW_HEALTH)
        service_locator.event_handler.subscribe(self, Events.NEW_SCORE)
        service_locator.event_handler.subscribe(self, Events.NEW_POTIONS_LEFT)
        service_locator.event_handler.subscribe(self, Events.PAUSE_UNPAUSE)
    
    # TODO:
    def draw(self, surface):
        surface.blit(self.healthbar_back, (HUD_OFFSET, HUD_OFFSET, 128, 32))
        scaled = pygame.transform.scale(self.healthbar_fore, (self.health_wid, 32))
        surface.blit(scaled, (HUD_OFFSET, HUD_OFFSET, self.health_wid, 32))

        self.potions = self.font.render("x%s" % self.potions_left, True, (255, 255, 255))
        self.potions_rect = self.potions.get_rect()
        self.potions_rect.center = (WIDTH * 0.5, HUD_OFFSET * 1.5)
        surface.blit(self.potions, self.potions_rect)

        self.score = self.font.render("SCORE: %s" % self.player_score, True, (255, 255, 255))
        self.score_rect = self.score.get_rect()
        self.score_rect.left = WIDTH * 0.7
        self.score_rect.top = HUD_OFFSET * 1.5
        surface.blit(self.score, self.score_rect)

        if self.paused:
            surface.blit(self.pause_label, self.pause_rect)

    def on_notify(self, event, arg):
        if event == Events.NEW_HEALTH:
            self.player_health = arg
            self.health_wid = max(0, (128 * self.player_health) / player_data.player_type.max_health)
        elif event == Events.NEW_SCORE:
            self.player_score = arg
        elif event == Events.NEW_POTIONS_LEFT:
            self.potions_left = arg
        elif event == Events.PAUSE_UNPAUSE:
            self.paused = arg