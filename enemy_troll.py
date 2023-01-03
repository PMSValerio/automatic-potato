from common import *
import enemy 
import animation
import player_data
import entity

class Troll(enemy.Enemy):
    def __init__(self):
        super().__init__(enemy.EnemyTypes.TROLL, EntityLayers.ENEMY)

        self.fsm.change_state(EnemyStates.SEEKING)
        self.graphics = animation.Animation("assets/gfx/entities/ogre.png", True, 4)
        self.move_speed = self.seek_speed

        self.start_timer = False
        self.steal_cooldown = 3
        self.steal_timer = self.steal_cooldown

    def update(self, delta):
        # update position
        super().update(delta)

        if self.start_timer and self.steal_cooldown > 0:
            self.steal_timer -= delta

    def seeking(self, new):
        super().update_move_dir(self.target_pos)

        if self.pos.distance_to(self.target_pos) < self.attack_range:
            self.fsm.change_state(EnemyStates.ATTACKING)

    def attacking(self, new):
        if new: 
            # self.graphics.play("attack")
            self.move_speed = self.attack_speed
            self.start_timer = True
        
        else: 
            if self.steal_timer <= 0:
                self.steal_timer = self.steal_cooldown
                player_data.player_data.update_potions(-5)
    

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
        return Troll()
