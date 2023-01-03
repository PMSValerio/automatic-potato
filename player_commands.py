from common import *
from projectile import *

class MoveLeft:
    def execute(self, player):
        player.add_to_move_dir(Directions.LEFT)

class MoveRight:
    def execute(self, player):
        player.add_to_move_dir(Directions.RIGHT)

class MoveUp:
    def execute(self, player):
        player.add_to_move_dir(Directions.UP)

class MoveDown:
    def execute(self, player):
        player.add_to_move_dir(Directions.DOWN)

class Shoot:
    def execute(self, player):
        if player.projectile_type.name == "Spell":
            Spell(player.pos.copy(), player.shoot_dir.copy())
        else:
            PBomb(player.pos.copy(), player.shoot_dir.copy())
