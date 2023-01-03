from common import *
from pygame import Vector2
import animation
import enemy
import entity
import player_data

class Ghost(enemy.Enemy):
    def __init__(self):
        super().__init__(enemy.EnemyTypes.GHOST, EntityLayers.ENEMY_MELEE)
        self.graphics = animation.Animation("assets/gfx/entities/ghost.png", True, 4)
        self.wander_pos = super().get_wandering_position(100, 150) 


    def update(self, delta):
        # update position
        super().update(delta)


    def wandering(self, new = False):
        self.move_speed = self.wandering_speed

        # get direction to wandering position
        super().update_move_dir(self.wander_pos)

        # is close to the center of the map
        if self.pos.distance_to(self.target_pos) < self.attack_distance: 
            self.fsm.change_state(EnemyStates.ATTACKING)

        # reached wandering position, recalculate
        if self.pos.distance_to(self.wander_pos) < 2: 
            self.wander_pos = super().get_wandering_position(150, 200) 


    def attacking(self, new):
        # if its the first time entering this state, change to attack speed and calculate 
        # the target position: direction of the center * 1.5, so it dashes through the caldron 
        if new: 
            self.move_speed = self.attack_speed 

            direction = (self.target_pos - self.pos) * 1.5

            self.target = self.target_pos + direction
            self.move_dir = direction.normalize()


        # passed through the center, change to fleeing
        if not new:
            if self.pos.distance_to(self.target) < self.attack_range: 
                self.fsm.change_state(enemy.EnemyStates.FLEEING)

    
    def fleeing(self, new):
        if new:
            self.graphics.play("flee")
        
            # just change the move speed, exit in the same direction as the dash 
            self.move_speed = self.flee_speed 

        # reached flee position
        # deduct from potions left and from the player's score, disappear 
        if super().check_outside_map(self.pos):
            self.die()
            player_data.player_data.update_potions(-1)
            player_data.player_data.update_score(-self.score_value)


    def dying(self, new):
        # when entering this state for the first time, move speed to 0 and play effect
        if new: 
            self.play_effect(entity.Effects.FADE)
            self.move_speed = 0
        
        if self.effect_end:
            player_data.player_data.update_score(self.score_value)  
            self.die()
            super().dying()


    def clone(self):
        return Ghost()