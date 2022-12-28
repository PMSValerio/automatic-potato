import pygame

class GraphicsLoader:

    def __init__(self):
        self.images = {} # image file repository organised by filename
        self.anim_strips = {} # repository of animation strips (dict of dicts) ordered by animation name in file
        self.init_anim_strips()
    
    # adapted from https://www.pygame.org/wiki/Spritesheet
    def load_image(self, filename):
        if not filename in self.images:
            try:
                self.images[filename] = pygame.image.load(filename).convert_alpha()
            except pygame.error as message:
                print('Unable to load spritesheet image:', filename)
                raise SystemExit(message)
        return self.images[filename]
    
    # Load a specific image from a specific rectangle
    def image_at(self, filename, rectangle, colorkey = None):
        # Loads image from x,y,x+offset,y+offset
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        if colorkey == None:
            image.set_colorkey(self.load_image(filename).get_colorkey(), pygame.RLEACCEL)
        else:
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        image.blit(self.load_image(filename), (0, 0), rect)
        return image
    
    # Load a whole bunch of images and return them as a list
    def images_at(self, filename, rects, colorkey = None):
        # Loads multiple images, supply a list of coordinates
        return [self.image_at(filename, rect, colorkey) for rect in rects]
    
    # Load a whole strip of images
    def load_strip(self, filename, rect, image_count, colorkey = None):
        # Loads a strip of images and returns them as a list
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(filename, tups, colorkey)
    
    def add_anim_strip(self, filename, anim_name, row, wid, hei, nframes):
        if filename not in self.anim_strips:
            self.anim_strips[filename] = {}
        self.anim_strips[filename][anim_name] = self.load_strip(filename, (0, hei * row, wid, hei), nframes)
    
    def get_file_strips(self, filename):
        return self.anim_strips[filename]
    
    # initialise all animation strips used in the game
    def init_anim_strips(self):
        filename = "assets/gfx/player.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "idle_right", 0, 32, 32, 1)
        self.add_anim_strip(filename, "move_left", 1, 32, 32, 1)
        self.add_anim_strip(filename, "move_right", 2, 32, 32, 1)
        self.add_anim_strip(filename, "move_up", 3, 32, 32, 1)
        self.add_anim_strip(filename, "move_down", 4, 32, 32, 1)

        filename = "assets/gfx/spell.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "default", 0, 32, 32, 4)

        filename = "assets/gfx/speed_pickup.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "default", 0, 32, 32, 1)
