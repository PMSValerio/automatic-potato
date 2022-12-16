import pygame

# adapted from https://www.pygame.org/wiki/Spritesheet
class Spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as message:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit(message)
    
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        # Loads image from x,y,x+offset,y+offset
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        if colorkey == None:
            image.set_colorkey(self.sheet.get_colorkey(), pygame.RLEACCEL)
        else:
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        image.blit(self.sheet, (0, 0), rect)
        return image
    
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        # Loads multiple images, supply a list of coordinates
        return [self.image_at(rect, colorkey) for rect in rects]
    
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        # Loads a strip of images and returns them as a list
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


# simple animation class, plays a series of subimages in a spritesheet in a loop
class Animation:
    def __init__(self, filename, frame_width, frame_height, loop = False, delay_ticks=0):
        self.spritesheet = Spritesheet(filename) # TODO: get from image_loader (Flyweight pattern)
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.loop = loop
        self.delay_ticks = delay_ticks

        # for each key (animaton name), stores a list of images from the strip to be played in sequence
        self.animations = {}

        self.ix = 0
        self.current_anim = ""
        self.paused = False

        self.tick_cnt = 0
    
    # extracts all subimages in a specific row in the spritesheet
    def add_animation(self, anim_name, row, nframes):
        self.animations[anim_name] = self.spritesheet.load_strip((0, self.frame_height * row, self.frame_width, self.frame_height), nframes)
        if self.current_anim == "":
            self.current_anim = anim_name
    
    # set a new animation
    def play(self, animation, delay_ticks=0):
        self.delay_ticks = delay_ticks
        if animation != self.current_anim and animation in self.animations.keys():
            self.current_anim = animation
            self.ix = 0
    
    # pause or unpause
    def toggle_pause(self, pause):
        self.paused = pause
    
    # updates and returns the next frame in the animation
    def get_frame(self):
        frame = self.animations[self.current_anim][self.ix]

        if self.paused: # do not update frame if paused
            return frame

        if self.tick_cnt >= self.delay_ticks:
            self.tick_cnt = 0
            if self.ix + 1 >= len(self.animations[self.current_anim]): # if last frame
                if self.loop:
                    self.ix = 0
            else: # only increment if not last frame
                self.ix += 1
        else:
            self.tick_cnt += 1
        
        return frame
    
    def is_last_frame(self):
        return self.ix == len(self.animations[self.current_anim]) - 1
