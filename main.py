import random
import pygame as pg
from pygame import Vector2

from common import *
import services
import player_data
import game_state

def main():

    # set up pygame
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Auto Spud")

    # set up services
    services.service_locator = services.Services.get()
    services.service_locator.setup()

    # set up player data
    player_data.player_data = player_data.PlayerData.get()


    # game state machine initialisation
    states = {
        GameStates.TITLE_SCREEN: game_state.TitleState(),
        GameStates.CHARACTER_SELECT: game_state.CharacterSelectState(),
        GameStates.LEVEL: game_state.LevelState()
    }
    game_machine = game_state.GameStateMachine(states, states[GameStates.CHARACTER_SELECT])

    # game loop
    clock = pg.time.Clock()
    running = True
    while running:
        delta_time = clock.tick(FPS) / 1000 # get time in seconds

        running = services.service_locator.game_input.update(delta_time)
        running = running and game_machine.current_state.update(delta_time)
        game_machine.current_state.draw(screen)

        pg.display.update()
    
    pg.quit()


main()