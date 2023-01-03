from common import *
from pygame import Vector2
import enemy
import animation
import player_data
import projectile
import entity

class SkeletonProjectile():
    def shoot(self, skely):
        projectile.Projectile(skely.pos.copy(), skely.shoot_dir.copy(), skely.projectile_type)


class Skeleton(enemy.Enemy):
    def __init__(self):
        super().__init__(enemy.EnemyTypes.SKELETON, EntityLayers.ENEMY)
        
        self.graphics = animation.Animation("assets/gfx/entities/skeleton.png", True, 4)

        self.move_speed = self.wandering_speed
        self.wander_pos = super().get_wandering_position() 
        self.flee_pos = super().get_flee_position()

        self.shoot_dir = Vector2(1, 0)
        self.shoot_timer = 0
        self.shoot = False

    def update(self, delta):
        # update position
        super().update(delta)

        # update shoot timer 
        if self.shoot_timer > 0:
            self.shoot_timer -= delta
        
        # shoot if activated and cooldown 
        if self.shoot and self.shoot_timer <= 0:
            SkeletonProjectile().shoot(self)
            self.shoot_timer = self.projectile_type.cooldown
        

    def wandering(self, new):
        if new: 
            self.graphics.play("run")

        self.move_speed = self.wandering_speed

        # change direction to wandering position
        super().update_move_dir(self.wander_pos)
        
        self.player_pos = player_data.player_data.get_player_pos()
        
        # reached wandering position, recalculate
        if self.pos.distance_to(self.wander_pos) < 1: 
            self.wander_pos = super().get_wandering_position() 

        # if within center range, change to seeking state
        elif self.pos.distance_to(self.target_pos) < self.seek_distance: 
            self.target = self.target_pos
            self.fsm.change_state(enemy.EnemyStates.SEEKING)
        
        # if within attack range, change to seeking state
        elif self.pos.distance_to(self.player_pos) < self.attack_distance:
            self.fsm.change_state(enemy.EnemyStates.ATTACKING)


    def seeking(self, new):
        if new:
            # change move speed to seek: go faster 
            self.graphics.play("run", 4)
            self.move_speed = self.seek_speed
            super().update_move_dir(self.target_pos)

        # change direction depending on the target (player or caldron)
        self.player_pos = player_data.player_data.get_player_pos()
        
        # if the player is closer than the target and within attack range, change to attack 
        if self.pos.distance_to(self.player_pos) < self.pos.distance_to(self.target_pos) and \
            self.pos.distance_to(self.player_pos) < self.attack_range:
            self.fsm.change_state(enemy.EnemyStates.ATTACKING)

        # if reached the center of the map, change state to fleeing
        elif self.pos.distance_to(self.target_pos) < 1: 
            self.fsm.change_state(enemy.EnemyStates.FLEEING)


    def attacking(self, new):
        # if within attack range, stop and shoot towards the player
        if new:
            self.graphics.play("run", 4)
            self.move_speed = self.attack_speed
        
        super().update_move_dir(self.player_pos)
        self.player_pos = player_data.player_data.get_player_pos()
        
        if self.pos.distance_to(self.player_pos) <= self.attack_range:
            self.fsm.change_state(EnemyStates.SHOOTING)

        # if the target (center) is closer than the player 
        # give up on the chase and start seeking 
        if self.pos.distance_to(self.player_pos) > self.pos.distance_to(self.target_pos):
            self.target = self.target_pos
            self.shoot = False
            self.fsm.change_state(enemy.EnemyStates.SEEKING)


    def shooting(self, new):
        if new:
            self.graphics.play("idle", 4)
            self.move_speed = 0
            self.shoot = True   

        super().update_move_dir(self.player_pos)
        self.player_pos = player_data.player_data.get_player_pos()
        self.shoot_dir = self.move_dir
        
        if self.pos.distance_to(self.player_pos) > self.attack_range:
            self.shoot = False
            self.fsm.change_state(EnemyStates.ATTACKING)


    def fleeing(self, new):
        if new:
            # change to attack speed 
            self.graphics.play("flee", 4)
            self.move_speed = self.flee_speed 
            super().update_move_dir(self.flee_pos)

        # a random feeling goal position was assigned when the instance was created
        # move towards that position and ignore everything else
        # if the enemy is able to escape with potion, i.e not die in the process,
        # deduct score value from player's score and update potion number to -1 
        if self.pos.distance_to(self.flee_pos) < 2: 
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


    def collide(self, other):
        super().collide(other)


    def damage(self, value):
        super().damage(value)


    def clone(self):
        return Skeleton()