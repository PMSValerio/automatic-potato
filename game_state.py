import pygame

from common import *
from gui_utils import *
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
        import animation

        self.timer_count = 0
        self.timer = 0.2
        self.to_write = "Automatic Potato"
        self.written = ""

        # in-game text labels
        self.click_text = TextLabel("Press ENTER: Start Game", WIDTH * 0.5, HEIGHT * 0.85, Align.CENTER, Align.CENTER, 16)
        self.click_text2 = TextLabel("Press SPACE: Achievements", WIDTH * 0.5, HEIGHT * 0.9, Align.CENTER, Align.CENTER, 16)
        self.title_text = TextLabel("Automatic Potato", WIDTH * 0.5, HEIGHT * 0.25, Align.CENTER, Align.CENTER, 48)

        # background animation
        self.cauldron = animation.Animation("assets/gfx/ui/title_cauldron.png", True, 6)

        # fade effect
        self.fade_panel = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA).convert_alpha()
        self.fade_panel.fill((20, 20, 20))
    

    def enter(self):
        services.service_locator.sound_mixer.play_music(Music.TITLE)
        self.can_click = False
        self.fade_alpha = 255 # make panel fully opaque
    

    def update(self, delta) -> bool:
        import pygame

        self.cauldron.update_frame()

        # gradually fade in by reducing panel alpha
        if self.fade_alpha > 0:
            self.fade_alpha = max(0, self.fade_alpha - 1)
            self.fade_panel.set_alpha(self.fade_alpha)
        
        # slight delay before text appears
        else:
            if self.timer_count >= self.timer:
                self.can_click = True
            else:
                self.timer_count += delta
        
        if self.can_click:
            if services.service_locator.game_input.key_pressed(pygame.K_RETURN):
                services.service_locator.event_handler.publish(Events.NEW_GAME_STATE, GameStates.CHARACTER_SELECT)
            elif services.service_locator.game_input.key_pressed(pygame.K_SPACE):
                services.service_locator.event_handler.publish(Events.NEW_GAME_STATE, GameStates.ACHIEVEMENTS)
        # skip animation
        else:
            if services.service_locator.game_input.any_pressed():
                self.fade_alpha = 0
        
        return True
    

    def draw(self, surface):
        surface.fill((40, 40, 45))

        # draw title and animation
        self.title_text.draw(surface)
        im = self.cauldron.get_frame()
        rect = im.get_rect(center = (WIDTH * 0.5, HEIGHT * 0.55))
        surface.blit(im, rect)

        if self.fade_alpha > 0: # only draw panel if not totally invisible
            surface.blit(self.fade_panel, self.fade_panel.get_rect())
        if self.can_click:
            self.click_text.draw(surface)
            self.click_text2.draw(surface)


# --- || Character Select Screen State || ---
class CharacterSelectState(GameState):
    def __init__(self):
        self.state = -1 # -1: select character; 0 - n: select control keybind

        self.selected_skin = 0 # 0 if witch; 1 if cat
        self.skin_count = 2

        self.skin_labels = list(player_types.keys()) # skin names

        # player set controls
        self.key_binds_labels = []
        for action in player_data.player_data.key_map.keys():
            self.key_binds_labels.append(action + ": <Press any key>")
        
        # ui panels
        self.selected_skin_panel = services.service_locator.graphics_loader.load_image("assets/gfx/skin_selected.png")
        self.chosen_skin_panel = services.service_locator.graphics_loader.load_image("assets/gfx/skin_chosen.png")

        self.text_label = TextLabel("", 0, 0, Align.CENTER, Align.CENTER, 16)
    

    def enter(self):
        services.service_locator.sound_mixer.play_music(Music.TITLE)
    

    def update(self, delta) -> bool:

        # selecting skin
        if self.state <= -1:
            if services.service_locator.game_input.key_pressed(pygame.K_RETURN): # confirm skin
                player_data.player_data.select_player_type(player_types[self.skin_labels[self.selected_skin]])
                self.state = 0
            else: # navigate skins
                move = 0
                if services.service_locator.game_input.key_pressed(pygame.K_RIGHT):
                    move = 1
                elif services.service_locator.game_input.key_pressed(pygame.K_LEFT):
                    move = -1
                self.selected_skin = max(0, min(self.selected_skin + move, self.skin_count - 1))

        # selecting controls
        elif self.state < len(player_data.player_data.key_map):
            pressed = services.service_locator.game_input.get_last_pressed() # sequentially assign first key pressed key to current action
            if pressed is not None:
                action = list(player_data.player_data.key_map.keys())[self.state]
                player_data.player_data.key_map[action] = pressed
                self.key_binds_labels[self.state] = action + ": " + str(pygame.key.name(pressed))

                self.state += 1

        # awaiting player input to start
        else:
            if services.service_locator.game_input.key_pressed(pygame.K_RETURN):
                services.service_locator.event_handler.publish(Events.NEW_GAME_STATE, GameStates.LEVEL)
        
        return True


    def draw(self, surface):
        surface.fill((40, 40, 40))
        yline = HEIGHT * 0.25
        skin_cursor_x = (self.selected_skin+1) * WIDTH/(self.skin_count+1)

        # State specific instructions drawing
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
    def draw_text(self, surface, text_string, centerx, centery):
        self.text_label.set_text(text_string, centerx, centery)
        self.text_label.draw(surface)


# --- || Game Level State || ---
class LevelState(GameState):
    def __init__(self):
        import hud
        import animation

        self.hud = hud.HUD()

        self.background = animation.Animation("assets/gfx/ui/background.png", True, 4)

        # win conditions
        services.service_locator.event_handler.subscribe(self, Events.BOSS_DEFEATED)

        # lose conditions
        services.service_locator.event_handler.subscribe(self, Events.NEW_HEALTH)
        services.service_locator.event_handler.subscribe(self, Events.NEW_POTIONS_LEFT)
        services.service_locator.event_handler.subscribe(self, Events.BOSS_REACH_TARGET)

        self.end_timer = 1.5 # sec; used when game finishes
        self.ending = False # waiting for lose delay to end
        self.paused = False

        # game running status
        self.end_game = 0 # 0: game still running; -1: lose; 1: win


    def enter(self):
        from pygame import Vector2
        import player
        import player_data
        import pickups

        services.service_locator.sound_mixer.play_music(Music.LEVEL)
        services.service_locator.entity_manager.clear()

        # manually spawn player
        player.Player(Vector2(WIDTH / 2, HEIGHT * 0.6))

        #pickups.WeaponPickup(Vector2(WIDTH * 0.5, HEIGHT * 0.3))

        # set initial potions
        player_data.player_data.update_potions(20)
    

    def update(self, delta) -> bool:
        import random

        # if game end condition is met, enter finish routine
        if self.end_game != 0:
            self.finish_game(delta)

        # pause/unpause
        if not self.ending and services.service_locator.game_input.key_pressed(pygame.K_ESCAPE):
            self.paused = not self.paused
            services.service_locator.event_handler.publish(Events.PAUSE_UNPAUSE, self.paused)

        # update entities only if not paused
        if not self.paused and not self.ending:
            services.service_locator.entity_manager.update_all(delta)
        
        self.hud.update(delta)
        services.service_locator.enemy_handler.update(delta)

        return True


    def exit(self):
        services.service_locator.entity_manager.clear()
    

    def draw(self, surface):
        # background animation
        surface.fill((220, 220, 220))
        image = self.background.get_frame().copy()
        surface.blit(image, image.get_rect())
        self.background.update_frame()

        # draw all entities regardless of pause
        services.service_locator.entity_manager.draw_all(surface)

        self.hud.draw(surface)
    
    # freeze game for a while before ending
    def finish_game(self, delta):
        import player_data
        if not self.ending:
            services.service_locator.sound_mixer.stop_music()
            if self.end_game > 0:  # if win, add win bonus
                player_data.player_data.win = True
                services.service_locator.sound_mixer.play_music(Music.WIN)
            else:
                services.service_locator.sound_mixer.play_music(Music.GAME_OVER)
        self.end_timer -= delta
        self.ending = True


        # decide next state based on whether the player beat the game or died
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

        self.title = TextLabel("", WIDTH * 0.5, HEIGHT * 0.5, Align.CENTER, Align.CENTER, 32)

        self.can_click = False
    

    # gradually write more letters
    def update(self, delta) -> bool:
        self.timer_count += delta
        if self.timer_count >= self.timer:
            self.timer_count = 0
            if self.to_write == "":
                self.can_click = True
            else:
                self.to_write, self.written = self.to_write[1:], self.written + self.to_write[0]
                self.title.set_text(self.written)
                if self.to_write == "":
                    self.title.set_colour((200, 0, 0))
        
        if self.can_click:
            if services.service_locator.game_input.any_pressed():
                services.service_locator.event_handler.publish(Events.NEW_GAME_STATE, GameStates.END_RESULTS)
        
        return True
    

    def draw(self, surface):
        surface.fill((40, 40, 40))
        self.title.draw(surface)



# --- || Results Screen || ---
class ResultsState(GameState):
    def __init__(self):
        self.timer_count = 0
        self.timer = 0.4

        self.xoffset1 = 32
        self.xoffset2 = WIDTH * 0.45
        self.yoffset = WIDTH * 0.2
        self.y_step = 32

        self.state = -1
        self.title = TextLabel("FINAL RESULTS", self.xoffset1, self.xoffset1, Align.BEGIN, Align.BEGIN, 24)

        self.measures_value = []
        self.measures = []
        self.weights = []

        self.list_item = TextLabel("", 0, 0, Align.CENTER, Align.BEGIN, 16)
    

    def enter(self):
        # measures values to be accounted to score
        self.measures_value = [
            player_data.player_data.potions_left,
            player_data.player_data.score,
            1
        ]

        # measures labels to be displayed
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

        # final score calculations
        total = sum([z[0] * z[1] for z in zip(self.measures_value, self.weights)])
        self.total = TextLabel("TOTAL: " + str(total), self.xoffset1, self.yoffset + self.y_step * (len(self.measures) + 2), Align.CENTER, Align.BEGIN, 24)
        player_data.player_data.score = total # update score with final result


    def update(self, delta):
        # delays between each metric shows
        if self.timer_count >= self.timer and self.timer > 0:
            self.timer_count = 0
            self.state += 1
            if self.state == len(self.measures):
                self.timer = 0.6
            elif self.state == len(self.measures) + 1:
                self.timer = 0.2
        else:
            self.timer_count += delta
        
        # at the end, await player input
        if self.state >= len(self.measures) + 2:
            if services.service_locator.game_input.any_pressed():
                services.service_locator.event_handler.publish(Events.NEW_GAME_STATE, GameStates.SCOREBOARD)
        
        return True
    

    def draw(self, surface):
        surface.fill((40, 40, 40))

        self.title.draw(surface)

        current_y = self.yoffset

        # cycle through and draw all measures and weights in appropriate positions
        for i in range(len(self.measures)):
            if i > self.state:
                break
            self.list_item.set_text(self.measures[i], self.xoffset1, current_y)
            self.list_item.draw(surface)

            self.list_item.set_text(("x" if i < len(self.measures) - 1 else "") + str(self.weights[i]), self.xoffset2, current_y)
            self.list_item.draw(surface)

            current_y += self.y_step

        
        if self.state > len(self.measures):
            self.total.draw(surface)



# --- || Scoreboard State || ---
class ScoreboardState(GameState):
    def __init__(self):
        self.scoreboard = {}

        # player's place on scoreboard, -1 if below 10th
        self.player_index = -1
        self.editing = False

        # ui elements
        self.title = TextLabel("SCOREBOARD", WIDTH * 0.5, BLOCK, Align.BEGIN, Align.CENTER, 48)
        self.record = TextLabel("", 0, 0, Align.CENTER, Align.BEGIN, 24)
        self.footnote = TextLabel("Edit name with arrow keys, confirm with ENTER", WIDTH * 0.5, HEIGHT - BLOCK, Align.CENTER, Align.CENTER, 16)

        # positions for ui
        self.column1 = WIDTH * 0.2
        self.column2 = WIDTH * 0.6
        self.yoffset = BLOCK * 6
        self.y_step = 80

        # available name symbols and cursors
        self.characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ.!?- "
        self.selected_char = 0 # selected symbol
        self.name_cursor = 0 # position in the three letter name

        # ui elements for name inputting
        self.new_entry_panel = services.service_locator.graphics_loader.load_image("assets/gfx/score_panel.png")
        self.cursor_texture = services.service_locator.graphics_loader.load_image("assets/gfx/cursor.png")


    def enter(self):
        # load scoreboard data
        import json
        filepath = os.path.join(OG_PATH, "data/scoreboard.json")
        if not os.path.exists(filepath):
            filepath = get_asset("json/default_scoreboard.json")

        with open(filepath) as fin:
            self.scoreboard = json.load(fin, parse_int=int)
        
        # check if player is in top ten and update table if so
        score = player_data.player_data.score
        player_in_table = False
        entry = ["xxx", -1] # default, should never need to be used
        for i in range(len(self.scoreboard)):
            if player_in_table:
                new_entry = self.scoreboard[str(i)]
                self.scoreboard[str(i)] = entry
                entry = new_entry
            else:
                entry = self.scoreboard[str(i)]
                if score > entry[1]: # player beat this score, takes its place
                    self.scoreboard[str(i)] = ["---", score]
                    player_in_table = True
                    self.player_index = i
                    self.editing = True
    

    def exit(self):
        # save scoreboard data
        import json
        with open(os.path.join(OG_PATH, "data/scoreboard.json"), mode = "w") as fout:
            json.dump(self.scoreboard, fout)
    

    def update(self, delta):
        if not self.editing and services.service_locator.game_input.any_pressed():
            return False
        
        if self.player_index >= 0 and self.editing: # select name
            old_name = self.scoreboard[str(self.player_index)][0]

            # select letter
            if services.service_locator.game_input.key_pressed(pygame.K_DOWN):
                self.selected_char = (self.selected_char + 1) % len(self.characters)
            elif services.service_locator.game_input.key_pressed(pygame.K_UP):
                self.selected_char = self.selected_char -1 if self.selected_char > 0 else len(self.characters) - 1
            # change cursor position
            elif services.service_locator.game_input.key_pressed(pygame.K_LEFT):
                self.name_cursor = max(0, self.name_cursor - 1)
                self.selected_char = self.characters.find(old_name[self.name_cursor])
            elif services.service_locator.game_input.key_pressed(pygame.K_RIGHT):
                self.name_cursor = min(2, self.name_cursor + 1)
                self.selected_char = self.characters.find(old_name[self.name_cursor])
            # confirm name
            elif services.service_locator.game_input.key_pressed(pygame.K_RETURN):
                self.editing = False
            
            # update name
            old_name = self.scoreboard[str(self.player_index)][0]
            old_name = old_name[:self.name_cursor] + self.characters[self.selected_char] + old_name[self.name_cursor + 1:]
            self.scoreboard[str(self.player_index)][0] = old_name

        return True
    

    def draw(self, surface):
        surface.fill((40, 40, 40))
        self.title.draw(surface)

        ix = 0
        half_len = len(self.scoreboard) / 2
        # draw all scores
        for rank, stats in self.scoreboard.items():
            self.record.set_text(stats[0] + ": " + str(stats[1]), self.column1 if ix < half_len else self.column2, self.yoffset + self.y_step * (ix % half_len))
            
            # if this is player position and still editing name, draw cursors
            if ix == self.player_index and self.editing:
                rect = self.new_entry_panel.get_rect()
                rect.center = self.record.rect.center
                surface.blit(self.new_entry_panel, rect)

                rect = self.cursor_texture.get_rect()
                rect.top = self.record.rect.top + 16
                rect.left = self.record.rect.left + (24 * self.name_cursor)
                surface.blit(self.cursor_texture, rect)

                self.footnote.draw(surface)
            self.record.draw(surface)
            ix += 1



# --- || Achievements Screen State || ---
class AchievementsState(GameState):
    def __init__(self):

        # ui positions
        self.column1 = WIDTH * 0.03
        self.column2 = WIDTH * 0.53
        self.yoffset = HEIGHT * 0.4
        self.y_step = 64

        # ui elements
        self.title = TextLabel("ACHIEVEMENTS", WIDTH * 0.5, BLOCK, Align.CENTER, Align.CENTER, 32)
        self.footnote = TextLabel("Press any key to return to title", WIDTH * 0.5, HEIGHT - BLOCK, Align.CENTER, Align.CENTER, 16)

        # name and text for each achievement
        self.name_label = TextLabel("", 0, 0, Align.CENTER, Align.BEGIN, 16)
        self.text_label = TextLabel("", 0, 0, Align.CENTER, Align.BEGIN, 16, (180, 180, 180))
    

    def update(self, delta):
        # if input return to title
        if services.service_locator.game_input.any_pressed():
            services.service_locator.event_handler.publish(Events.NEW_GAME_STATE, GameStates.TITLE_SCREEN)
        return True


    def draw(self, surface):
        surface.fill((40, 40, 40))

        self.title.draw(surface)
        self.footnote.draw(surface)

        ix = 0
        l = len(services.service_locator.achievements_tracker.achievements_data) / 2
        # draw all achievements (if not unlocked, draw ???)
        for key, ach_data in services.service_locator.achievements_tracker.achievements_data.items():
            complete = services.service_locator.achievements_tracker.progress[key]
            self.name_label.set_text(ach_data["name"] if complete else "???", self.column1 if ix < l else self.column2, self.yoffset + self.y_step * (ix % l), (255, 255, 255) if complete else (180, 180, 180))
            self.name_label.draw(surface)
            self.text_label.set_text(ach_data["text"], self.column1 if ix < l else self.column2, self.yoffset + self.y_step * (ix % l) + 24)
            self.text_label.draw(surface)
            ix += 1



class GameStateMachine:
    def __init__(self, states : dict, init_state : GameState):
        self.current_state : GameState = init_state
        self.current_state.enter()

        self.states = states

        services.service_locator.event_handler.subscribe(self, Events.NEW_GAME_STATE)
    

    # perform any necessary clean-up, mainly, call the exit method on current state
    def close(self):
        self.current_state.exit()
    
    
    def on_notify(self, event, arg):
        if event == Events.NEW_GAME_STATE:
            if arg in self.states:
                self.current_state.exit()
                self.current_state = self.states[arg]
                self.current_state.enter()
