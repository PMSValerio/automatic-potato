import random
import pygame as pg
from common import *
import gui_utils
import services
import player_data
import game_state

def main():
    dirpath = os.path.join(OG_PATH, "data")
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)

    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)

    # set up pygame
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Auto Spud")

    # set up services
    services.service_locator = services.Services.get()
    services.service_locator.setup()

    gui_utils.load_fonts()

    # set up player data
    player_data.player_data = player_data.PlayerData.get()

    # game state machine initialisation
    states = {
        GameStates.TITLE_SCREEN: game_state.TitleState(),
        GameStates.CHARACTER_SELECT: game_state.CharacterSelectState(),
        GameStates.LEVEL: game_state.LevelState(),
        GameStates.GAME_OVER: game_state.GameOverState(),
        GameStates.END_RESULTS: game_state.ResultsState(),
        GameStates.SCOREBOARD: game_state.ScoreboardState(),
        GameStates.ACHIEVEMENTS: game_state.AchievementsState(),
    }

    game_machine = game_state.GameStateMachine(states, states[GameStates.TITLE_SCREEN])
    
    # game loop
    clock = pg.time.Clock()
    running = True
    while running:
        delta_time = clock.tick(FPS) / 1000 # get time in seconds

        running = services.service_locator.game_input.update(delta_time)
        running = running and game_machine.current_state.update(delta_time)
        game_machine.current_state.draw(screen)

        pg.display.update()

    services.service_locator.achievements_tracker.save()
    game_machine.close()

    pg.quit()


main()