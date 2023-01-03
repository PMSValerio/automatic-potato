from enum import Enum
from pygame import Vector2

from common import *
from services import service_locator
from player_data import player_data
from entity import Entity, Effects
from animation import Animation

from fsm import FSM
from player_commands import *

class States(Enum):
    IDLE = 0
    MOVING = 1

class Player(Entity):
    def __init__(self, pos):
        Entity.__init__(self, pos, EntityLayers.PLAYER)

        # upgrade data
        self.speed_modifier = 1 # multiplied to movement speed
        self.invincible_timer = 0 # if > 0, player is invulnerable to enemy attacks

        self.move_force : Vector2 = Vector2(0, 0) # different from dir, only controls movement dir


        self.stats = player_data.player_type
        self.data = player_data

        # weapon data
        self.projectile_type = projectile_types["Spell"] if self.stats.name == "Witch" else projectile_types["Fish"]
        self.shoot_dir = Vector2(1, 0)
        self.shoot_timer = 0

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

        self.graphics = Animation(self.stats.anim_filepath, True, 5) # animation object
    
    def update(self, delta):
        # update move action
        self.move_force.xy = (0, 0)
        new_shoot_dir = Vector2(0, 0)
        for action in ["move_left", "move_right", "move_up", "move_down"]:
            if self.check_action(action):
                self.command_map[action].execute(self)
                new_shoot_dir.x += self.dir_map[action].value[0]
                new_shoot_dir.y += self.dir_map[action].value[1]
        if self.move_force.length() > 0:
            self.dir = self.move_force.normalize()
            self.move_force = self.dir * delta
        if new_shoot_dir.length() > 0:
            self.shoot_dir = new_shoot_dir.normalize()
        
        self.data.update_position(self.pos)

        # update shoot action
        if self.shoot_timer > 0:
            self.shoot_timer -= delta
        shoot = self.check_action("shoot")
        if shoot and self.shoot_timer <= 0:
            self.command_map["shoot"].execute(self)
            self.shoot_timer = self.projectile_type.cooldown

        # check if in healing zone
        if self.pos.distance_to(Vector2(TARGET_X, TARGET_Y)) <= HEAL_RANGE:
            self.change_health(HEAL_RATE * delta)
        
        # update invincibility counter
        self.invincible_timer = max(0, self.invincible_timer - delta)
        
        self.fsm.update()
    
    def collide(self, other):
        if other.col_layer == EntityLayers.ENEMY_MELEE:
            self.change_health(-other.strength)
            
        if other.col_layer == EntityLayers.ENEMY_ATTACK:
            self.change_health(-other.stats.power)
            self.play_effect(Effects.FLASH)
    
    def check_action(self, action, just_pressed = False):
        if just_pressed:
            return service_locator.game_input.key_pressed(player_data.key_map[action])
        return service_locator.game_input.key_down(player_data.key_map[action])
    
    def add_to_move_dir(self, new_dir):
        self.move_force.x += new_dir.value[0]
        self.move_force.y += new_dir.value[1]
    
    def change_health(self, amount):
        self.health = max(0, min(self.health + amount, self.stats.max_health))
        service_locator.event_handler.publish(Events.NEW_HEALTH, self.health)

    # --- || State Callbacks || ---
    
    def idle(self, new = False):
        if new:
            if self.dir.y < 0:
                self.graphics.play("idle_up", 4)
            elif self.dir.y > 0:
                self.graphics.play("idle_down", 4)
            elif self.dir.x < 0:
                self.graphics.play("idle_left", 4)
            elif self.dir.x > 0:
                self.graphics.play("idle_right", 4)

        if self.move_force.length() != 0:
            self.fsm.change_state(States.MOVING)

    def moving(self, new = False):

        self.pos = self.pos + self.stats.speed * self.speed_modifier * self.move_force
        # clamp position inside map borders
        self.pos.x = max(MAP_BORDER_LEFT, min(self.pos.x, MAP_BORDER_RIGHT))
        self.pos.y = max(MAP_BORDER_UP, min(self.pos.y, MAP_BORDER_DOWN))

        if self.dir.y < 0:
            self.graphics.play("move_up", 3)
        elif self.dir.y > 0:
            self.graphics.play("move_down", 3)
        elif self.dir.x < 0:
            self.graphics.play("move_left", 3)
        elif self.dir.x > 0:
            self.graphics.play("move_right", 3)
        
        if self.move_force.length() == 0:
            self.fsm.change_state(States.IDLE)