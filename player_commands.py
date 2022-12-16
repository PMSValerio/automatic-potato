from common import *
from player_projectile import PlayerProjectile

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
        PlayerProjectile(player.pos.copy(), player.shoot_dir.copy())
