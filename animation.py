import services

# simple animation class, plays a series of subimages in a spritesheet in a loop
class Animation:
    def __init__(self, filename, loop = False, delay_ticks=0):
        self.filename = filename
        self.loop = loop
        self.delay_ticks = delay_ticks

        self.animations = services.service_locator.graphics_loader.get_file_strips(filename)
        
        self.ix = 0
        self.current_anim = list(self.animations.keys())[0]
        self.paused = False

        self.tick_cnt = 0

        self.end = False # becomes true when the last frame was reached
    
    # set a new animation
    def play(self, animation, delay_ticks=0):
        self.delay_ticks = delay_ticks
        if animation != self.current_anim and animation in self.animations.keys():
            self.current_anim = animation
            self.ix = 0
    
    # pause or unpause
    def toggle_pause(self, pause):
        self.paused = pause
    
    # update frame to next
    def update_frame(self):
        self.end = False
        if not self.paused:
            if self.tick_cnt >= self.delay_ticks:
                self.tick_cnt = 0
                if self.ix + 1 >= len(self.animations[self.current_anim]): # if last frame
                    if self.loop:
                        self.ix = 0
                else: # only increment if not last frame
                    self.ix += 1
            else:
                self.tick_cnt += 1
        if self.ix == len(self.animations[self.current_anim]) - 1:
            self.end = True

    # returns the next frame in the animation
    def get_frame(self):
        return self.animations[self.current_anim][self.ix]
    
    def is_last_frame(self):
        return self.ix == len(self.animations[self.current_anim]) - 1
