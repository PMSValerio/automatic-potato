import pygame

from common import *

class GraphicsLoader:

    def __init__(self):
        self.images = {} # image file repository organised by filename
        self.anim_strips = {} # repository of animation strips (dict of dicts) ordered by animation name in file
        self.init_anim_strips()
     

    # adapted from https://www.pygame.org/wiki/Spritesheet
    def load_image(self, filename):
        if not filename in self.images:
            try:
                self.images[filename] = pygame.image.load(get_asset(filename)).convert_alpha()
            except pygame.error as message:
                print('Unable to load spritesheet image:', filename)
                raise SystemExit(message)
        return self.images[filename]
    

    # Load a specific image from a specific rectangle
    def image_at(self, filename, rectangle, colorkey = None, scale = (1, 1)):
        # Loads image from x,y,x+offset,y+offset
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        if colorkey == None:
            image.set_colorkey(self.load_image(filename).get_colorkey(), pygame.RLEACCEL)
        else:
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        
        image.blit(self.load_image(filename), (0, 0), rect)
        if scale != (1, 1):
            image = pygame.transform.scale(image, (rect.width * scale[0], rect.height * scale[1]))
        return image
    

    # Load a whole bunch of images and return them as a list
    def images_at(self, filename, rects, colorkey = None, scale = (1, 1)):
        # Loads multiple images, supply a list of coordinates
        return [self.image_at(filename, rect, colorkey = colorkey, scale = scale) for rect in rects]
    

    # Load a whole strip of images
    def load_strip(self, filename, rect, image_count, colorkey = None, scale = (1, 1)):
        # Loads a strip of images and returns them as a list
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(filename, tups, colorkey = colorkey, scale = scale)
    

    def get_anim_strip(self, filename, anim_name, ix = -1):
        strip = self.anim_strips[filename][anim_name].copy()
        if ix >= 0 and ix < len(strip):
            return strip[ix]
        return strip
    

    def add_anim_strip(self, filename, anim_name, row, wid, hei, nframes, scale = (1, 1)):
        if filename not in self.anim_strips:
            self.anim_strips[filename] = {}
        self.anim_strips[filename][anim_name] = self.load_strip(filename, (0, hei * row, wid, hei), nframes, scale = scale)
    

    def get_file_strips(self, filename):
        return self.anim_strips[filename]
    
    
    # initialise all animation strips used in the game
    def init_anim_strips(self):
        # --Misc--

        filename = "assets/gfx/ui/background.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "default", 0, WIDTH, HEIGHT, 4)

        filename = "assets/gfx/ui/icons.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "potion", 0, 32, 32, 1)

        filename = "assets/gfx/ui/title_cauldron.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "default", 0, 128, 128, 4, (3, 3))

        # --Entities--

        filename = "assets/gfx/entities/witch.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "idle_left", 0, 64, 64, 4, (1.5, 1.5))
        self.add_anim_strip(filename, "idle_right", 1, 64, 64, 4, (1.5, 1.5))
        self.add_anim_strip(filename, "idle_up", 2, 64, 64, 4, (1.5, 1.5))
        self.add_anim_strip(filename, "idle_down", 3, 64, 64, 4, (1.5, 1.5))
        self.add_anim_strip(filename, "move_left", 0, 64, 64, 4, (1.5, 1.5))
        self.add_anim_strip(filename, "move_right", 1, 64, 64, 4, (1.5, 1.5))
        self.add_anim_strip(filename, "move_up", 2, 64, 64, 4, (1.5, 1.5))
        self.add_anim_strip(filename, "move_down", 3, 64, 64, 4, (1.5, 1.5))

        filename = "assets/gfx/entities/cat.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "idle_left", 0, 64, 64, 4, (1.5, 1.5))
        self.add_anim_strip(filename, "idle_right", 1, 64, 64, 4, (1.5, 1.5))
        self.add_anim_strip(filename, "idle_up", 2, 64, 64, 4, (1.5, 1.5))
        self.add_anim_strip(filename, "idle_down", 3, 64, 64, 4, (1.5, 1.5))
        self.add_anim_strip(filename, "move_left", 4, 64, 64, 5, (1.5, 1.5))
        self.add_anim_strip(filename, "move_right", 5, 64, 64, 5, (1.5, 1.5))
        self.add_anim_strip(filename, "move_up", 6, 64, 64, 5, (1.5, 1.5))
        self.add_anim_strip(filename, "move_down", 7, 64, 64, 5, (1.5, 1.5))

        filename = "assets/gfx/entities/pumpkin.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "run", 1, 96, 96, 8, (1.5, 1.5))
        self.add_anim_strip(filename, "idle", 0, 96, 96, 4, (1.5, 1.5))
        self.add_anim_strip(filename, "flee", 2, 96, 96, 8, (1.5, 1.5))
        self.add_anim_strip(filename, "attack", 3, 96, 96, 14, (1.5, 1.5))

        filename = "assets/gfx/entities/skeleton.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "run", 1, 64, 64, 6, (1.5, 1.5))
        self.add_anim_strip(filename, "idle", 0, 64, 64, 4, (1.5, 1.5))
        self.add_anim_strip(filename, "flee", 2, 64, 64, 6, (1.5, 1.5))

        filename = "assets/gfx/entities/ghost.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "run", 0, 64, 64, 4, (1.5, 1.5))
        self.add_anim_strip(filename, "flee", 1, 64, 64, 4, (1.5, 1.5))

        filename = "assets/gfx/entities/ogre.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "run", 1, 192, 96, 6, (1.5, 1.5))
        self.add_anim_strip(filename, "idle", 0, 192, 96, 4, (1.5, 1.5))
        self.add_anim_strip(filename, "attack", 2, 192, 96, 8, (1.5, 1.5))

        filename = "assets/gfx/entities/auto_spud.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "default", 0, 128, 128, 8, (2, 2))

        # --Projectiles--

        filename = "assets/gfx/entities/spell.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "default", 0, 32, 32, 4, (1.5, 1.5))

        filename = "assets/gfx/entities/pbomb.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "default", 0, 32, 32, 8, (1.5, 1.5))

        filename = "assets/gfx/entities/fish.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "default", 0, 32, 32, 1, (1.5, 1.5))

        filename = "assets/gfx/entities/shark.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "default", 0, 64, 64, 2, (1.5, 1.5))
        
        filename = "assets/gfx/entities/potato.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "default", 0, 32, 32, 1, (1.5, 1.5))

        filename = "assets/gfx/entities/bone.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "default", 0, 32, 32, 4, (1.5, 1.5))

        filename = "assets/gfx/vfx/explosion.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "default", 0, 96, 96, 4, (1.5, 1.5))

        # --Pickups--

        filename = "assets/gfx/entities/pickups.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "invuln", 0, 32, 32, 2, (1.5, 1.5))
        self.add_anim_strip(filename, "speed", 1, 32, 32, 2, (1.5, 1.5))
        self.add_anim_strip(filename, "pbomb", 2, 32, 32, 2, (1.5, 1.5))
        self.add_anim_strip(filename, "shark", 3, 32, 32, 2, (1.5, 1.5))

        # --VFX--

        filename = "assets/gfx/vfx/spell_hit.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "default", 0, 32, 32, 4, (1.5, 1.5))

        filename = "assets/gfx/vfx/normal_hit.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "default", 0, 32, 32, 4, (1.5, 1.5))

        filename = "assets/gfx/vfx/null_hit.png"
        self.load_image(filename)
        self.add_anim_strip(filename, "default", 0, 32, 32, 4, (1.5, 1.5))
