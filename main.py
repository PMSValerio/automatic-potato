import random
import pygame as pg
from pygame import Vector2

from common import *
import services
import game_state

def main():

    # set up pygame
    pg.init()
    screen = pg.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
    pg.display.set_caption("Auto Spud")

    # set up services
    services.service_locator = services.Services.get()
    services.service_locator.setup()

    # game state machine initialisation
    states = {
        "level": game_state.LevelState()
    }
    game_machine = game_state.GameStateMachine(states, states["level"])

    # game loop
    clock = pg.time.Clock()
    running = True
    while running:
        delta_time = clock.tick(FPS) / 1000 # get time in seconds

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                running = False

        game_machine.current_state.update(delta_time)
        game_machine.current_state.draw(screen)

        pg.display.update()
    
    pg.quit()


main()