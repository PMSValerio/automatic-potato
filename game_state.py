from common import *
import services

class GameState:
    def enter(self):
        pass

    def update(self, delta):
        raise NotImplementedError

    def exit(self):
        pass

    def draw(self, surface):
        raise NotImplementedError


class TitleState(GameState):
    def __init__(self):
        import pygame
        self.timer_count = 0
        self.timer = 0.04
        self.click_font = pygame.font.Font("assets/font/Pokemon Classic.ttf", 16)
        self.title_font = pygame.font.Font("assets/font/Pokemon Classic.ttf", 48)
        self.to_write = "Automatic Potato"
        self.written = ""

        self.click = self.click_font.render("Click to Start", True, (255, 255, 255))
        self.click_rect = self.click.get_rect()
        self.click_rect.center = (WIDTH / 2, HEIGHT * 0.8)
        self.title = self.title_font.render("", True, (255, 255, 255))
        self.title_rect = self.title.get_rect()

        self.can_click = False
    
    def update(self, delta):
        import pygame
        self.timer_count += delta
        if self.timer_count >= self.timer:
            self.timer_count = 0
            if self.to_write == "":
                self.can_click = True
            else:
                self.to_write, self.written = self.to_write[1:], self.written + self.to_write[0]
                self.title = self.title_font.render(self.written, True, (255, 255, 255))
                self.title_rect = self.title.get_rect()
                self.title_rect.center = (WIDTH / 2, HEIGHT * 0.3)
                if self.to_write == "":
                    self.timer = 0.7
        
        if self.can_click:
            if pygame.mouse.get_pressed()[0]:
                services.service_locator.event_handler.publish("new_game_state", GameStates.LEVEL)
        
    def draw(self, surface):
        surface.fill((40, 40, 40))
        surface.blit(self.title, self.title_rect)
        if self.can_click:
            surface.blit(self.click, self.click_rect)


class LevelState(GameState):
    def enter(self):
        from pygame import Vector2
        import player
        services.service_locator.entity_manager.clear()
        player.Player(Vector2(WIDTH / 2, HEIGHT / 2), witch_stats)
    
    def update(self, delta):
        import random
        from pygame import Vector2
        import test_entities

        if random.random() < 0.01:
            xx = random.randrange(0, WIDTH)
            yy = random.randrange(0, HEIGHT)
            test_entities.Test2(Vector2(xx, yy))

        services.service_locator.entity_manager.update_all(delta)

    def exit(self):
        services.service_locator.entity_manager.clear()
    
    def draw(self, surface):
        surface.fill((220, 220, 220))
        services.service_locator.entity_manager.draw_all(surface)


class GameStateMachine:
    def __init__(self, states : dict, init_state : GameState):
        self.current_state : GameState = init_state
        self.current_state.enter()

        self.states = states

        services.service_locator.event_handler.subscribe(self, "new_game_state")
    
    def on_notify(self, event, arg):
        if event == "new_game_state":
            if arg in self.states:
                self.current_state.exit()
                self.current_state = self.states[arg]
                self.current_state.enter()
