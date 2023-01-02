import pygame

class GameInput:
    def __init__(self):
        self.last_keys = None
        self.curr_keys = None
        self.last_key_pressed = None
    
    def update(self, delta):
        self.last_keys = self.curr_keys
        self.curr_keys = pygame.key.get_pressed()

        self.last_key_pressed = None
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return False
            if ev.type == pygame.KEYDOWN:
                self.last_key_pressed = ev.key
        
        return True
    
    def _stable(self):
        return self.last_keys is not None and self.curr_keys is not None
    
    def any_down(self):
        return self._stable() and any(self.curr_keys)

    def key_down(self, key_code):
        return self._stable() and self.curr_keys[key_code]
    
    def any_pressed(self):
        return self._stable() and any([t[0] and not t[1] for t in zip(self.curr_keys, self.last_keys)])
    
    def key_pressed(self, key_code):
        return self._stable() and not self.last_keys[key_code] and self.curr_keys[key_code]
    
    def any_released(self):
        return self._stable() and any([not t[0] and t[1] for t in zip(self.curr_keys, self.last_keys)])

    def key_released(self, key_code):
        return self._stable() and self.last_keys[key_code] and not self.curr_keys[key_code]
    
    def get_last_pressed(self):
        return self.last_key_pressed
