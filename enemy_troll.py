import enemy
import animation
import numpy
import player_data

class Troll(enemy.Enemy):
    def __init__(self):
        super().__init__(enemy.EnemyTypes.TROLL)
        
        self.graphics = animation.Animation("assets/gfx/test.png", True, 5)
        self.wander_pos = super().get_wandering_position() 
        self.move_speed = self.wandering_speed


    def update(self, delta):
        super().update(delta)

        self.pos += self.move_speed * self.move_dir * delta


    def wandering(self, new = False):
        self.player_pos = player_data.player_data.get_player_pos()

        # get direction to wandering position
        direction = (self.wander_pos - self.pos)
        self.move_dir = direction / numpy.linalg.norm(direction)
        
        # reached wandering position, recalculate
        if self.pos.distance_to(self.wander_pos) < 1: 
            self.wander_pos = super().get_wandering_position() 

        # check how much time elapsed between generating the mob and 
        # rn to see if it's necessary to force change to seek 

        if self.pos.distance_to(self.target_pos) < self.seek_distance: 
            print("from wandering to seek")
            self.fsm.change_state(enemy.EnemyStates.SEEK)

        if self.pos.distance_to(self.player_pos) < self.attack_distance:
            print("from wandering to attack")
            self.fsm.change_state(enemy.EnemyStates.ATTACK)

    def seek(self, new = False):
        self.move_speed = self.seek_speed
        self.player_pos = player_data.player_data.get_player_pos()
        # change move speed to go faster 

        # get direction to the center of the map 
        direction = (self.target_pos - self.pos) 
        self.move_dir = direction / numpy.linalg.norm(direction)

        # if the player is close, change to attack 
        if self.pos.distance_to(self.player_pos) < self.pos.distance_to(self.target_pos):
            print("from seek to attack")
            self.fsm.change_state(enemy.EnemyStates.ATTACK)

        if self.pos.distance_to(self.player_pos) < 30:
            print("from attack to seek")
            self.fsm.change_state(enemy.EnemyStates.SEEK)


    def attack(self, new = False):
        self.move_speed = self.attack_speed 
        self.player_pos = player_data.player_data.get_player_pos()
        # change to attack speed 

        # get direction to the player's position
        direction = (self.player_pos - self.pos) 
        self.move_dir = direction / numpy.linalg.norm(direction)

        if self.pos.distance_to(self.player_pos) >= 30:
            print("from attack to seek")
            self.fsm.change_state(enemy.EnemyStates.SEEK)
        

    def collide(self, other):
        super().collide(other)


    def damage(self, value):
        super().damage(value)

    def clone(self):
        return Troll()