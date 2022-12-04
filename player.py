from enum import Enum
import pygame
from pygame import Vector2

from common import *
from services import service_locator
from entity import Entity
from graphics import Animation

from fsm import FSM
from player_commands import *

class States(Enum):
    IDLE = 0
    MOVING = 1

class PlayerStats:
    def __init__(self, max_health, base_speed):
        self.max_health = max_health # max hp
        self.speed = base_speed # pix/sec

witch_stats = PlayerStats(10, 160)
cat_stats = PlayerStats(8, 200)

class Player(Entity):
    def __init__(self, pos, stats : PlayerStats):
        Entity.__init__(self, pos, EntityLayers.PLAYER)

        self.colour = (0, 255, 0) # temporary colour to indicate state

        self.move_force : Vector2 = Vector2(0, 0) # different from dir, only controls movement dir

        self.stats = stats

        self.fsm = FSM()
        self.fsm.add_state(States.IDLE, self.idle, True)
        self.fsm.add_state(States.MOVING, self.moving)

        self.key_map = {
            "move_left": pygame.K_a,
            "move_right": pygame.K_d,
            "move_up": pygame.K_w,
            "move_down": pygame.K_s,
        }
        self.command_map = {
            "move_left": MoveLeft(),
            "move_right": MoveRight(),
            "move_up": MoveUp(),
            "move_down": MoveDown(),
        }

        self.graphics = Animation("assets/gfx/player.png", 32, 32, True, 5) # animation object
        self.graphics.add_animation("idle_right", 0, 1)
        self.graphics.add_animation("move_left", 1, 1)
        self.graphics.add_animation("move_right", 2, 1)
        self.graphics.add_animation("move_up", 3, 1)
        self.graphics.add_animation("move_down", 4, 1)
    
    def update(self, delta):
        self.move_force = Vector2(0, 0)
        for action in self.key_map.keys():
            if self.check_action(action):
                self.command_map[action].execute(self)
        if self.move_force.length() > 0:
            self.dir = self.move_force.normalize()
            self.move_force = self.dir * delta

        self.fsm.update()

        self.update_bbox()
    
    def check_action(self, action, just_pressed = False):
        if just_pressed:
            return service_locator.game_input.key_pressed(self.key_map[action])
        return service_locator.game_input.key_down(self.key_map[action])
    
    def add_to_move_dir(self, new_dir):
        self.move_force.x += new_dir.value[0]
        self.move_force.y += new_dir.value[1]

    # --- || State Callbacks || ---
    
    def idle(self, new = False):
        if new:
            self.colour = (0, 255, 0)
            if self.graphics.current_anim != "idle_right":
                self.graphics.play("idle_right")

        if self.move_force.length() != 0:
            self.fsm.change_state(States.MOVING)

    def moving(self, new = False):
        if new:
            self.colour = (255, 255, 0)

        self.pos = self.pos + self.stats.speed * self.move_force

        if self.dir.x < 0:
            self.graphics.play("move_left")
        elif self.dir.x > 0:
            self.graphics.play("move_right")
        elif self.dir.y < 0:
            self.graphics.play("move_up")
        elif self.dir.y > 0:
            self.graphics.play("move_down")

        if self.move_force.length() == 0:
            self.fsm.change_state(States.IDLE)
