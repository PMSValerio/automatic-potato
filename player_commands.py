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
        name = player.projectile_type.name
        if name == "Spell":
            Spell(player.pos.copy(), player.shoot_dir.copy())
        elif name == "Pumpkin Bomb":
            PBomb(player.pos.copy(), player.shoot_dir.copy())
        elif name == "Fish":
            Fish(player.pos.copy(), player.shoot_dir.copy())
        elif name == "Shark":
            Shark(player.pos.copy(), player.shoot_dir.copy())
