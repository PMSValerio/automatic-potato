from enum import Enum
import pygame
from pygame import Vector2

from common import *
from services import service_locator
from player_data import player_data
from entity import Entity
from animation import Animation

from fsm import FSM
from player_commands import *

class States(Enum):
    IDLE = 0
    MOVING = 1

HEAL_RATE = 5 # when in healing zone, heal 5 per sec

class Player(Entity):
    def __init__(self, pos):
        Entity.__init__(self, pos, EntityLayers.PLAYER)

        self.shoot_dir = Vector2(1, 0)
        self.shoot_cooldown = 0.2 # sec
        self.shoot_timer = 0

        self.move_force : Vector2 = Vector2(0, 0) # different from dir, only controls movement dir

        self.stats = player_data.player_type

        self.health = 0
        self.change_health(self.stats.max_health)

        self.fsm = FSM()
        self.fsm.add_state(States.IDLE, self.idle, True)
        self.fsm.add_state(States.MOVING, self.moving)

        self.command_map = {
            "move_left": MoveLeft(),
            "move_right": MoveRight(),
            "move_up": MoveUp(),
            "move_down": MoveDown(),
            "shoot": Shoot(),
        }
        self.dir_map = {
            "move_left": Directions.LEFT,
            "move_right": Directions.RIGHT,
            "move_up": Directions.UP,
            "move_down": Directions.DOWN,
        }

        self.graphics = Animation("assets/gfx/player.png", True, 5) # animation object
    
    def update(self, delta):
        # update move action
        self.move_force = Vector2(0, 0)
        for action in ["move_left", "move_right", "move_up", "move_down"]:
            if self.check_action(action):
                self.command_map[action].execute(self)
                self.shoot_dir.xy = self.dir_map[action].value
        if self.move_force.length() > 0:
            self.dir = self.move_force.normalize()
            self.move_force = self.dir * delta
        
        # update shoot action
        if self.shoot_timer > 0:
            self.shoot_timer -= delta
        shoot = self.check_action("shoot")
        if shoot and self.shoot_timer <= 0:
            self.command_map["shoot"].execute(self)
            self.shoot_timer = self.shoot_cooldown

        if self.pos.distance_to(Vector2(WIDTH * 0.5, HEIGHT * 0.5)) <= HEAL_RANGE:
            self.change_health(HEAL_RATE * delta)

        self.fsm.update()

        self.update_bbox()

        # TODO: remove
        self.change_health(-delta)
    
    def check_action(self, action, just_pressed = False):
        if just_pressed:
            return service_locator.game_input.key_pressed(player_data.key_map[action])
        return service_locator.game_input.key_down(player_data.key_map[action])
    
    def add_to_move_dir(self, new_dir):
        self.move_force.x += new_dir.value[0]
        self.move_force.y += new_dir.value[1]
    
    def change_health(self, amount):
        self.health = max(0, min(self.health + amount, self.stats.max_health))
        service_locator.event_handler.publish("new_health", self.health)

    # --- || State Callbacks || ---
    
    def idle(self, new = False):
        if new:
            if self.graphics.current_anim != "idle_right":
                self.graphics.play("idle_right")

        if self.move_force.length() != 0:
            self.fsm.change_state(States.MOVING)

    def moving(self, new = False):

        self.pos = self.pos + self.stats.speed * self.move_force

        if self.dir.y < 0:
            self.graphics.play("move_up")
        elif self.dir.y > 0:
            self.graphics.play("move_down")
        elif self.dir.x < 0:
            self.graphics.play("move_left")
        elif self.dir.x > 0:
            self.graphics.play("move_right")

        if self.move_force.length() == 0:
            self.fsm.change_state(States.IDLE)
