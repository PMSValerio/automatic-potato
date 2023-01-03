import pygame

from common import *
from gui_utils import *
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


        self.potion_icon = service_locator.graphics_loader.get_anim_strip("assets/gfx/ui/icons.png", "potion", 0)
        self.potions = TextLabel("x0", WIDTH * 0.5, HUD_OFFSET * 1.5, Align.CENTER, Align.CENTER, 16)

        self.score = TextLabel("SCORE: " + str(self.player_score), WIDTH * 0.7, HUD_OFFSET * 1.5, Align.BEGIN, Align.BEGIN, 16)

        self.paused = False
        self.pause_label = TextLabel("--GAME PAUSED--", WIDTH * 0.5, HEIGHT * 0.9, Align.CENTER, Align.CENTER, 16)


        self.achievement_panel = AchievementNotification()

        service_locator.event_handler.subscribe(self, Events.NEW_HEALTH)
        service_locator.event_handler.subscribe(self, Events.NEW_SCORE)
        service_locator.event_handler.subscribe(self, Events.NEW_POTIONS_LEFT)
        service_locator.event_handler.subscribe(self, Events.PAUSE_UNPAUSE)
        service_locator.event_handler.subscribe(self, Events.ACHIEVEMENT)
    
    def update(self, delta):
        self.achievement_panel.update(delta)

    def draw(self, surface):
        surface.blit(self.healthbar_back, (HUD_OFFSET, HUD_OFFSET, 128, 32))
        scaled = pygame.transform.scale(self.healthbar_fore, (self.health_wid, 32))
        surface.blit(scaled, (HUD_OFFSET, HUD_OFFSET, self.health_wid, 32))

        self.potions.set_text("x" + str(self.potions_left))
        self.potions.draw(surface)
        rect = self.potion_icon.get_rect()
        rect.right = self.potions.rect.left
        rect.centery = self.potions.rect.centery
        surface.blit(self.potion_icon, rect)

        self.score.set_text("SCORE: " + str(self.player_score))
        self.score.draw(surface)

        if self.paused:
            self.pause_label.draw(surface)
        
        self.achievement_panel.draw(surface)

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
        elif event == Events.ACHIEVEMENT:
            self.achievement_panel.turn_on(service_locator.achievements_tracker.achievements_data[str(arg.value)]["name"])
            