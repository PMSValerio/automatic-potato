import pygame

class GameInput:
    def __init__(self):
        self.last_keys = None
        self.curr_keys = None
    
    def update(self, delta):
        self.last_keys = self.curr_keys
        self.curr_keys = pygame.key.get_pressed()
    
    def _stable(self):
        return self.last_keys is not None and self.curr_keys is not None
    
    # def any_down(self, filter_list = []):
    #     return len([key for key, v in enumerate(self.curr_keys) if v and (filter_list == [] or key in filter_list)]) > 0
    
    def key_down(self, key_code):
        return self._stable() and self.curr_keys[key_code]
    
    def key_pressed(self, key_code):
        return self._stable() and not self.last_keys[key_code] and self.curr_keys[key_code]
    
    def key_released(self, key_code):
        return self._stable() and self.last_keys[key_code] and not self.curr_keys[key_code]
