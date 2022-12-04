from enum import Enum
import pygame
from pygame import Vector2

from common import *
from services import service_locator
from entity import Entity
from fsm import FSM

class States(Enum):
    IDLE = 0
    MOVING = 1

class PlayerStats:
    def __init__(self, max_health, base_speed):
        self.max_health = max_health # max hp
        self.speed = base_speed # pix/sec

witch_stats = PlayerStats(10, 80)
cat_stats = PlayerStats(8, 100)

class Player(Entity):
    def __init__(self, pos, stats : PlayerStats):
        Entity.__init__(self, pos, EntityLayers.PLAYER)

        self.colour = (0, 255, 0) # temporary colour to indicate state

        self.move_dir : Vector2 = Vector2(0, 0) # different from dir, only controls movement dir

        self.stats = stats

        self.fsm = FSM()
        self.fsm.add_state(States.IDLE, self.idle, True)
        self.fsm.add_state(States.MOVING, self.moving)

        self.action_map = {
            "move_left": pygame.K_a,
            "move_right": pygame.K_d,
            "move_up": pygame.K_w,
            "move_down": pygame.K_s,
        }
    
    def update(self, delta):
        # TODO: change to use commands instead
        self.move_dir = Vector2(0, 0)
        if service_locator.game_input.key_down(pygame.K_a):
            self.add_to_move_dir(Directions.LEFT)
        if service_locator.game_input.key_down(pygame.K_d):
            self.add_to_move_dir(Directions.RIGHT)
        if service_locator.game_input.key_down(pygame.K_w):
            self.add_to_move_dir(Directions.UP)
        if service_locator.game_input.key_down(pygame.K_s):
            self.add_to_move_dir(Directions.DOWN)
        if self.move_dir.length() > 0:
            self.move_dir = self.move_dir.normalize()

        self.fsm.update()

        self.update_bbox()

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)
    
    def check_action(self, action, just_pressed = False):
        if just_pressed:
            return service_locator.game_input.key_pressed(self.action_map)
    
    def add_to_move_dir(self, new_dir):
        self.move_dir.x += new_dir.value[0]
        self.move_dir.y += new_dir.value[1]

    # --- || State Callbacks || ---
    
    def idle(self, new = False):
        if new:
            self.colour = (0, 255, 0)
        
        if self.move_dir.length() != 0:
            self.fsm.change_state(States.MOVING)

    def moving(self, new = False):
        if new:
            self.colour = (255, 255, 0)
        
        if self.move_dir.length() == 0:
            self.fsm.change_state(States.IDLE)
