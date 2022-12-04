from common import *

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