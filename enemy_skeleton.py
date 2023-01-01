import enemy
import animation
import player_data
import projectile
from common import *
import entity

class SkeletonProjectile():
    def shoot(self, skely):
        projectile.Projectile(skely.pos.copy(), skely.shoot_dir.copy(), skely.projectile_type)


class Skeleton(enemy.Enemy):
    def __init__(self):
        super().__init__(enemy.EnemyTypes.SKELETON)
        
        self.graphics = animation.Animation("assets/gfx/test.png", True, 5)
        self.wander_pos = super().get_wandering_position() 
        self.move_speed = self.wandering_speed
        self.shoot = False
        self.flee_pos = super().get_flee_position()


    def update(self, delta):
        super().update(delta)

        if self.shoot_timer > 0:
            self.shoot_timer -= delta
        
        if self.shoot and self.shoot_timer <= 0:
            SkeletonProjectile().shoot(self)
            self.shoot_timer = self.projectile_type.cooldown
        
        self.pos += self.move_speed * self.move_dir * delta



    def wandering(self, new = False):
        self.move_speed = self.wandering_speed
        self.player_pos = player_data.player_data.get_player_pos()

        # get direction to wandering position
        super().update_move_dir(self.wander_pos)
        
        # reached wandering position, recalculate
        if self.pos.distance_to(self.wander_pos) < 1: 
            self.wander_pos = super().get_wandering_position() 

        # check how much time elapsed between generating the mob and 
        # rn to see if it's necessary to force change to seek 

        elif self.pos.distance_to(self.target_pos) < self.seek_distance: 
            # TODO remove
            print("from wandering to seek")
            self.fsm.change_state(enemy.EnemyStates.SEEKING)

        elif self.pos.distance_to(self.player_pos) < self.attack_distance:
            # TODO remove
            print("from wandering to attack")
            self.fsm.change_state(enemy.EnemyStates.ATTACKING)


    def seeking(self, new = False):
        self.move_speed = self.seek_speed
        self.player_pos = player_data.player_data.get_player_pos()
        # change move speed to go faster 

        # get direction to the center of the map 
        super().update_move_dir(self.target_pos)

        # if the player is close, change to attack 
        if self.pos.distance_to(self.player_pos) < self.pos.distance_to(self.target_pos):
            # TODO remove
            print("from seek to attack")
            self.fsm.change_state(enemy.EnemyStates.ATTACKING)

        elif self.pos.distance_to(self.target_pos) < 1: 
            # TODO remove
            print("from seek to flee")
            self.fsm.change_state(enemy.EnemyStates.FLEEING)


    def attacking(self, new = False):
        self.move_speed = self.attack_speed 
        self.player_pos = player_data.player_data.get_player_pos()
        # change to attack speed 

        # get direction to the player's position
        super().update_move_dir(self.player_pos)

        if self.pos.distance_to(self.player_pos) < 90: 
            self.shoot = True
            self.shoot_dir = self.move_dir
            return

        elif self.pos.distance_to(self.player_pos) > self.pos.distance_to(self.target_pos):
            # TODO remove
            print("from attack to seek")
            self.shoot = False
            self.fsm.change_state(enemy.EnemyStates.SEEKING)

        # reached center of the map  
        elif self.pos.distance_to(self.target_pos) < 1: 
            # TODO remove
            print("from attack to flee")
            self.shoot = False
            self.fsm.change_state(enemy.EnemyStates.FLEEING)
            

    def fleeing(self, new = False):
        direction = (self.flee_pos - self.pos)
        self.move_dir = direction.normalize()

        # if the enemy is able to escape with potion, deduct score value from player's score
        if self.pos.distance_to(self.flee_pos) < 1: 
            self.die()
            player_data.player_data.update_potions(-1)
            player_data.player_data.update_score(-self.score_value)
            

    def dying(self, new):
        print("die")
        if new: 
            self.play_effect(entity.Effects.FADE)
            self.move_speed = 0
        
        if self.effect_end:
            player_data.player_data.update_score(self.score_value)  
            self.die()


    def collide(self, other):
        super().collide(other)


    def damage(self, value):
        super().damage(value)


    def clone(self):
        return Skeleton()