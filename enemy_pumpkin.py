from common import * 
import enemy
import animation
class Pumpkin(enemy.Enemy):
    def __init__(self):
        super().__init__(enemy.EnemyTypes.PUMPKIN, EntityLayers.ENEMY)

        self.graphics = animation.Animation("assets/gfx/entities/pumpkin.png", True, 4)
        self.wander_pos = super().get_wandering_position(100, 150) 
        self.move_speed = self.wandering_speed
        
        self.start_timer = False
        self.idle_cooldown = 4
        self.idle_timer = 4

    def update(self, delta):
        # update position
        super().update(delta)

        if self.start_timer and self.idle_timer > 0:
            self.idle_timer -= delta


    def wandering(self, new):
        if new: 
            self.graphics.play("run", 4)

        self.move_speed = self.wandering_speed

        # get direction to wandering position
        super().update_move_dir(self.wander_pos)

        # reached wandering position, recalculate
        if self.pos.distance_to(self.wander_pos) < 1: 
            self.fsm.change_state(EnemyStates.IDLE)


    def idle(self, new):
        if new: 
            self.start_timer = True
            self.move_speed = 0
            self.graphics.play("idle", 4)
        
        else:
            if self.idle_timer <= 0:
                self.idle_timer = self.idle_cooldown
                self.start_timer = False

                self.wander_pos = super().get_wandering_position(100, 150)
                self.fsm.change_state(EnemyStates.WANDERING)
    
    def dying(self, new):
        if new:
            pass
        else:
            super().dying()

    def clone(self):
        return Pumpkin()