from common import * 
from pygame import Vector2
import enemy
import animation
import player_data
import entity
from vfx import VisualEffect


class PumpkinHitbox(entity.Entity):
    # an enemy attack that happens in place and disappears when colliding 
    def __init__(self, strength, position : Vector2, p_type):
        entity.Entity.__init__(self, position, EntityLayers.ENEMY_ATTACK)
        self.stats = p_type
        self.dir = Vector2(0, 0)
        self.strength = strength

    def update(self, delta):
        pass

    def draw(self, surface):
        pass

    def collide(self, other):
        self.die()
        VisualEffect(self.pos.copy(), self.stats.hit_effect)


class Pumpkin(enemy.Enemy):
    def __init__(self):
        super().__init__(enemy.EnemyTypes.PUMPKIN, EntityLayers.ENEMY)

        self.graphics = animation.Animation("assets/gfx/entities/pumpkin.png", True, 4)
        self.wander_pos = super().get_wandering_position(250, 300) 
        self.flee_pos = super().get_flee_position()
        self.move_speed = self.wandering_speed
        
        self.start_timer = False
        self.idle_cooldown = 4
        self.idle_timer = self.idle_cooldown

        self.start_bomb_timer = False
        self.bomb_cooldown = 3
        self.bomb_timer = 0

    def update(self, delta):
        # update position
        super().update(delta)

        if self.start_timer and self.idle_timer > 0:
            self.idle_timer -= delta

        if self.start_bomb_timer and self.bomb_cooldown > 0:
            self.bomb_timer -= delta

    def wandering(self, new):
        if new: 
            self.graphics.play("run", 4)

        self.move_speed = self.wandering_speed

        # get direction to wandering position
        super().update_move_dir(self.wander_pos)

        # get player's position 
        self.player_pos = player_data.player_data.get_player_pos()

        # reached wandering position, recalculate
        if self.pos.distance_to(self.wander_pos) < 1: 
            self.fsm.change_state(EnemyStates.IDLE)

        # if within center range, change to seeking state
        elif self.pos.distance_to(self.target_pos) < self.seek_distance: 
            self.target = self.target_pos
            self.fsm.change_state(enemy.EnemyStates.SEEKING)
        
        # if within attack range, change to seeking state
        elif self.pos.distance_to(self.player_pos) < self.attack_range:
            self.fsm.change_state(enemy.EnemyStates.ATTACKING)


    def idle(self, new):
        if new: 
            # play idle animation and stop moving, start timer 
            self.start_timer = True
            self.move_speed = 0
            self.graphics.play("idle", 4)
        
        else:
            # when the timer runs out, back to wandering 
            if self.idle_timer <= 0:
                self.idle_timer = self.idle_cooldown
                self.start_timer = False

                self.wander_pos = super().get_wandering_position(250, 300) 
                self.fsm.change_state(EnemyStates.WANDERING)
    

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
        if new: 
            # self.graphics.play("idle", 4)
            self.move_speed = self.attack_speed
            # commit to the position where the player was in when the attack started
            self.player_pos = player_data.player_data.get_player_pos()
            super().update_move_dir(self.player_pos)
        
        else:
            if self.pos.distance_to(self.player_pos) < 2 and self.bomb_timer <= 0: 
                self.graphics.play("attack", 4)
                self.fsm.change_state(EnemyStates.SHOOTING)
                self.bomb_timer = self.bomb_cooldown

            # when the player leaves their range, go back to seeking
            if self.pos.distance_to(self.player_pos) >= self.attack_range:
                self.fsm.change_state(EnemyStates.SEEKING)
    

    def shooting(self, new):
        if new: 
            self.start_bomb_timer = True
            self.move_speed = 0

        else:
            # when the pumpkin drops on the floor, init hitbox
            if self.graphics.ix == 7:
                PumpkinHitbox(self.strength, self.pos, self.projectile_type)

            # change state when animation ended
            if self.graphics.end:
                self.fsm.change_state(EnemyStates.SEEKING)
        

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
        else:
            player_data.player_data.update_score(self.score_value)  
            self.die()
            super().dying()


    def collide(self, other):
        super().collide(other)


    def damage(self, value):
        super().damage(value)


    def clone(self):
        return Pumpkin()