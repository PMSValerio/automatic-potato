import pygame

from common import *
import services
import player_data

class GameState:
    def enter(self):
        pass

    def update(self, delta) -> bool:
        raise NotImplementedError

    def exit(self):
        pass

    def draw(self, surface):
        raise NotImplementedError

# --- || Title Screen State || ---

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
    
    def update(self, delta) -> bool:
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
                services.service_locator.event_handler.publish(Events.NEW_GAME_STATE, GameStates.LEVEL)
        
        return True
    
    def draw(self, surface):
        surface.fill((40, 40, 40))
        surface.blit(self.title, self.title_rect)
        if self.can_click:
            surface.blit(self.click, self.click_rect)

# --- || Character Select Screen State || ---

class CharacterSelectState(GameState):
    def __init__(self):
        self.font = pygame.font.Font("assets/font/Pokemon Classic.ttf", 16)

        self.state = -1 # -1: select character; 0 - n: select control keybind

        self.selected_skin = 0 # 0 if witch, 1 if cat
        self.skin_count = 2

        self.skin_labels = list(player_types.keys())

        self.key_binds_labels = []
        for action in player_data.player_data.key_map.keys():
            self.key_binds_labels.append(action + ": <Press any key>")
        
        self.selected_skin_panel = services.service_locator.graphics_loader.load_image("assets/gfx/skin_selected.png")
        self.chosen_skin_panel = services.service_locator.graphics_loader.load_image("assets/gfx/skin_chosen.png")
    
    def update(self, delta) -> bool:
        if self.state <= -1:
            if services.service_locator.game_input.key_pressed(pygame.K_RETURN):
                player_data.player_data.select_player_type(player_types[self.skin_labels[self.selected_skin]])
                self.state = 0
            else:
                move = 0
                if services.service_locator.game_input.key_pressed(pygame.K_RIGHT):
                    move = 1
                elif services.service_locator.game_input.key_pressed(pygame.K_LEFT):
                    move = -1
                self.selected_skin = max(0, min(self.selected_skin + move, self.skin_count - 1))
        elif self.state < len(player_data.player_data.key_map):
            pressed = services.service_locator.game_input.get_last_pressed()
            if pressed is not None:
                action = list(player_data.player_data.key_map.keys())[self.state]
                player_data.player_data.key_map[action] = pressed
                self.key_binds_labels[self.state] = action + ": " + str(pygame.key.name(pressed))

                self.state += 1
        else:
            if services.service_locator.game_input.key_pressed(pygame.K_RETURN):
                services.service_locator.event_handler.publish(Events.NEW_GAME_STATE, GameStates.LEVEL)
        
        return True

    def draw(self, surface):
        # TODO: improve code
        surface.fill((40, 40, 40))
        yline = HEIGHT * 0.25
        skin_cursor_x = (self.selected_skin+1) * WIDTH/(self.skin_count+1)

        # State specific drawing
        if self.state <= -1:
            surface.blit(self.selected_skin_panel, (skin_cursor_x-48, yline-48, 96, 96))
            self.draw_text(surface, "Select with < > - Choose with ENTER", WIDTH * 0.5, HEIGHT * 0.1)
        elif self.state < len(player_data.player_data.key_map):
            surface.blit(self.chosen_skin_panel, (skin_cursor_x-48, yline-48, 96, 96))
            self.draw_text(surface, "Control Mapping", WIDTH * 0.5, HEIGHT * 0.5)
        else:
            surface.blit(self.chosen_skin_panel, (skin_cursor_x-48, yline-48, 96, 96))
            self.draw_text(surface, "Press ENTER to start", WIDTH * 0.5, HEIGHT * 0.9)

        # Text drawing
        for i, text in enumerate(self.skin_labels):
            self.draw_text(surface, text, (i+1) * WIDTH/(self.skin_count+1), yline)
        
        yline = HEIGHT * 0.6
        for keybind in self.key_binds_labels:
            self.draw_text(surface, keybind, WIDTH * 0.5, yline)
            yline += 32

    # draw text centered on position
    def draw_text(self, surface, text_string, centerx, centery, color = (255, 255, 255)):
        rendered = self.font.render(text_string, True, color)
        rect = rendered.get_rect()
        rect.center = (centerx, centery)
        surface.blit(rendered, rect)

# --- || Game Level State || ---

class LevelState(GameState):
    def enter(self):
        from pygame import Vector2
        import player
        import boss
        import hud
        import player_data
        # initialise player and set player type
        self.hud = hud.HUD()
        services.service_locator.entity_manager.clear()
        player.Player(Vector2(WIDTH / 2, HEIGHT * 0.6))

        boss.Boss(Vector2(WIDTH * 0.5, HEIGHT))

        # win conditions
        services.service_locator.event_handler.subscribe(self, Events.BOSS_DEFEATED)

        # lose conditions
        services.service_locator.event_handler.subscribe(self, Events.NEW_HEALTH)
        services.service_locator.event_handler.subscribe(self, Events.NEW_POTIONS_LEFT)
        services.service_locator.event_handler.subscribe(self, Events.BOSS_REACH_TARGET)

        player_data.player_data.update_potions(100)

        self.end_timer = 1.5 # sec; used when game finishes
        self.ending = False
        self.paused = False

        self.end_game = 0 # 0: game still running; -1: lose; 1: win
    
    def update(self, delta) -> bool:
        import random
        from pygame import Vector2
        import test_entities

        if self.end_game != 0:
            self.finish_game(delta)

        if random.random() < 0.01:
            xx = random.randrange(0, WIDTH)
            yy = random.randrange(0, HEIGHT)
            # test_entities.Test2(Vector2(xx, yy))

        if not self.ending and services.service_locator.game_input.key_pressed(pygame.K_ESCAPE):
            self.paused = not self.paused
            services.service_locator.event_handler.publish(Events.PAUSE_UNPAUSE, self.paused)

        if not self.paused and not self.ending:
            services.service_locator.entity_manager.update_all(delta)

        return True

    def exit(self):
        services.service_locator.entity_manager.clear()
    
    def draw(self, surface):
        surface.fill((220, 220, 220))
        services.service_locator.entity_manager.draw_all(surface)

        self.hud.draw(surface)
    
    def finish_game(self, delta):
        import player_data
        if not self.ending and self.end_game > 0: # if win, add win bonus
            player_data.player_data.win = True
        self.end_timer -= delta
        self.ending = True

        if self.end_timer <= 0:
            if self.end_game < 0:
                services.service_locator.event_handler.publish(Events.NEW_GAME_STATE, GameStates.GAME_OVER)
            else:
                services.service_locator.event_handler.publish(Events.NEW_GAME_STATE, GameStates.END_RESULTS)
    
    def on_notify(self, event, arg = None):
        # win conditions
        if event == Events.BOSS_DEFEATED:
            self.end_game = 1
            print("boss was defeated")
        # lose conditions
        elif event == Events.NEW_HEALTH:
            if arg <= 0:
                self.end_game = -1
                print("player died")
        elif event == Events.NEW_POTIONS_LEFT:
            if arg <= 0:
                self.end_game = -1
                print("all potions destroyed")
        elif event == Events.BOSS_REACH_TARGET:
            self.end_game = -1
            print("boss destroyed target")

# --- || Game Over State || ---

class GameOverState(GameState):
    def __init__(self):
        import pygame
        self.timer_count = 0
        self.timer = 0.1
        self.title_font = pygame.font.Font("assets/font/Pokemon Classic.ttf", 32)
        self.to_write = "--GAME OVER--"
        self.written = ""

        self.title = self.title_font.render("", True, (255, 255, 255))
        self.title_rect = self.title.get_rect()

        self.can_click = False
    
    def update(self, delta) -> bool:
        self.timer_count += delta
        if self.timer_count >= self.timer:
            self.timer_count = 0
            if self.to_write == "":
                self.can_click = True
            else:
                self.to_write, self.written = self.to_write[1:], self.written + self.to_write[0]
                self.title = self.title_font.render(self.written, True, (255, 255, 255) if self.to_write != "" else (200, 0, 0))
                self.title_rect = self.title.get_rect()
                self.title_rect.center = (WIDTH * 0.5, HEIGHT * 0.5)
        
        if self.can_click:
            if services.service_locator.game_input.any_down():
                services.service_locator.event_handler.publish(Events.NEW_GAME_STATE, GameStates.END_RESULTS)
        
        return True
    
    def draw(self, surface):
        surface.fill((40, 40, 40))
        surface.blit(self.title, self.title_rect)

# --- || Results Screen || ---

class ResultsState(GameState):
    def __init__(self):
        import player_data

        self.font = pygame.font.Font("assets/font/Pokemon Classic.ttf", 16)

        self.timer_count = 0
        self.timer = 0.4

        xoffset1 = 32
        xoffset2 = WIDTH * 0.45
        yoffset = WIDTH * 0.2
        current_y = yoffset
        y_step = 32

        self.state = -1

        self.font_big = pygame.font.Font("assets/font/Pokemon Classic.ttf", 24)
        self.title = self.font_big.render("FINAL RESULTS", True, (255, 255, 255))
        self.title_rect = self.title.get_rect()
        self.title_rect.left = xoffset1
        self.title_rect.top = xoffset1

        # measures to be accounted to score
        self.measures_value = [
            player_data.player_data.potions_left,
            player_data.player_data.score,
            1
        ]
        self.measures = [
            "Potions Remaining: " + str(player_data.player_data.potions_left),
            "Score: " + str(player_data.player_data.score),
            "WIN BONUS" if player_data.player_data.win else "LOSE PENALTY"
        ]
        # these values are multiplied to their corresponding measures
        self.weights = [
            5,
            1,
            100 if player_data.player_data.win else -100
        ]

        self.rendered = []

        for measure in self.measures:
            rendered, rect = self.get_rendered_text(measure)
            rect.left = xoffset1
            rect.centery = current_y
            self.rendered.append((rendered, rect))
            current_y += y_step
        current_y = yoffset
        for weight in self.weights:
            rendered, rect = self.get_rendered_text("x" + str(weight))
            rect.right = xoffset2
            rect.centery = current_y
            self.rendered.append((rendered, rect))
            current_y += y_step
        
        total = sum([z[0] * z[1] for z in zip(self.measures_value, self.weights)])
        self.total = self.font_big.render("TOTAL: " + str(total), True, (255, 255, 255))
        self.total_rect = self.total.get_rect()
        self.total_rect.left = xoffset1
        self.total_rect.centery = current_y + y_step * 2

    def update(self, delta):
        if self.timer_count >= self.timer and self.timer > 0:
            self.timer_count = 0
            self.state += 1
            if self.state == len(self.measures):
                self.timer = 0.6
            elif self.state == len(self.measures) + 1:
                self.timer = 0.2
                # TODO: animation?
        else:
            self.timer_count += delta
        
        if self.state >= len(self.measures) + 2:
            if services.service_locator.game_input.any_down():
                return False
        
        return True
    
    def draw(self, surface):
        surface.fill((40, 40, 40))

        surface.blit(self.title, self.title_rect)

        # vv cursed code vv
        for i in range(len(self.measures)):
            if i > self.state:
                break
            surface.blit(self.rendered[i][0], self.rendered[i][1])
            surface.blit(self.rendered[i + len(self.measures)][0], self.rendered[i + len(self.measures)][1])

        
        if self.state > len(self.measures):
            surface.blit(self.total, self.total_rect)

    def get_rendered_text(self, text_string, color = (255, 255, 255)):
        rendered = self.font.render(text_string, True, color)
        rect = rendered.get_rect()

        return rendered, rect

class GameStateMachine:
    def __init__(self, states : dict, init_state : GameState):
        self.current_state : GameState = init_state
        self.current_state.enter()

        self.states = states

        services.service_locator.event_handler.subscribe(self, Events.NEW_GAME_STATE)
    
    def on_notify(self, event, arg):
        if event == Events.NEW_GAME_STATE:
            if arg in self.states:
                self.current_state.exit()
                self.current_state = self.states[arg]
                self.current_state.enter()
